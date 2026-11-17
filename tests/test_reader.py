from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import unittest
from unittest.mock import patch
from src.report import build_report, source_path
from src.build_reader import render, source_directory
from tests.test_report import row


class Tables(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tables=[]
        self.cell=None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag=='table': self.tables.append([])
        if tag=='tr': self.tables[-1].append([])
        if tag in ('td','th'): self.cell=[]

    def handle_data(self, text):
        if self.cell is not None: self.cell.append(text)

    def handle_endtag(self, tag):
        if tag in ('td','th'):
            self.tables[-1][-1].append(''.join(self.cell))
            self.cell=None

    def with_header(self, header):
        matches=[t for t in self.tables if t[0]==header]
        if len(matches)!=1: raise AssertionError(f'Expected one table: {header}')
        return matches[0][1:]


class ReaderTests(unittest.TestCase):
    def test_null_estimates_render_in_the_correct_cells(self):
        calibration={'cells':[{'model':1,'N':300,'true_beta':2.,'bias':.001,
                              'cp_interval_99pct_family':[.03,.07],'outer_tests':2000,'rejections_at_005':100}]}
        ps={'selected_pairs':0,'not_precision_audited_pairs':62150,
            'models':{m:{s:0 for s in ('rejected','non_rejected','unresolved')} for m in ('f1','f2')},'strata':[]}
        for count in (0,5):
            with self.subTest(count=count):
                a={1:row(1,count,count,1,.5)}
                report=build_report(a,deepcopy(a))
                result=render(report,ps,[],calibration,'a'*64)
                parsed=Tables(result)
                moments=parsed.with_header(['Model','Accepted books','Mean β','SD (population)','SD (sample)','Paper mean / SD'])
                expected=[['f1','0','unavailable','unavailable','unavailable','2.03 / 0.15'],
                          ['f2','0','unavailable','unavailable','unavailable','2.02 / 0.17']] if count==0 else [
                          ['f1','1','2.0000','0.0000','unavailable','2.03 / 0.15'],
                          ['f2','1','2.1000','0.0000','unavailable','2.02 / 0.17']]
                self.assertEqual(moments,expected)
                stability=parsed.with_header(['Model','Accepted A','Accepted B','A only','B only','Switches','Relative net change','κ'])
                self.assertEqual(stability,[[m,str(int(count>=5)),str(int(count>=5)),
                                            '0','0','0 (0.00%)','unavailable' if count==0 else '+0.00%','unavailable'] for m in ('f1','f2')])
                gates=parsed.with_header(['Comparison','Run minus paper','Allowed difference','Outcome'])
                self.assertEqual(gates[-1][1], 'unavailable' if count==0 else '-1.722149')
                for token in ('None','NaN','@@'): self.assertNotIn(token,result)
                self.assertEqual(result,render(report,ps,[],calibration,'a'*64))

    def test_historical_windows_paths_resolve_on_posix(self):
        with patch('src.build_reader.Path',PurePosixPath), patch('src.build_reader.ROOT',PurePosixPath('/project')):
            self.assertEqual(source_directory({'path':r'results\pass-A'}),PurePosixPath('/project/results/pass-A'))
            self.assertEqual(source_directory({'path':'results/pass-B'}),PurePosixPath('/project/results/pass-B'))
            self.assertEqual(source_directory({'path':'/relocated/B'}),PurePosixPath('/relocated/B'))

    def test_explicit_pass_paths_override_serialized_locations(self):
        for key in ('A','B'):
            override=Path('relocated')/key
            self.assertEqual(source_directory({'path':'nonexistent/original'},override),override)

    def test_report_paths_are_project_relative_and_portable(self):
        root=Path(__file__).resolve().parents[1]
        self.assertEqual(source_path(root/'results/pass-A'),'results/pass-A')
        self.assertEqual(source_path(root.parent/'external-pass'),(root.parent/'external-pass').as_posix())

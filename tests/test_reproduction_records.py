import unittest
import math
import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from src.reproduce import validate_book_result,require_manifest_for_checkpoint,validate_calibration


class ReproductionRecordTests(unittest.TestCase):
    def setUp(self):
        self.source={'pg_id':'302','N':'27','L':'1029','sha256':'a'*64}
        model={'B':100,'K_ge':5,'K_gt':4,'ties':1,'raw_float_ties':1,'ks_refinements':1,
               'inverse_refinements':0,'large_integers':0,'beta':2.,'D':.1}
        self.row={'pg_id':302,'N':27,'L':1029,'source_sha256':'a'*64,'pass_seed':2026111703,
                  'f1':deepcopy(model),'f2':deepcopy(model),
                  'lr':{'R':1.,'variance':1.,'p_lr':math.erfc(1/math.sqrt(54)),
                        'p_lr_sample':math.erfc(1/math.sqrt(54*27/26)),'degenerate':False}}

    def test_pass_seed_and_source_identity(self):
        validate_book_result(self.row,self.source,2026111703)
        for key,value in (('pass_seed',2026111704),('source_sha256','b'*64),('L',1028)):
            row=deepcopy(self.row);row[key]=value
            with self.assertRaises(ValueError): validate_book_result(row,self.source,2026111703)

    def test_malformed_counts_and_fit_rejected(self):
        for key,value in (('K_ge',101),('K_gt',6),('ties',0),('B',99),('beta',float('nan')),('D',2.)):
            row=deepcopy(self.row);row['f1'][key]=value
            with self.assertRaises(ValueError): validate_book_result(row,self.source,2026111703)

    def test_orphan_checkpoint_is_not_adopted(self):
        workspace=Path(__file__).resolve().parents[1]/'work'
        workspace.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=workspace) as temporary:
            folder=Path(temporary).resolve()
            self.assertTrue(folder.is_relative_to(workspace.resolve()))
            checkpoint=folder/'books.jsonl';checkpoint.write_bytes(b'{"pg_id":302}\n')
            with self.assertRaises(ValueError): require_manifest_for_checkpoint(checkpoint,folder/'manifest.json')

    def test_summary_claim_cannot_replace_calibration_records(self):
        manifest={'mode':'full','random_engine':'PCG64','B':100,'main_outer':2000,'diagnostic_outer':200,
                  'main_N':[300,3000,30000],'diagnostic_N':[27,84,210347],'betas':[1.5,2.,3.]}
        def read(path):
            if path.name=='summary.json': return json.dumps({'complete':True,'calibration_pass':True,'completed_tasks':39600}).encode()
            if path.name=='manifest.json': return json.dumps(manifest).encode()
            raise FileNotFoundError(path)
        with patch.object(Path,'read_bytes',read):
            with self.assertRaises(FileNotFoundError): validate_calibration(Path('missing-calibration-fixture'))

    def test_lr_p_values_rederived(self):
        row=deepcopy(self.row);row['lr']['p_lr']=.5
        with self.assertRaises(ValueError): validate_book_result(row,self.source,2026111703)

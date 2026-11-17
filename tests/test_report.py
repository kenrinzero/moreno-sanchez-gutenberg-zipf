from copy import deepcopy
import unittest
from src.report import build_report


def row(pg,k1,k2,R,p,p_sample=None):
    return {'pg_id':pg,'N':100,'L':pg*100,'source_sha256':'a'*64,
            'f1':{'K_ge':k1,'K_gt':max(0,k1-1),'beta':2.,'D':.1},
            'f2':{'K_ge':k2,'K_gt':max(0,k2-1),'beta':2.1,'D':.11},
            'lr':{'R':R,'p_lr':p,'p_lr_sample':p if p_sample is None else p_sample,'degenerate':False}}


class ReportArithmeticTests(unittest.TestCase):
    def test_signed_cells_and_neither_exclusion(self):
        rows=[row(1,5,0,1,.01),row(2,0,5,-1,.01),row(3,6,6,-1,.01,.06),row(4,0,0,-1,.01)]
        a={r['pg_id']:r for r in rows};b=deepcopy(a)
        b[1]['f1']['K_ge']=4;b[2]['f1']['K_ge']=5
        report=build_report(a,b)
        self.assertEqual([g['observed'] for g in report['table1']['total_lr']],[1,2,3])
        self.assertEqual([g['observed'] for g in report['table2']['total_first_three_rows']],[1,2])
        self.assertEqual([g['observed'] for g in report['table2']['neither']],[0,1])
        self.assertEqual(report['strict_p_sensitivity'],{'both':1,'neither':3})
        self.assertEqual(report['sample_variance_lr_sensitivity']['total_first_three_rows'],[1,1])
        self.assertEqual(report['stability']['f1']['A_only'],1)
        self.assertEqual(report['stability']['f1']['B_only'],1)
        self.assertTrue(report['plus_one_p_sensitivity']['centile_grid_classifications_identical'])

    def test_empty_acceptance_is_unavailable_not_nan(self):
        a={1:row(1,0,0,1,.5)}
        report=build_report(a,deepcopy(a))
        self.assertIsNone(report['acceptance_ratio']['observed'])
        self.assertFalse(report['acceptance_ratio']['pass'])
        self.assertIsNone(report['beta_moments']['f1']['mean'])
        self.assertIsNone(report['beta_moments']['f1']['sd_sample'])
        self.assertIsNone(report['stability']['f1']['kappa'])

    def test_deterministic_drift_rejected(self):
        a={1:row(1,5,5,1,.5)};b=deepcopy(a);b[1]['f1']['beta']=2.01
        with self.assertRaises(ValueError): build_report(a,b)

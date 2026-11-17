import unittest
from copy import deepcopy
from src.calibrate import summarize,BETAS,MAIN_N,DIAGNOSTIC_N,cp_interval


class CalibrationRecordTests(unittest.TestCase):
    def rows(self):
        return [dict(key=f'{model}:{N}:{index}:{outer}',model=model,N=N,true_beta=beta,
                     outer_index=outer,B=100,beta=beta,K_ge=5,K_gt=5,ties=0,raw_float_ties=0,
                     elapsed_seconds=.1,ks_refinements=0,inverse_refinements=0,
                     outer_inverse_refinements=0,large_integers=0,outer_large_integers=0)
                for model in (1,2) for N in MAIN_N+DIAGNOSTIC_N
                for index,beta in enumerate(BETAS) for outer in range(2)]

    def test_missing_duplicate_and_misidentified_jobs_rejected(self):
        rows=self.rows()
        for bad in (rows[:-1],rows[:-1]+[rows[0]]):
            with self.assertRaises(ValueError): summarize(bad,'benchmark')
        bad=deepcopy(rows);bad[0]['N']=30000
        with self.assertRaises(ValueError): summarize(bad,'benchmark')

    def test_benchmark_never_satisfies_full_gate(self):
        result=summarize(self.rows(),'benchmark')
        self.assertFalse(result['complete'])
        self.assertFalse(result['calibration_pass'])
        self.assertEqual(len(result['cells']),36)
        self.assertTrue(all(len(c['K_ge_histogram'])==101 for c in result['cells']))

    def test_binomial_interval_boundaries(self):
        lower,upper=cp_interval(0,100,.05)
        self.assertEqual(lower,0.)
        self.assertAlmostEqual(upper,1-.025**.01,places=13)
        lower,upper=cp_interval(100,100,.05)
        self.assertEqual(upper,1.)
        self.assertAlmostEqual(lower,.025**.01,places=13)

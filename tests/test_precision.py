from copy import deepcopy
import unittest
from src.precision import select_pairs,validate_pair
from src.calibrate import cp_interval


class PrecisionTests(unittest.TestCase):
    def test_selection_bounds_and_order_independence(self):
        books={i:{'pg_id':i,'f1':{'K_ge':i%22,'beta':2.,'D':.01},
                  'f2':{'K_ge':i%22,'beta':2.1,'D':.02}} for i in range(1,2001)}
        a=select_pairs(books)
        self.assertEqual(a,select_pairs(dict(reversed(list(books.items())))))
        self.assertEqual(len(a),400)
        self.assertEqual(len({(r['model'],r['pg_id']) for r in a}),400)
        for r in a:
            self.assertLessEqual(r['stratum'][0],r['selecting_K'])
            self.assertLessEqual(r['selecting_K'],r['stratum'][1])
        self.assertEqual(select_pairs({}),[])

    def test_interval_and_selection_custody(self):
        selection={'model':1,'pg_id':123,'stratum':[4,5],'candidate_count':70,
                   'selecting_K':5,'beta_expected':2.,'D_expected':.01}
        metadata={'N':'100','L':'500','sha256':'a'*64}
        for K,status in ((0,'rejected'),(500,'unresolved'),(10000,'non_rejected')):
            result={**selection,'N':100,'L':500,'seed':2026111705,'B':10000,
                    'source_sha256':'a'*64,'beta':2.,'D':.01,'K_ge':K,'K_gt':K,
                    'ties':0,'raw_float_ties':0,'ks_refinements':0,'inverse_refinements':0,
                    'large_integers':0,'cp95':list(cp_interval(K,10000,.05)),
                    'precision_status':status,'worst_case_mc_se':.005}
            validate_pair(result,selection,metadata)
            for key,value in (('model',True),('pg_id',123.),('selecting_K',4),
                              ('K_ge',10001),('cp95',[0.,1.]),('precision_status','invented')):
                broken=deepcopy(result);broken[key]=value
                with self.assertRaises(ValueError): validate_pair(broken,selection,metadata)

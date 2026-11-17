import math
import unittest
import mpmath as mp
import numpy as np
from src.models import Histogram,HeadTailSampler,exact_inverse_floor,fit,ks,logmass,survival,likelihood_ratio
from src.reference import high_precision_fit_ks,compare_refined_ks
from src.bootstrap import bootstrap


class NumericalTests(unittest.TestCase):
    def test_rejects_lossy_input_and_overflow(self):
        for x,c in (([1.5],[1]),([1],[1.5]),([1],[[2]]),([1],[True]),([True],[1]),([1],[2**63]),([1,2],[2**62,2**62])):
            with self.assertRaises(ValueError): Histogram.from_counts(x,c)
        for values in ([1.2],[True],[0],[-1],[[1]]):
            with self.assertRaises(ValueError): Histogram.from_sample(values)

    def test_normalization_and_beta2_identities(self):
        h=Histogram.from_counts(range(1,1001),np.ones(1000,dtype=int))
        for model in (1,2):
            for beta in (1.1,1.5,2.,3.,4.):
                mass=np.exp(logmass(model,beta,h)).sum()
                tail=survival(model,beta,np.array([math.log(1001)]),np.array([1/1001]))[0]
                self.assertAlmostEqual(mass+tail,1.,places=12)
        self.assertAlmostEqual(math.exp(logmass(1,2.,h)[0]),6/math.pi**2,places=14)
        self.assertAlmostEqual(math.exp(logmass(2,2.,h)[0]),.5,places=14)

    def test_high_precision_mass_survival_extreme_support(self):
        support=(1,2,3,64,65,10**8,2**60,10**500)
        h=Histogram.from_counts(support,[1]*len(support))
        with mp.workdps(650):
            for model in (1,2):
                for beta in (1.1,1.5,2.,3.,4.):
                    logs=logmass(model,beta,h)
                    sf=survival(model,beta,h.logn,h.inverse)
                    b=mp.mpf(beta)
                    for i,x in enumerate(support):
                        n=mp.mpf(x)
                        pmf=n**(-b)/mp.zeta(b) if model==1 else n**(1-b)-(n+1)**(1-b)
                        surv=mp.zeta(b,n)/mp.zeta(b) if model==1 else n**(1-b)
                        self.assertLessEqual(abs(logs[i]-float(mp.log(pmf))),1e-10)
                        self.assertLessEqual(abs(sf[i]-float(surv)),1e-12)

    def test_ks_against_full_integer_grid(self):
        h=Histogram.from_counts([2,7,29],[5,2,1])
        grid=np.arange(1,31)
        empirical=np.array([sum(c for x,c in zip(h.support,h.counts) if x>=n)/h.N for n in grid])
        for model in (1,2):
            for beta in (1.5,2.,3.,4.):
                theoretical=survival(model,beta,np.log(grid),1/grid)
                self.assertAlmostEqual(ks(model,beta,h),float(np.max(abs(empirical-theoretical))),places=14)

    def test_mle_and_final_ks_against_independent_reference(self):
        for h in (Histogram.from_counts([1,2,3,11],[300,90,40,4]),Histogram.from_counts([1,8,100],[3,7,2])):
            for model in (1,2):
                beta=fit(model,h)
                ref_beta,ref_ks=high_precision_fit_ks(model,h)
                self.assertLessEqual(abs(beta-float(ref_beta)),1e-9)
                self.assertLessEqual(abs(ks(model,beta,h)-float(ref_ks)),1e-12)

    def test_constrained_boundary(self):
        h=Histogram.from_counts([1],[27])
        for model in (1,2):
            self.assertEqual(fit(model,h),4.)
            ref_beta,ref_ks=high_precision_fit_ks(model,h)
            self.assertEqual(ref_beta,4)
            self.assertLessEqual(abs(ks(model,4,h)-float(ref_ks)),1e-12)

    def test_inverse_integer_boundaries_and_large_values(self):
        for a in (1,65):
            for beta in (1.5,2.,3.,4.,1.23456789):
                self.assertEqual(exact_inverse_floor(1.,beta,a),a)
                for u in (.5,.25,math.ldexp(1.,-53),float(np.nextafter(.5,0)),float(np.nextafter(.5,1))):
                    n=exact_inverse_floor(u,beta,a)
                    with mp.workdps(200):
                        uu=mp.mpf(u)
                        t=mp.mpf(beta)-1
                        self.assertLessEqual(uu,(mp.mpf(a)/n)**t)
                        self.assertGreater(uu,(mp.mpf(a)/(n+1))**t)

    def test_sampler_probabilities_and_reproducibility(self):
        N=200000
        for model in (1,2):
            sampler=HeadTailSampler(model,2.)
            h=sampler.sample(N,np.random.default_rng(np.random.SeedSequence([2026111702,1,model])))
            for n in (1,2,10,64,65,1000):
                observed=sum(c for x,c in zip(h.support,h.counts) if x>=n)/N
                with mp.workdps(40):
                    expected=float(mp.zeta(2,n)/mp.zeta(2)) if model==1 else 1/n
                self.assertLessEqual(abs(observed-expected),6*math.sqrt(expected*(1-expected)/N)+1/N)
            a=HeadTailSampler(model,1.5).sample(300,np.random.default_rng(42))
            b=HeadTailSampler(model,1.5).sample(300,np.random.default_rng(42))
            self.assertEqual(a.support,b.support)
            np.testing.assert_array_equal(a.counts,b.counts)

    def test_independent_direct_sampler_agreement(self):
        # Different algorithms: NumPy's Zipf RNG and scalar rational inversion at beta2.
        N=100000
        for model in (1,2):
            rng=np.random.default_rng([2026111702,2,model])
            values=rng.zipf(2.,N) if model==1 else [int(1/u) for u in 1-rng.random(N)]
            direct=Histogram.from_sample(values)
            headtail=HeadTailSampler(model,2.).sample(N,np.random.default_rng([2026111702,3,model]))
            for threshold in (2,3,10,65,1000):
                p=sum(c for n,c in zip(direct.support,direct.counts) if n>=threshold)/N
                q=sum(c for n,c in zip(headtail.support,headtail.counts) if n>=threshold)/N
                pooled=(p+q)/2
                self.assertLessEqual(abs(p-q),6*math.sqrt(2*pooled*(1-pooled)/N)+2/N)

    def test_refined_comparison_has_structural_ties(self):
        a=Histogram.from_counts([1,2],[99,1])
        b=Histogram.from_counts([1,3],[99,1])
        for model in (1,2):
            self.assertEqual(fit(model,a),4.)
            self.assertEqual(fit(model,b),4.)
            self.assertEqual(compare_refined_ks(model,a,b),0)

    def test_compressed_likelihood_and_lr_degenerate(self):
        h=Histogram.from_counts([1,2,7],[4,3,2])
        expanded=Histogram.from_sample([1]*4+[2]*3+[7]*2)
        for model in (1,2):
            with mp.workdps(50):
                direct=sum(mp.log(mp.mpf(n)**-2/mp.zeta(2) if model==1 else mp.mpf(1)/n-mp.mpf(1)/(n+1)) for n in [1]*4+[2]*3+[7]*2)
            self.assertLessEqual(abs(float(np.dot(h.counts,logmass(model,2,h)))-float(direct)),1e-12)
        degenerate=likelihood_ratio(Histogram.from_counts([1],[100]),2.,2.)
        self.assertTrue(degenerate['degenerate'])
        self.assertIsNone(degenerate['p_lr'])

    def test_bootstrap_counts_and_exact_ties(self):
        h=Histogram.from_counts([1],[1])
        for B in (0,-1,1.5,True):
            with self.assertRaises(ValueError): bootstrap(1,h,B,np.random.default_rng(1))
        for model in (1,2):
            r=bootstrap(model,h,10,np.random.default_rng(123))
            self.assertEqual(r['K_ge'],r['K_gt']+r['ties'])
            self.assertGreater(r['ties'],0)
            self.assertEqual(r['B'],10)

    def test_mle_parameter_error_across_regimes(self):
        for model in (1,2):
            for index,beta in enumerate((1.1,1.5,2.,3.,3.8)):
                h=HeadTailSampler(model,beta).sample(80,np.random.default_rng([2026111702,20+index,model]))
                reference,_=high_precision_fit_ks(model,h)
                self.assertLessEqual(abs(fit(model,h)-float(reference)),1e-9)

    def test_near_one_parameter_amplification(self):
        h=Histogram.from_counts([10**500],[1])
        for model in (1,2):
            reference,reference_ks=high_precision_fit_ks(model,h)
            beta=fit(model,h)
            self.assertLessEqual(abs(beta-float(reference)),1e-9)
            self.assertLessEqual(abs(ks(model,beta,h)-float(reference_ks)),1e-12)

    def test_extremely_close_ks_are_not_forced_equal(self):
        a=Histogram.from_counts([1,10**100],[1,1])
        b=Histogram.from_counts([1,10**100+1],[1,1])
        self.assertNotEqual(compare_refined_ks(2,a,b),0)


if __name__=='__main__':
    unittest.main()

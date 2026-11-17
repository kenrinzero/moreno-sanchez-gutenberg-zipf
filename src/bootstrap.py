"""Refitted parametric bootstrap with explicit strict/inclusive counts."""
from .models import HeadTailSampler, fit, ks
from .reference import compare_refined_ks


def bootstrap(model,h,B,rng):
    if isinstance(B,bool) or not isinstance(B,int) or B<=0:
        raise ValueError('B must be a positive integer')
    beta=fit(model,h)
    observed=ks(model,beta,h)
    sampler=HeadTailSampler(model,beta)
    ge=gt=ties=refined=raw_float_ties=0
    for _ in range(B):
        simulated=sampler.sample(h.N,rng)
        fitted=fit(model,simulated)
        statistic=ks(model,fitted,simulated)
        raw_float_ties+=statistic==observed
        # Conservative parameter/CDF ambiguity guard; refine instead of widening ties.
        guard=4e-9/(min(beta,fitted)-1)+4e-12
        if abs(statistic-observed)<=guard:
            refined+=1
            comparison=compare_refined_ks(model,h,simulated)
        else:
            comparison=1 if statistic>observed else -1
        ge+=comparison>=0
        gt+=comparison>0
        ties+=comparison==0
    return {'beta':beta,'D':observed,'B':B,'K_ge':ge,'K_gt':gt,'ties':ties,'raw_float_ties':raw_float_ties,
            'ks_refinements':refined,'inverse_refinements':sampler.refinements,
            'large_integers':sampler.large_integers,'max_log_draw':sampler.max_log_draw}

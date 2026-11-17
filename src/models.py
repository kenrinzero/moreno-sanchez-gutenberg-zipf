"""Numerical f1/f2 kernels and head/tail sampling on unbounded support."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math

import mpmath as mp
import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta, erfc

LOWER = 1.0 + 1e-8


@dataclass
class Histogram:
    support: tuple[int, ...]
    counts: np.ndarray
    logn: np.ndarray
    inverse: np.ndarray
    N: int

    @classmethod
    def from_counts(cls, support, counts):
        raw_x,raw_c = tuple(support),tuple(counts)
        if any(isinstance(v,(bool,np.bool_)) or not isinstance(v,(int,np.integer)) for v in raw_x+raw_c):
            raise ValueError('Support and counts must be exact one-dimensional integers')
        x = tuple(int(n) for n in raw_x)
        c_python = tuple(int(n) for n in raw_c)
        if not x or len(x) != len(c_python) or min(x) < 1 or min(c_python) <= 0:
            raise ValueError('Expected nonempty positive support and multiplicities')
        N = sum(c_python)
        if N > np.iinfo(np.int64).max:
            raise ValueError('Type count exceeds supported int64 multiplicity range')
        c = np.asarray(c_python,dtype=np.int64)
        if any(a >= b for a,b in zip(x,x[1:])):
            raise ValueError('Support must be strictly increasing')
        if x[-1] < 2**1023:
            values = np.asarray(x,dtype=np.float64)
            logs = np.log(values)
            inverse = 1.0/values
        else:
            logs = np.asarray([math.log(n) for n in x])
            inverse = np.exp(-logs)
        return cls(x,c,logs,inverse,N)

    @classmethod
    def from_sample(cls, values):
        values = tuple(values)
        if any(isinstance(n,(bool,np.bool_)) or not isinstance(n,(int,np.integer)) or n<=0 for n in values):
            raise ValueError('Sample must contain positive exact integers')
        counts = Counter(map(int,values))
        support = sorted(counts)
        return cls.from_counts(support,[counts[n] for n in support])


def logmass(model: int, beta: float, h: Histogram) -> np.ndarray:
    if model not in (1,2) or not 1 < beta <= 4:
        raise ValueError('Invalid model or parameter')
    if model == 1:
        return -beta*h.logn - math.log(float(zeta(beta,1)))
    t = beta-1
    q = np.log1p(h.inverse)
    large = h.inverse <= 1e-8
    result = np.empty_like(q)
    result[~large] = -t*h.logn[~large]+np.log(-np.expm1(-t*q[~large]))
    result[large] = math.log(t)-beta*h.logn[large]-.5*beta*h.inverse[large]
    return result


def survival(model: int, beta: float, logs: np.ndarray, inverse: np.ndarray) -> np.ndarray:
    if model not in (1,2) or not 1 < beta <= 4:
        raise ValueError('Invalid model or parameter')
    t = beta-1
    if model == 2:
        return np.exp(-t*logs)
    large = inverse <= 1e-8
    result = np.empty_like(logs)
    result[~large] = zeta(beta,np.exp(logs[~large]))/zeta(beta,1)
    inv = inverse[large]
    result[large] = np.exp(-t*logs[large])/(t*zeta(beta,1))*(1+t*inv/2+t*beta*inv*inv/12)
    return result


def fit(model: int, h: Histogram) -> float:
    meanlog = float(np.dot(h.counts,h.logn)/h.N)
    if model == 1:
        def score(beta):
            step = min(1e-3,(beta-1)*.001)
            # Sixth-order difference permits a wider, less cancellation-prone step.
            zm3,zm2,zm1,zp1,zp2,zp3 = (float(zeta(beta+k*step,1)) for k in (-3,-2,-1,1,2,3))
            derivative = (-zm3+9*zm2-45*zm1+45*zp1-9*zp2+zp3)/(60*step)
            return -derivative/float(zeta(beta,1))-meanlog
    elif model == 2:
        q = np.log1p(h.inverse)
        def score(beta):
            t = beta-1
            small = t*q < 1e-5
            ratio = np.empty_like(q)
            ratio[small] = 1/t-q[small]/2+t*q[small]**2/12
            ratio[~small] = q[~small]/np.expm1(t*q[~small])
            return float(np.dot(h.counts,ratio)/h.N)-meanlog
    else:
        raise ValueError('Invalid model')
    if score(4.0) >= 0:
        return 4.0
    if score(LOWER) <= 0:
        raise ArithmeticError('MLE reaches the open-boundary numerical guard')
    estimate=float(brentq(score,LOWER,4.0,xtol=1e-13,rtol=1e-14))
    if estimate<1.05:
        # Close to one, tiny beta errors are amplified in the survival curve.
        from .reference import high_precision_fit_ks
        reference,reference_ks=high_precision_fit_ks(model,h)
        estimate=float(reference)
        if abs(ks(model,estimate,h)-float(reference_ks))>1e-12:
            raise ArithmeticError('Binary64 beta cannot meet final KS precision')
    return estimate


def ks(model: int, beta: float, h: Histogram) -> float:
    cumulative = np.cumsum(h.counts,dtype=np.float64)/h.N
    before = 1-np.r_[0.0,cumulative[:-1]]
    after = 1-cumulative
    at = survival(model,beta,h.logn,h.inverse)
    nextlogs = h.logn+np.log1p(h.inverse)
    nextinv = h.inverse/(1+h.inverse)
    following = survival(model,beta,nextlogs,nextinv)
    return float(max(np.max(np.abs(before-at)),np.max(np.abs(after-following))))


def likelihood_ratio(h: Histogram, beta1: float, beta2: float) -> dict:
    differences = logmass(1,beta1,h)-logmass(2,beta2,h)
    total = float(np.dot(h.counts,differences))
    variance = 0.0 if np.all(differences==differences[0]) else float(np.dot(h.counts,(differences-total/h.N)**2)/h.N)
    if variance == 0:
        p = 1.0 if total == 0 else None
        return {'R':total,'variance':variance,'p_lr':p,'p_lr_sample':p,'degenerate':total!=0}
    p = float(erfc(abs(total)/math.sqrt(2*h.N*variance)))
    p_sample = float(erfc(abs(total)/math.sqrt(2*h.N*variance*h.N/(h.N-1)))) if h.N>1 else None
    return {'R':total,'variance':variance,'p_lr':p,'p_lr_sample':p_sample,'degenerate':False}


def _integer_root(value: int, degree: int) -> int:
    if degree == 1:
        return value
    low,high = 0,1 << ((value.bit_length()+degree-1)//degree)
    while low+1 < high:
        mid = (low+high)//2
        if mid**degree <= value:
            low = mid
        else:
            high = mid
    return high if high**degree<=value else low


def exact_inverse_floor(u: float, beta: float, a: int) -> int:
    """Certify floor(a*U**(-1/t)) using rational or interval arithmetic."""
    if not 0 < u <= 1 or not 1 < beta <= 4 or a<1:
        raise ValueError('Invalid inverse input')
    if u == 1:
        return a
    numerator,denominator = u.as_integer_ratio()
    p,q = (beta-1).as_integer_ratio()
    if p<=16 and q<=16:
        return _integer_root((a**p*denominator**q)//numerator**q,p)
    digits = max(80,int((math.log(a)-math.log(u)/(beta-1))/math.log(10))+50)
    if digits>10000:
        raise ArithmeticError('Inverse requires more than 10000 decimal digits')
    previous = mp.iv.dps
    try:
        for extra in (0,40,100):
            mp.iv.dps = digits+extra
            u_iv = mp.iv.mpf(numerator)/denominator
            t_iv = mp.iv.mpf(p)/q
            value = a*u_iv**(-1/t_iv)
            lower,upper = int(value.a),int(value.b)
            if lower == upper:
                return lower
        raise ArithmeticError('Inverse integer remains ambiguous')
    finally:
        mp.iv.dps = previous


class HeadTailSampler:
    """Exact categorical decomposition; all exceptional inverse draws retained."""
    def __init__(self, model: int, beta: float, cutoff: int=64):
        if model not in (1,2) or not 1<beta<=4 or cutoff<1:
            raise ValueError('Invalid sampler parameters')
        self.model,self.beta,self.cutoff = model,beta,cutoff
        self.a,self.t = cutoff+1,beta-1
        head = Histogram.from_counts(range(1,cutoff+1),np.ones(cutoff,dtype=int))
        self.probabilities = np.exp(logmass(model,beta,head))
        tail = float(survival(model,beta,np.array([math.log(self.a)]),np.array([1/self.a]))[0])
        if np.any(self.probabilities<0) or not np.isfinite(self.probabilities).all() or abs(self.probabilities.sum()+tail-1)>2e-12:
            raise ArithmeticError('Invalid head/tail probabilities')
        self.probabilities = np.r_[self.probabilities,tail]
        self.refinements = 0
        self.large_integers = 0
        self.max_log_draw = 0.0

    def _tail_proposals(self, count: int, rng) -> list[int]:
        uniforms = 1-rng.random(count)  # (0,1], never silently redraw zero.
        logx = math.log(self.a)-np.log(uniforms)/self.t
        safe = logx < math.log(2**52)
        approximations = np.zeros(count)
        approximations[safe] = np.exp(logx[safe])
        distance = np.abs(approximations-np.rint(approximations))
        tolerance = 64*np.finfo(float).eps*np.maximum(approximations,1)*(1+np.abs(logx))
        refine = ~safe | (distance<=tolerance)
        self.refinements += int(refine.sum())
        values = []
        for i in range(count):
            value = exact_inverse_floor(float(uniforms[i]),self.beta,self.a) if refine[i] else int(approximations[i])
            if value < self.a:
                raise ArithmeticError('Inverse below tail support')
            self.large_integers += int(value>2**52)
            values.append(value)
        if count:
            self.max_log_draw = max(self.max_log_draw,float(logx.max()))
        return values

    def sample(self, N: int, rng) -> Histogram:
        if isinstance(N,(bool,np.bool_)) or not isinstance(N,(int,np.integer)) or N<=0:
            raise ValueError('N must be positive integer')
        head_counts = rng.multinomial(N,self.probabilities)
        needed = int(head_counts[-1])
        tail = []
        while len(tail)<needed:
            proposals = self._tail_proposals(needed-len(tail),rng)
            if self.model == 2:
                tail.extend(proposals)
            else:
                uniforms = rng.random(len(proposals))
                numerator = self.a*(-math.expm1(-self.t*math.log1p(1/self.a)))
                for n,u in zip(proposals,uniforms):
                    if n>10**8:
                        inverse = math.exp(-math.log(n))
                        denominator = self.t*(1-(self.t+1)*inverse/2)
                    else:
                        denominator = n*(-math.expm1(-self.t*math.log1p(1/n)))
                    acceptance = numerator/denominator
                    if not 0 < acceptance <= 1+2e-12:
                        raise ArithmeticError('Invalid rejection probability')
                    if u<=min(acceptance,1.0):
                        tail.append(n)
        frequencies = {i+1:int(c) for i,c in enumerate(head_counts[:-1]) if c}
        frequencies.update(Counter(tail))
        support = sorted(frequencies)
        h = Histogram.from_counts(support,[frequencies[n] for n in support])
        if h.N != N:
            raise ArithmeticError('Sampler changed N')
        return h

"""Independent high-precision formulas used only for numerical certification."""
import math
from fractions import Fraction
import mpmath as mp


def masses(model,beta,n):
    b=mp.mpf(beta)
    return n**(-b)/mp.zeta(b) if model==1 else n**(1-b)-(n+1)**(1-b)


def high_precision_fit_ks(model,h,dps=80,details=False):
    with mp.workdps(dps):
        support=list(map(mp.mpf,h.support))
        counts=list(map(lambda x:mp.mpf(int(x)),h.counts))
        logs=[mp.log(n) for n in support]
        qs=[mp.log1p(1/n) for n in support]
        meanlog=sum(c*x for c,x in zip(counts,logs))/h.N
        def score(b):
            if model==1:
                return -mp.diff(mp.zeta,b)/mp.zeta(b)-meanlog
            return sum(c*q/mp.expm1((b-1)*q) for q,c in zip(qs,counts))/h.N-meanlog
        if score(mp.mpf(4))>=0:
            beta=mp.mpf(4)
            bracket=mp.mpf(0)
        else:
            low,high=mp.mpf(1)+mp.mpf('1e-8'),mp.mpf(4)
            if score(low)<=0:
                raise ArithmeticError('Reference lower boundary')
            for _ in range(math.ceil(dps*math.log2(10))+20):
                mid=(low+high)/2
                if mid==low or mid==high:
                    break
                if score(mid)>0: low=mid
                else: high=mid
            beta=(low+high)/2
            bracket=high-low
        def sf(n):
            return mp.zeta(beta,n)/mp.zeta(beta) if model==1 else n**(1-beta)
        cumulative=0
        candidates=[]
        for integer,c in zip(h.support,h.counts):
            candidates.append((abs(mp.mpf(h.N-cumulative)/h.N-sf(mp.mpf(integer))),(integer,h.N-cumulative)))
            cumulative+=int(c)
            # Add one as an exact Python integer before high-precision conversion.
            candidates.append((abs(mp.mpf(h.N-cumulative)/h.N-sf(mp.mpf(integer+1))),(integer+1,h.N-cumulative)))
        maximum,witness=max(candidates,key=lambda item:item[0])
        alternatives=[value for value,key in candidates if key!=witness]
        gap=maximum-max(alternatives) if alternatives else mp.inf
        return (+beta,+maximum,witness,+gap,+bracket) if details else (+beta,+maximum)


def _equal_f1_parameter(a,b):
    if a.N!=b.N:
        return False
    bit_work=sum(n.bit_length()*int(c) for h in (a,b) for n,c in zip(h.support,h.counts))
    if bit_work>1000000:
        return False  # This shortcut is optional; never replace it by float equality.
    products=[]
    for h in (a,b):
        value=1
        for n,c in zip(h.support,h.counts): value*=n**int(c)
        products.append(value)
    return products[0]==products[1]


def _boundary_f2_ks(h):
    cumulative=0
    differences=[]
    for n,c in zip(h.support,h.counts):
        differences.append(abs(Fraction(h.N-cumulative,h.N)-Fraction(1,n**3)))
        cumulative+=int(c)
        differences.append(abs(Fraction(h.N-cumulative,h.N)-Fraction(1,(n+1)**3)))
    return max(differences)


def compare_refined_ks(model,observed,simulated):
    """Return a stable separated sign or a structurally proved exact tie."""
    if observed.support==simulated.support and (observed.counts==simulated.counts).all():
        return 0
    previous_sign=None
    for digits in (80,120,200,320):
        b0,d0,w0,gap0,width0=high_precision_fit_ks(model,observed,digits,True)
        b1,d1,w1,gap1,width1=high_precision_fit_ks(model,simulated,digits,True)
        both_boundary=b0==4 and b1==4
        if model==2 and both_boundary:
            x,y=_boundary_f2_ks(observed),_boundary_f2_ks(simulated)
            return (y>x)-(y<x)
        same_parameter=both_boundary or (model==1 and _equal_f1_parameter(observed,simulated))
        with mp.workdps(digits):
            delta=d1-d0
            scale=(1+max(abs(mp.log(n)) for h in (observed,simulated) for n in h.support))/min(b0-1,b1-1)
            margin=(mp.power(10,-digits+20)+width0+width1)*scale
            if same_parameter and observed.N==simulated.N and w0==w1 and min(gap0,gap1)>4*margin:
                return 0
            sign=1 if delta>margin else -1 if delta < -margin else None
        if sign is not None and sign==previous_sign:
            return sign
        previous_sign=sign
    raise ArithmeticError('KS comparison unresolved at 320 digits; no forced tie')

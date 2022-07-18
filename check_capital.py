def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)
def get_positive_part(x):
    return x**2
    # if x >= 0 : return x
    # else : return 0
def get_price(u,d,r,x0,s0,d0,d1_H,d1_T,d2_HH,d2_TT,d2_HT,d2_TH):
    p,q = get_pricing_measure(u,d,r)
    (x1_H,x1_T,x2_HH,x2_HT,x2_TH,x2_TT,x3_HHH,x3_HHT,
            x3_HTH,x3_HTT,x3_THH,x3_THT,x3_TTH,x3_TTT) = get_capital(u,d,r,x0,s0,d0,d1_H,d1_T,d2_HH,d2_TT,d2_HT,d2_TH)
    y0 = (1+r)**(-3)*(p*(p*(p*get_positive_part(x3_HHH)+
        q * get_positive_part(x3_HHT))+
        q * (p * get_positive_part(x3_HTH) + q * get_positive_part(x3_HTT)))+
    q * (p * (p * get_positive_part(x3_THH) + q * get_positive_part(x3_THT))
    + q * (p * get_positive_part(x3_TTH) + q * get_positive_part(x3_TTT))))
    return y0
def get_capital(u,d,r,x0,s0,d0,d1_H,d1_T,d2_HH,d2_TT,d2_HT,d2_TH):
    x1_H = d0 * (s0 * u) + (1+r) * (x0 - d0 *s0)
    x1_T = d0 * (s0 * d) + (1+r) * (x0 - d0 *s0)

    x2_HH = (1+r)*(x1_H - d1_H * (s0 * u)) + (s0 *u**2) * d1_H
    x2_HT = (1+r)*(x1_H - d1_H * (s0 *u)) + (s0*u*d) * d1_H
    x2_TH = (1+r)*(x1_T - d1_T * (s0 * d)) + (s0*u*d) * d1_T
    x2_TT = (1+r)*(x1_T- d1_T * (s0*d)) + (s0*d**2) * d1_T

    x3_HHH = (1+r)*(x2_HH - d2_HH * (s0*u**2)) + (s0*u**3) * d2_HH
    x3_HHT = (1+r)*(x2_HH - d2_HH * (s0*u**2)) + (s0*(u**2)*d) * d2_HH
    x3_HTH = (1+r)*(x2_HT - d2_HT * (s0*u*d)) + (s0*(u**2)*d) * d2_HT
    x3_HTT = (1+r)*(x2_HT - d2_HT * (s0*u*d)) + (s0*(d**2)*u) * d2_HT
    x3_THH = (1+r)*(x2_TH - d2_TH * (s0*u*d)) + (s0*(u**2)*d) * d2_TH
    x3_THT = (1+r)*(x2_TH - d2_TH * (s0*u*d)) + (s0*(d**2)*u) * d2_TH
    x3_TTH = (1+r)*(x2_TT - d2_TT * (s0*d**2)) + (s0*(d**2)*u) * d2_TT
    x3_TTT = (1+r)*(x2_TT - d2_TT * (s0*d**2)) + (s0*d**3) * d2_TT
    return (x1_H,x1_T,x2_HH,x2_HT,x2_TH,x2_TT,x3_HHH,x3_HHT,
            x3_HTH,x3_HTT,x3_THH,x3_THT,x3_TTH,x3_TTT)
print(get_price(2,0.6,0.25,5,10,1,1,1,1,1,1,1))
print(get_price(2,0.6,0.25,5,10,-1,-1,-1,-1,-1,-1,-1))
print(get_capital(2,0.6,0.25,5,10,-1,1,-1,-1,1,-1,-1))
print(get_pricing_measure(2,0.6,0.25))
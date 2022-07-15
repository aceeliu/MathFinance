#use Monte-Carlo algorithm to estimate V0 for high period models for sellers
#use Las-Vegas algorithm to find strategy for buyers 

#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
import random

from types import SimpleNamespace
cnt = SimpleNamespace(nn=0)

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    if p >= 1 or p <= 0 or q >= 1 or q <= 0:
        quit("Arbitrage")
    else:
        return (p,q)
def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_yk(u, d, r,Sk, Xk, k, n, comb, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    choice = random.choice([-1,1])
    comb.append(choice)
    Xk_H = (1 + r)*(Xk - Sk * choice) + u * Sk * choice
    Xk_T = (1 + r)*(Xk - Sk * choice) + d * Sk * choice
    if k < n:
        y1 = get_yk(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, cnt)
        y2 = get_yk(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, cnt)
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        return ret  
    else:
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return ret
        
def get_y0(u, d, r, s0, x0, k, n, comb): #implement formula of calculating y0
    comb = []
    y0 = (1+r) ** (-n) * get_yk(u, d, r, s0, x0, 1, n, comb, cnt)
    return y0,comb


def input_fn():
    print("input your u : ")
    u = float(input())
    print("input your d : ")
    d = float(input())
    print("input your r : ")
    r = float(input())
    print("input your s0 : ")
    s0 = float(input())
    print("input your x0 : ")
    x0 = float(input())
    print("input your n : ")
    n = int(input())
    return u,d,r,s0,x0,n

u,d,r,s0,x0,n = input_fn()

def mc(u,d,r,s0,x0,n): #calculate according to your input 
    maxx = 0
    avg_cnt = 0
    avg = 0
    for t in range (2**10):
       y0,comb = get_y0(u, d, r, s0, x0, 0, n, [])
       avg_cnt += 1
       avg += y0
       if (y0 > maxx):
           maxx = y0
           best_comb = comb
    result = avg/avg_cnt
    print("final best:", best_comb, maxx)
    print("average result:", result)
    return result

result = mc(u,d,r,s0,x0,n)

def lv(u,d,r,s0,x0,n):
    while True:
        y0,comb = get_y0(u, d, r, s0, x0, 0, n, [])
        if y0 > result:
            print("strategy:", comb)
            return comb

lv(u,d,r,s0,x0,n)

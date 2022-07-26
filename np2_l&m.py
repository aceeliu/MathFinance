#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
# import matplotlib.pyplot as plt
# import numpy as np
import copy
from types import SimpleNamespace
import random
import math
cnt = SimpleNamespace(nn=0)

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    if p >= 1 or p <= 0 or q >= 1 or q <= 0:
        #quit("Arbitrage")
        return (0, 0)
    if p >= q:
        #quit("p >= q")
        return (0, 0)
    else:
        return (p,q)

def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_yk(u, d, r, Sk, Xk, k, n, comb, i, l, m, cnt):  #return y
    p,q = get_pricing_measure(u,d,r)
    if (p == 0 and q == 0):
        return 0
    Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + (Sk + l) * comb[i][cnt.nn]
    Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + (Sk - m) * comb[i][cnt.nn]
    if k < n:
        cnt.nn += 1
        y1 = get_yk((Sk + 2*l)/(Sk + l), (Sk+l-m)/(Sk+l), r, Sk + l, Xk_H, (k + 1), n, comb, i, l, m, cnt)
        cnt.nn += 1
        y2 = get_yk((Sk+l-m)/(Sk-m), (Sk - 2*m)/(Sk-m), r, Sk - m, Xk_T, (k + 1), n, comb, i, l, m, cnt)
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        return ret  
    else:
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return ret
    
def get_y0(r, s0, x0, n, comb, i, l, m): #implement formula of calculating y0
    cnt.nn = 0
    y0 = (1+r) ** (-n) * get_yk((s0 + l)/s0, (s0 - m)/s0, r, s0, x0, 1, n, comb, i, l, m, cnt)
    return y0
    
def get_conjecture(u, d, r, Sk, Xk, k, n, l, m, conjecture):
    p,q = get_pricing_measure(u,d,r)
    if (p == 0 and q == 0):
        return (0, [])
    if ((Xk > 0 and Sk > 0) or (Xk < 0 and Sk < 0)):
        conjecture.append(1)
        Xk_H = (1 + r)*(Xk - Sk) + u * Sk
        Xk_T = (1 + r)*(Xk - Sk) + d * Sk
    else:
        conjecture.append(-1)
        Xk_H = (1 + r)*(Xk - Sk * (-1)) + u * Sk * (-1)
        Xk_T = (1 + r)*(Xk - Sk * (-1)) + d * Sk * (-1)
    if (k < n):
        (y1, conjecture) = get_conjecture((Sk + 2*l)/(Sk + l), (Sk+l-m)/(Sk+l), r, Sk + l, Xk_H, (k + 1), n, l, m, conjecture)
        if (y1 == 0 and conjecture == []) :
            return (0, [])
        (y2, conjecture) = get_conjecture((Sk+l-m)/(Sk-m), (Sk - 2*m)/(Sk-m), r, Sk - m, Xk_T, (k + 1), n, l, m, conjecture)
        if (y2 == 0 and conjecture == []) :
            return (0, [])
        ret = p * get_positive_part(y1) + q * get_positive_part(y2)
        return (ret, conjecture)
    else:
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return (ret, conjecture)

def combination(n, curr, comb, curr_perm):
    if (curr == n) :
        tmp = copy.copy(curr_perm)
        comb.append(tmp)
    else:
        curr_perm.append(1.0)
        combination(n, (curr + 1), comb, curr_perm)
        curr_perm.pop()
        curr_perm.append(-1.0)
        combination(n, (curr + 1), comb, curr_perm)
        curr_perm.pop()
        
def main(r, s0, x0, n, l, m): #calculate according to your input 
    # print("input your r : ")
    # r = float(input())
    # print("input your s0 : ")
    # s0 = float(input())
    # print("input your x0 : ")
    # x0 = float(input())
    # print("input your n : ")
    # n = int(input())
    # print("input your lambda : ")
    # l = float(input())
    # print("input your miu : ")
    # m = float(input())
    n -= 1
    comb = []
    curr_perm = []
    num_of_delta = 2**n-1
    combination(num_of_delta, 0, comb, curr_perm)
    maxx = 0 
    best_comb = []
    for i in range (2**num_of_delta):
        cnt.nn = 0
        ans = get_y0(r, s0, x0, n, comb, i, l, m)
        #print("y0 =",ans," with these deltas:",comb[i])
        if (ans > maxx):
            maxx = ans
            best_comb = comb[i]
            # print(best_comb, maxx)
    #print("final best:", best_comb, maxx)
    return (best_comb, maxx)
    
def counter(): 
    while(1) :
        r = random.uniform(0.1, 0.9)
        s0 = random.randint(2, 100)
        x0 = random.randint(0, 100)
        l = random.randint(1, s0-1)
        m = random.randint(1, s0-1)
        if (s0 % m != 0 and s0 > m * 4):
            n = random.randint(2, 4)
            u = (s0 + l)/s0
            d = (s0 - m)/s0
            p,q = get_pricing_measure(u, d, r)
            if (q > 0):
                #print("r =", r, "s0 =", s0, "x0 =", x0, "n =", n, "lambda =", l, "miu =", m)
                (positive_part_conj, conjecture) = get_conjecture(u, d, r, s0, x0, 1, n-1, l, m, [])
                if (positive_part_conj == 0 and conjecture == []) :
                    continue
                (best_comb, maxx) = main(r, s0, x0, n, l, m)
                positive_part_conj = positive_part_conj * (1+r) ** (-(n-1))
                approx = math.isclose(maxx, positive_part_conj, abs_tol = 0.001)
                if (not approx and maxx > positive_part_conj) :
                    return (r, s0, x0, l, m, n, best_comb, maxx, conjecture, positive_part_conj)
            
(r, s0, x0, l, m, n, best_comb, maxx, conjecture, positive_part_conj) = counter()
print("r =", r, "s0 =", s0, "x0 =", x0, "lambda =", l, "miu =", m, "n =", n)
print("best_comb", best_comb, maxx)
print("conjecture", conjecture, positive_part_conj)
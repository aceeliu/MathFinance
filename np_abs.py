#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
#import matplotlib.pyplot as plt
#import numpy as np
import copy
import random
import math

from types import SimpleNamespace
cnt = SimpleNamespace(nn=0)

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    if p >= 1 or p <= 0 or q >= 1 or q <= 0:
        quit("Arbitrage")
    else:
        return (p,q)

def abs(x):
    if x > 0:
        return x
    else:
        return -x
def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_conjecture(u, d, r, Sk, Xk, k, n, conjecture):
    p,q = get_pricing_measure(u,d,r)
    if Xk > 0:
        conjecture.append(-1)
        Xk_H = (1 + r)*(Xk - Sk * (-1)) + u * Sk * (-1)
        Xk_T = (1 + r)*(Xk - Sk * (-1)) + d * Sk * (-1)
    else:
        conjecture.append(1)
        Xk_H = (1 + r)*(Xk - Sk) + u * Sk
        Xk_T = (1 + r)*(Xk - Sk) + d * Sk
    if (k < n):
        (y11, y12, conjecture) = get_conjecture(u, d, r, Sk*u, Xk_H, (k + 1), n, conjecture)
        (y21, y22, conjecture) = get_conjecture(u, d, r, Sk*d, Xk_T, (k + 1), n, conjecture)
        ret1 = p * y11 + q * y21
        ret2 = p * y21 + q * y22
        return (ret1, ret2, conjecture)
    else:
        ret1 = (p * abs(Xk_H) + q * abs(Xk_T))
        ret2 = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return (ret1, ret2, conjecture)
        
def get_yk(u, d, r, Sk, Xk, k, n, comb, i, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + u * Sk * comb[i][cnt.nn]
    Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + d * Sk * comb[i][cnt.nn]
    if k < n:
        cnt.nn += 1
        (y11, y12) = get_yk(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, i, cnt)
        cnt.nn += 1
        (y21, y22) = get_yk(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, i, cnt)
        # print("k = ", k, "y1 = ", y1, "y2 = ", y2)
        ret1 = p * y11 + q * y21
        ret2 = p * y21 + q * y22
        # print("y1=", y1, "y2=", y2, "ret=", ret, "k=", k, "p=", p, "q=", q)
        return (ret1, ret2)
    else:
        ret1 = (p * abs(Xk_H) + q * abs(Xk_T))
        ret2 = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        # print("Xk_H=", Xk_H, "Xk_T", Xk_T, "ret=", ret, "k=", k)
        return (ret1, ret2)
        
def get_y0(u, d, r, s0, x0, n, comb, id): #implement formula of calculating y0
    (y01, y02) = get_yk(u, d, r, s0, x0, 1, n, comb, id, cnt)
    y01 = y01 * (1+r) ** (-n)
    y02 = y02 * (1+r) ** (-n)
    #print(comb[i])
    return (y01, y02)
    
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

def main(u, d, r, s0, x0): #calculate according to your input 
    # print("input your u : ")
    # u = float(input())
    # print("input your d : ")
    # d = float(input())
    # print("input your r : ")
    # r = float(input())
    # print("input your s0 : ")
    # s0 = float(input())
    # print("input your x0 : ")
    # x0 = float(input())
    # print("input your n : ")
    # n = int(input())
    n = 4
    comb = []
    curr_perm = []
    num_of_delta = 2**n-1
    combination(num_of_delta, 0, comb, curr_perm)
    max1 = 0
    max2 = 0
    best_comb = []
    for i in range (2**num_of_delta):
        cnt.nn = 0
        (ans1, ans2) = get_y0(u, d, r, s0, x0, n, comb, i)
        # print("abs(y0)=",ans1,"positive part(y0)", ans2, "with these deltas:",comb[i])
        # if (ans1 > max1 or ans2 > max2):
        #     max1 = ans1
        #     max2 = ans2
        #     best_comb = comb[i]
        #     # print(best_comb, maxx)
        if (ans2 > max2) :
            max1 = ans1
            max2 = ans2
            best_comb = comb[i]
    # print("final best:", best_comb, max1, max2)
    (abs_conj, positive_part_conj, conjecture) = get_conjecture(u, d, r, s0, x0, 1, n, [])
    abs_conj = abs_conj * (1+r) ** (-n)
    positive_part_conj = positive_part_conj * (1+r) ** (-n)
    # print("conjecture", conjecture, abs_conj, positive_part_conj)
    return (best_comb, max1, max2, conjecture, abs_conj, positive_part_conj)

def counter(): 
    while(1) :
        r = random.uniform(0.1, 0.9)
        u = random.uniform(1 + r, 5)
        d = random.uniform(0.1, 0.9)
        s0 = random.uniform(1, 100)
        x0 = random.uniform(-1000, 1000)
        p,q = get_pricing_measure(u, d, r)
        if (p < q) :
            print("u=", u, "d=", d, "r=", r, "s0=", s0, "x0=", x0)
            (best_comb, max1, max2, conjecture, abs_conj, positive_part_conj) = main(u, d, r, s0, x0)
            approx = math.isclose(max2, positive_part_conj, abs_tol = 0.001)
            if (not approx and max2 > positive_part_conj) :
                return (u, d, r, s0, x0, best_comb, max1, max2, conjecture, abs_conj, positive_part_conj)
            
(u, d, r, s0, x0, best_comb, max1, max2, conjecture, abs_conj, positive_part_conj) = counter()
print("u=", u, "d=", d, "r=", r, "s0=", s0, "x0=", x0)
print("best_comb", best_comb, max2)
print("conjecture", conjecture, positive_part_conj)

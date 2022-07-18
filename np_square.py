#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
#import matplotlib.pyplot as plt
#import numpy as np
import copy

from types import SimpleNamespace
cnt = SimpleNamespace(nn=0)

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)

def square(x):
    return x**2

def get_yk(u, d, r, Sk, Xk, k, n, comb, i, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + u * Sk * comb[i][cnt.nn]
    Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + d * Sk * comb[i][cnt.nn]
    if k < n:
        cnt.nn += 1
        y1 = get_yk(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, i, cnt)
        cnt.nn += 1
        y2 = get_yk(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, i, cnt)
        # print("k = ", k, "y1 = ", y1, "y2 = ", y2)
        ret = p * y1 + q * y2
        print(y1, y2, ret, k)
        return ret  
    else:
        ret = (p * square(Xk_H) + q * square(Xk_T))
        print(Xk_H, Xk_T, ret, k)
        return ret
        
def get_y0(u, d, r, s0, x0, k, n, comb, id): #implement formula of calculating y0
    y0 = (1+r) ** (-n) * get_yk(u, d, r, s0, x0, 1, n, comb, id, cnt)
    #print(comb[i])
    return y0
    
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

def main(): #calculate according to your input 
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
    comb = []
    curr_perm = []
    num_of_delta = 2**n-1
    combination(num_of_delta, 0, comb, curr_perm)
    maxx = 0 
    best_comb = []
    for i in range (2**num_of_delta):
        cnt.nn = 0
        ans = get_y0(u, d, r, s0, x0, 0, n, comb, i)
        print("y0=",ans," with these deltas:",comb[i])
        if (ans > maxx):
            maxx = ans
            best_comb = comb[i]
            # print(best_comb, maxx)
    print("final best:", best_comb, maxx)
    
main()

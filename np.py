#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
import matplotlib.pyplot as plt
import numpy as np
import copy

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)

def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_yk(u, d, r,Sk, Xk, k, n, comb, i, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    if (k == n) :
        Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt]) + u*Sk
        cnt += 1
        Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt + 1]) + d*Sk
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        #print(i, k, ret)
        return ret
    else :
        #print(i,k)
        Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt]) + u*Sk
        Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt + 1]) + d*Sk
        y1 = get_yk(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, i, (cnt + 2))
        y2 = get_yk(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, i, (cnt + 2))
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        #print(i, k, ret)
        return ret
        
    
def get_y0(u, d, r, s0, x0, k, n, comb, id): #implement formula of calculating y0
    y0 = (1+r) ** (-n) * get_yk(u, d, r, s0, x0, 0, n, comb, id, 0)
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
    # f = open("2period.txt", "r") 
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
    num_of_delta = 2**(n+1)-1
    combination(num_of_delta, 0, comb, curr_perm)
    maxx = 0 
    best_comb = []
    for i in range (2**num_of_delta):
        ans = get_y0(u, d, r, s0, x0, 0, n, comb, i)
        if (ans > maxx):
            maxx = ans
            best_comb = comb[i]
            # print(best_comb, maxx)
    print("final best:", best_comb, maxx)
    
main()

#test with 2 period
#comb = []
#curr_perm = []
#combination(7, 0, comb, curr_perm)
#maxx = 0 
#best_comb = []
#for i in range (2**7):
#   ans = get_y0(2.0, 0.5, 0.25, 8, 0, 0, 2, comb, i)
#   if (ans > maxx):
#       maxx = ans
#       best_comb = comb[i]
#       print(best_comb, maxx)
#print("final best", best_comb, maxx)
#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
import matplotlib.pyplot as plt
import numpy as np
import copy


from types import SimpleNamespace
cnt = SimpleNamespace(n=0)
print(cnt)
print(cnt.n)

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)

def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_yk(u, d, r, Sk, Xk, k, n, comb, i, l, cnt):  #return y
    p,q = get_pricing_measure(u,d,r)
    Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt]) + (Sk + l) * comb[i][cnt.n]
    #print("k=",k, " n=",n, "cnt=", cnt)
    if (k == 0) :
        Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt]) + (Sk - l) * comb[i][cnt.n]
    else :
        Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt + 1]) + (Sk - l) * comb[i][cnt.n + 1]
    if k == n - 1 :
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return ret
    else:
        if (k == 0) : 
            cnt.n+=1
        else: 
            cnt.n+=2
        y1 = get_yk((Sk + l)/Sk, (Sk - l)/Sk, r, Sk + l, Xk_H, (k + 1), n, comb, i, l, cnt)
        y2 = get_yk((Sk + l)/Sk, (Sk - l)/Sk, r, Sk - l, Xk_T, (k + 1), n, comb, i, l, cnt)
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        return ret    
    
def get_y0(u, d, r, s0, x0, k, n, comb, id, l): #implement formula of calculating y0
    y0 = (1+r) ** (-n) * get_yk((s0 + l)/s0, (s0 - l)/s0, r, s0, x0, 0, n, comb, id, l, 0)
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
    print("input your lambda : ")
    l = float(input())
    comb = []
    curr_perm = []
    num_of_delta = 2**n-1
    #print("num_of_delta",num_of_delta)
    combination(num_of_delta, 0, comb, curr_perm)
    #print(comb)
    maxx = 0 
    best_comb = []
    for i in range (2**num_of_delta):
        ans = get_y0(u, d, r, s0, x0, 0, n, comb, l, cnt)
        print("y0=",ans," with these deltas:",comb[i])
        if (ans > maxx):
            maxx = ans
            best_comb = comb[i]
            # print(best_comb, maxx)
    print("final best:", best_comb, maxx)
    
main()

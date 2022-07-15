#can estimate the accuracy of the randomize algorithm by comparing 
#values up to 4 period 

import random
import copy
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

def get_yk_rand(u, d, r,Sk, Xk, k, n, comb, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    choice = random.choice([-1,1])
    comb.append(choice)
    Xk_H = (1 + r)*(Xk - Sk * choice) + u * Sk * choice
    Xk_T = (1 + r)*(Xk - Sk * choice) + d * Sk * choice
    if k < n:
        y1 = get_yk_rand(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, cnt)
        y2 = get_yk_rand(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, cnt)
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        return ret  
    else:
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return ret
        
def get_y0_rand(u, d, r, s0, x0, k, n, comb): #implement formula of calculating y0
    comb = []
    y0 = (1+r) ** (-n) * get_yk_rand(u, d, r, s0, x0, 1, n, comb, cnt)
    return y0,comb

def get_yk_np(u, d, r,Sk, Xk, k, n, comb, i, cnt) : #return y
    p,q = get_pricing_measure(u,d,r)
    # p,q = 0.5, 0.5
    Xk_H = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + u * Sk * comb[i][cnt.nn]
    Xk_T = (1 + r)*(Xk - Sk * comb[i][cnt.nn]) + d * Sk * comb[i][cnt.nn]
    if k < n:
        cnt.nn += 1
        y1 = get_yk_np(u, d, r, Sk*u, Xk_H, (k + 1), n, comb, i, cnt)
        cnt.nn += 1
        y2 = get_yk_np(u, d, r, Sk*d, Xk_T, (k + 1), n, comb, i, cnt)
        # print("k = ", k, "y1 = ", y1, "y2 = ", y2)
        ret = (p * get_positive_part(y1) + q * get_positive_part(y2))
        return ret  
    else:
        ret = (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
        return ret
        
def get_y0_np(u, d, r, s0, x0, k, n, comb, id): #implement formula of calculating y0
    y0 = (1+r) ** (-n) * get_yk_np(u, d, r, s0, x0, 1, n, comb, id, cnt)
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

def main_rand(u,d,r,s0,x0,n): #calculate according to your input 
    maxx = 0
    avg_cnt = 0
    avg = 0
    for t in range (2**10*10):
       y0,comb = get_y0_rand(u, d, r, s0, x0, 0, n, [])
       avg_cnt += 1
       avg += y0
       if (y0 > maxx):
           maxx = y0
           best_comb = comb
    result = avg/avg_cnt
    # print("final best:", best_comb, maxx)
    # print("average result:", result)
    return result

def main_np(u,d,r,s0,x0,n): #calculate according to your input
    comb = []
    curr_perm = []
    num_of_delta = 2**n-1
    combination(num_of_delta, 0, comb, curr_perm)
    maxx = 0 
    best_comb = []
    avg_cnt = 0
    avg = 0
    # num of period < 5
    for i in range (2**num_of_delta):
            cnt.nn = 0
            ans = get_y0_np(u, d, r, s0, x0, 0, n, comb, i)
            avg += ans
            avg_cnt += 1
            # print("y0=",ans," with these deltas:",comb[i])
            if (ans > maxx):
                maxx = ans
                best_comb = comb[i]
    # print("final best:", best_comb, maxx)
    return (avg/avg_cnt)

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

print("comment out line 132-137 when try to input n>=5")

u,d,r,s0,x0,n = input_fn()

result = main_rand(u,d,r,s0,x0,n)
ideal = main_np(u,d,r,s0,x0,n)
diff = abs(result - ideal) / ideal 

print(result,ideal)
print("Compare estimation with calculation--" )
print("difference in percentage:",diff*100)

result2 = main_rand(u,d,r,s0,x0,n)
diff2 = abs(result - result2) / result2
print(result,result2)
print("Compare estimation with different sets of samples--" )
print("difference in percentage:",diff2*100)

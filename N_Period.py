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

p,q = get_pricing_measure(u,d,r)
def get_yk(Sk, Xk, k, n, comb, id) : #return y
    if (k == n) :
        Xk_H = (1 + r)(Xk - Sk * comb[id][k]) + u*Sk
        Xk_T = (1 + r)(Xk - Sk * comb[id][k]) + d*Sk
        return (p * get_positive_part(Xk_H) + q * get_positive_part(Xk_T))
    else :
        Xk_H = (1 + r)(Xk - Sk * comb[id][k]) + u*Sk
        Xk_T = (1 + r)(Xk - Sk * comb[id][k]) + d*Sk
        y1 = get_yk(Sk*u, Xk_H, (k + 1), n)
        y2 = get_yk(Sk*d, Xk_T, (k + 1), n)
        return (p * get_positive_part(y1) + q * get_positive_part(y2))
        
    
def get_y0(s0, x0, k, n, comb, id): #implement formula of calculating y0
    y0 = (1+r) ** (-n) * get_yk(s0, x0, n, 0, comb)
    
def combination(n, curr, comb, curr_perm):
    if (curr == n) :
        tmp = copy.copy(curr_perm)
        comb.append(tmp)
    else:
        curr_perm.append(1)
        combination(n, (curr + 1), comb, curr_perm)
        curr_perm.pop()
        curr_perm.append(-1)
        combination(n, (curr + 1), comb, curr_perm)
        curr_perm.pop()
    
def main(): #calculate according to your input 
    # f = open("2period.txt", "r") 
    #combination_1(2, 0.5, 0.25, 8, 8)
    #combination_1(1.3, 0.94, 0.06, 8, 2)
    comb = []
    curr_perm = []
    combination(10, 0, comb, curr_perm)
    print(comb)
    for i in range(2 ** n)
        get_y0(, i)
#   y = np.zeros((101,8))
#   ystd = np.zeros(101)
#   for i in range(0, 100) :
#       y[i] = combination_2(1.3, 0.94, 0.06, 8, (i-50.0)*0.2)
#       ystd[i] = np.std(y[i])
#   x = np.arange(-10, 10.1, 0.2)
#   plt.plot(x, ystd)
#   plt.show()
    
#   print("input your u : ")
#   u = float(input())
#   print("input your d : ")
#   d = float(input())
#   print("input your r : ")
#   r = float(input())
#   print("input your s0 : ")
#   s0 = float(input())
#   print("input your x0 : ")
#   x0 = float(input())
#   print("input your ∆0 : ")
#   d0 = float(input())
#   print("input your ∆1(H) : ")
#   d_H = float(input())
#   print("input your ∆1(T) : ")
#   d_T = float(input())

main()
    
    
   
    
    



    
    
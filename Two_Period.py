#let d0 denotes ∆0, d_H denotes ∆1(H), d_T denotes ∆1(T)
import matplotlib.pyplot as plt
import numpy as np
#plt.plot([1, 2, 3, 4])
#plt.ylabel('some numbers')
#plt.show()
def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)


def get_positive_part(x):
    if x >= 0 : return x
    else : return 0

def get_y0(u,d,r,s0,x0,d0,d_H,d_T): #implement formula of calculating y0
    p,q = get_pricing_measure(u,d,r)

    bank_H = (1+r) * (u * s0 * (d0 - d_H) + (1+r) * (x0 - s0*d0))
    bank_T = (1+r) * (d * s0 * (d0 - d_T) + (1+r) * (x0 - s0*d0))
    x_HH = p * (u ** 2 * s0 * d_H + bank_H)
    x_HT = q * (u * d * s0 * d_H  + bank_H)
    x_TH = p * (u * d * s0 * d_T  + bank_T)
    x_TT = q * (d ** 2 * s0 * d_T  + bank_T)

    y0 = (1+r) ** (-2) * (p * (get_positive_part(x_HH) + get_positive_part(x_HT))
    + q * (get_positive_part(x_TH) + get_positive_part(x_TT)))
    # print("y0 is",y0)
    return y0

def combination_1(u, d, r, s0, x0): #calculate 8 cases of ∆0, ∆1(H), ∆1(T) varies between 1 , -1
    print(get_y0(u,d,r,s0,x0,1,1,1))
    print(get_y0(u,d,r,s0,x0,1,1,-1))
    print(get_y0(u,d,r,s0,x0,1,-1,1))
    print(get_y0(u,d,r,s0,x0,-1,1,1))
    print(get_y0(u,d,r,s0,x0,1,-1,-1))
    print(get_y0(u,d,r,s0,x0,-1,1,-1))
    print(get_y0(u,d,r,s0,x0,-1,-1,1))
    print(get_y0(u,d,r,s0,x0,-1,-1,-1))

def combination_2(u, d, r, s0, x0):
    return [
        get_y0(u,d,r,s0,x0,1,1,1), 
        get_y0(u,d,r,s0,x0,1,1,-1),
        get_y0(u,d,r,s0,x0,1,-1,1),
        get_y0(u,d,r,s0,x0,-1,1,1),
        get_y0(u,d,r,s0,x0,1,-1,-1),
        get_y0(u,d,r,s0,x0,-1,1,-1),
        get_y0(u,d,r,s0,x0,-1,-1,1),
        get_y0(u,d,r,s0,x0,-1,-1,-1)
    ]
def main(): #calculate according to your input 
    # f = open("2period.txt", "r") 
    #combination_1(2, 0.5, 0.25, 8, 8)
    #combination_1(1.3, 0.94, 0.06, 8, 2)
    y = np.zeros((101,8))
    ystd = np.zeros(101)
    for i in range(0, 100) :
        y[i] = combination_2(1.3, 0.94, 0.06, 8, (i-50.0)*0.2)
        ystd[i] = np.std(y[i])
    x = np.arange(-10, 10.1, 0.2)
    plt.plot(x, ystd)
    plt.show()
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
#   get_y0(u,d,r,s0,x0,d0,d_H,d_T)

    #check 1, 1, 1,...
    #special u*d = 1
    #may not need all paths
    #what is always strategy when (p < q) ^ (p == q) ^ (p > q)
    #limit in binomial model 

main()
    
    
   
    
    



    
    
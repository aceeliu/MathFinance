import copy

def get_pricing_measure(u,d,r):
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    return (p,q)

def get_positive_part(x):
    if (x <= 0): return 0
    else: return x

def combination(len, cur, comb, curr_perm):
    if (cur == len) :
        tmp = copy.copy(curr_perm)
        comb.append(tmp)
    else:
        curr_perm.append(1.0)
        combination(len, (cur + 1), comb, curr_perm)
        curr_perm.pop()
        curr_perm.append(-1.0)
        combination(len, (cur + 1), comb, curr_perm)
        curr_perm.pop()

def get_priceL(delta, u, d, r, num_period, cur_period, xn, sn, priceL):
    X_H = (1 + r)*(xn - delta[0]*sn) + delta[0] * u * sn
    X_T = (1 + r)*(xn - delta[0]*sn) + delta[0] * d * sn
    delta.pop(0)
    if (num_period - 1 == cur_period):
        priceL.append(X_H)
        priceL.append(X_T)
        return
    else:
        # print("before head case {}".format(delta))
        get_priceL(delta, u, d, r, num_period, cur_period+1, X_H, u*sn, priceL)
        # print("after {}".format(delta))
        # print("{}".format(priceL))
        # print(X_T, cur_period)
        # print(X_T, cur_period)
        get_priceL(delta, u, d, r, num_period, cur_period+1, X_T, d*sn, priceL)
        # print("One Case End ---------------------------------------------------")

def get_price(priceL, p, q):
    # print(priceL)
    if (len(priceL) == 1):
        # print(priceL[0])
        return priceL[0]
    newL = []
    for i in range(0, len(priceL), 2):
        X_H = p * (priceL[i])
        X_T = q * (priceL[i+1])
        newL.append(X_H + X_T)
    return get_price(newL, p, q)

def main():
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
    # print(comb)
    max = 0 
    best_comb = []
    comb_ = copy.deepcopy(comb)
    for i in range (len(comb)):
        new_price = []
        # print(comb[i])
        priceL = []
        get_priceL(comb[i], u, d, r, n, 0, x0, s0, priceL)
        p, q = get_pricing_measure(u,d,r)
        print(priceL)
        for elem in priceL:
            new_price.append(get_positive_part(elem))
        #     # print(new_price)
        ans = get_price(new_price, p, q) * ((1+r)**(-n))
        # print(ans)
        print("y0=",ans," with these deltas:",comb_[i])
    if (ans > max):
        max = ans
        best_comb = comb_[i]
            # print(best_comb, maxx)
    print("final best:", best_comb, max)
    
main()
import matplotlib.pyplot as plt
import numpy as np

def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def printaList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    print(f'X1_H'.center(fieldWidth+1), end='  ')
    print(f'X1_T'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'Δ0={-1+row*0.5}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()

def printx0List(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    print(f'X1_H'.center(fieldWidth+1), end='  ')
    print(f'X1_T'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'x0={0+row*0.5}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()

def get_pricing_measure(u,d,r):
    L = [0,0]
    p = (1+r-d)/(u-d)
    q = (u-1-r)/(u-d)
    L[0] = p
    L[1] = q
    return L

def one_time_binomial(S0, u, d, r, x0, a): #N=1
    #given initial capital x0
    #buy a shares of stock at time 1
    S1_H = S0 * u
    S1_T = S0 * d
    bank0 = x0 - S0 * a
    X1_H = S1_H * a + bank0 * (1+r)
    X1_T = S1_T * a + bank0 * (1+r)
    #print when #a remains unchanged and #x0 remains unchanged
    return ([X1_H, X1_T])

def build_a_list(S0, u, d, r, x0):
    print("S0=",S0, "u=",u, "d=",d, "r=",r, "x0=",x0)
    print("p,q",get_pricing_measure(u,d,r))
    #take in x0, vary a
    result = []
    a = -1
    while (a <= 1):
        result.append(one_time_binomial(S0, u, d, r, x0, a))
        a += 0.5
    return result

def build_x0_list(S0, u, d, r, a):
    print("S0=",S0, "u=",u, "d=",d, "r=",r, "Δ0=",a)
    print("p,q",get_pricing_measure(u,d,r))
    #take in x0, vary a
    result = []
    x0 = 0
    while (x0 <= 2 * S0):
        result.append(one_time_binomial(S0, u, d, r, x0, a))
        x0 += 1
    return result
  
print("vary in Δ0")
printaList(build_a_list(8, 4, 0.5, 0.5, 0))

print("vary in x0")
# printx0List(build_x0_list(8, 4, 0.5, 0.5, 1))
# printx0List(build_x0_list(8, 4, 0.5, 0.5, -1))
# printx0List(build_x0_list(8, 2.5, 0.5, 0.5, 1)) #p=q
# printx0List(build_x0_list(8, 2.5, 0.5, 0.5, -1)) #p=q
# printx0List(build_x0_list(8, 2, 0.4, 0.2, 1)) #p=q
# printx0List(build_x0_list(8, 2, 0.4, 0.2, -1)) #p=q
# printx0List(build_x0_list(10, 2.5, 0.5, 0.5, 1)) #p=q
# printx0List(buil[]pod_x0_list(10, 2.5, 0.5, 0.5, -1)) #p=q
# printx0List(build_x0_list(8, 2, 0.5, 0.5, 1)) #p=q
# printx0List(build_x0_list(8, 2, 0.5, 0.5, -1)) #p=q
def main():
    print("input your u : ")
    u = input()
    print("input your d : ")
    d = input()
    print("input your r : ")
    r = input()
    print("input your s0 : ")
    s0 = input()
    print("Vary Δ0 or initial capital: (enter stock or x))")
    choice = input()
    if (choice == "stock"):
        print("input your x0")
        x0 = input()
        printaList(build_a_list(s0, u, d, r, x0))
    if (choice == "x"):
        print("input your Δ0")
        a = input()
        printaList(build_x0_list(s0, u, d, r, a))

   

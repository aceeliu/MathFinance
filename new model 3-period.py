
def get_pricing_measure(l,s0,r):
    p = (l + s0 * r)/(2 * l)
    q = 1 - p
    return (p,q)

def get_positive_part(x):
    if x >= 0 : return x
    else : return 0
    
def get_square_part(x):
    return x**2

def get_y0(x0,d,d1_H,d1_T,d2_HH,d2_TT,d2_HT,d2_TH,l,s0,r):
    x1_H = d * (s0 + l) + (1+r) * (x0 - d *s0)
    x1_T = d * (s0 - l) + (1+r) * (x0 - d *s0)

    x2_HH = (1+r)*(x1_H - d1_H * (s0 + l)) + (s0 + 2*l) * d1_H
    x2_HT = (1+r)*(x1_H - d1_H * (s0 + l)) + (s0) * d1_H
    x2_TH = (1+r)*(x1_T - d1_T * (s0 - l)) + (s0) * d1_T
    x2_TT = (1+r)*(x1_T- d1_T * (s0 - l)) + (s0-2*l) * d1_T

    x3_HHH = (1+r)*(x2_HH - d2_HH * (s0 + 2*l)) + (s0 + 3*l) * d2_HH
    x3_HHT = (1+r)*(x2_HH - d2_HH * (s0 + 2*l)) + (s0 + l) * d2_HH
    x3_HTH = (1+r)*(x2_HT - d2_HT * (s0)) + (s0 + l) * d2_HT
    x3_HTT = (1+r)*(x2_HT - d2_HT * (s0)) + (s0 - l) * d2_HT
    x3_THH = (1+r)*(x2_TH - d2_TH * (s0)) + (s0 + l) * d2_TH
    x3_THT = (1+r)*(x2_TH - d2_TH * (s0)) + (s0 - l) * d2_TH
    x3_TTH = (1+r)*(x2_TT - d2_TT * (s0-2*l)) + (s0 - l) * d2_TT
    x3_TTT = (1+r)*(x2_TT - d2_TT * (s0-2*l)) + (s0 - 3*l) * d2_TT
    p1,q1 = get_pricing_measure(l,s0,r)
    p2_H,q2_H = get_pricing_measure(l,s0+l,r)
    p2_T,q2_T = get_pricing_measure(l,s0-l,r)
    p3_HH,q3_HH = get_pricing_measure(l,s0+2*l,r)
    p3_HT,q3_HT = get_pricing_measure(l,s0,r)
    p3_TH,q3_TH = get_pricing_measure(l,s0,r)
    p3_TT,q3_TT = get_pricing_measure(l,s0-2*l,r)
    y0 = (1+r)**(-3)*(p1*(p2_H*(p3_HH*get_positive_part(x3_HHH)+
        q3_HH * get_positive_part(x3_HHT))+
        q2_H * (p3_HT * get_positive_part(x3_HTH) + q3_HT * get_positive_part(x3_HTT)))+
    q1 * (p2_T * (p3_TH * get_positive_part(x3_THH) + q3_TH * get_positive_part(x3_THT))
    + q2_T * (p3_TT * get_positive_part(x3_TTH) + q3_TT * get_positive_part(x3_TTT))))
    # return (x3_HHH,x3_HHT,x3_HTH,x3_HTT,x3_THH,x3_THT,x3_TTH,x3_TTT,y0)
    y1 = (1+r)**(-3)*(p1*(p2_H*(p3_HH*get_square_part(x3_HHH)+
        q3_HH * get_square_part(x3_HHT))+
        q2_H * (p3_HT * get_square_part(x3_HTH) + q3_HT * get_square_part(x3_HTT)))+
    q1 * (p2_T * (p3_TH * get_square_part(x3_THH) + q3_TH * get_square_part(x3_THT))
    + q2_T * (p3_TT * get_square_part(x3_TTH) + q3_TT * get_square_part(x3_TTT))))
    return (y0,y1)
def main():
  print("input your x0 : ")
  x0 = float(input())
  print("input your l : ")
  l = float(input())
  print("input your r : ")
  r = float(input())
  print("input your s0 : ")
  s0 = float(input())
  y0,y1 = get_y0(x0,1,1,1,1,1,1,1,l,s0,r)
  p0,q0 = get_pricing_measure(l,s0,r)
  print("p0 is", p0)
  print("q0 is", q0)
  print("Y0 is", y0)
  print("Y1 is", y1)
main()

    
    
   
    
    



    
    
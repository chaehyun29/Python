 
a= 10
b =30 

def swap(a, b):
    temp = a
    a= b
    b= temp
    print(f"바뀐후의 값은 {a},{b}입니다.")


swap(a,b)
print(f"현재 값은 {a},{b}입니다.")

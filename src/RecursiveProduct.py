def product(First, Second, Count = 0, num = 0):
    if Count == First:
        return num
    else:
        Count += 1
        num += Second 
        return product(First, Second, Count, num)
    

a = 20 
b = 5 
print(product(a,b))
    
    
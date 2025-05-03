def sumList(List:list[int], ind = 0, count= 0 )->int: 
     if ind == len(List):
          return count
     else:
        count += List[ind]
        ind +=1
     return sumList(List, ind, count)

lista1 = [1,2,4,6,7,9,0,10]

print(sumList(lista1))
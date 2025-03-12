def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def RecursivePermutations(Word: str, Count: int = 0, List = []):
    if Count == factorial(len(Word)):
        return List
    else: 
        NewList = list(Word)
        FirstElement = NewList[0]
        NewList.pop(0)
        NewList.append(FirstElement)
        NewWord = ''.join(NewList)
        List.append(NewWord)
        return RecursivePermutations(NewWord, Count + 1, List)
    

word = "juan"
permutations = RecursivePermutations(word)
print(permutations)
def IsPalindromo(Word:str, count = -1, reversedWord = "" )->bool: 
    
    if len(Word) == (count*-1)-1:
        return Word == reversedWord
    else:
        reversedWord += Word[count]
        count -=1
        return IsPalindromo(Word, count, reversedWord )


Palabra1 = "radar"

print(IsPalindromo(Palabra1))
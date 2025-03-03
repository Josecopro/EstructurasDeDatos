def HowMuchVocals(s):
    def helper(s, index):
        if index == len(s):
            return 0
        if s[index] in "aeiouAEIOU":
            return 1 + helper(s, index + 1)
        return helper(s, index + 1)
    
    return helper(s, 0)

print(HowMuchVocals("aeiouAEIOU")) # 10

print(HowMuchVocals("aeiouAEIOUaeiouAEIOU")) # 20

print(HowMuchVocals("hola")) # 2
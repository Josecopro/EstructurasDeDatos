def delrepetivechars(s):
    def helper(s, index):
        if index == len(s) - 1:
            return s[index]
        if s[index] == s[index + 1]:
            return helper(s, index + 1)
        else:
            return s[index] + helper(s, index + 1)
    
    if len(s) == 0:
        return s
    return helper(s, 0)

print(delrepetivechars("aaabbbccc"))
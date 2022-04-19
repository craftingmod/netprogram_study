lst = ["H", "e", "l", "l", "o", " ", "I", "a", "T"]

# A
lst[7] = "o"
print(lst)

# B
lst.append("?")
print(lst)

# C
print(len(lst))

# D
print("".join(lst))

# E
lst.sort(reverse=True)
print(lst)
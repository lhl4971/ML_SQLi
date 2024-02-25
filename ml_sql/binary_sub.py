from typing import Literal

# Define an auxiliary function for binary search in the list
def binary_search(list, target):
    left = 0
    right = len(list) - 1
    while left <= right:
        mid = (left + right) // 2
        if list[mid] == target:
            return True
        elif list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

def binary_sub(str, list, type:Literal['keywords','functions'] = 'functions'): 
    # Initialize an empty string to store the results
    result = ""
    # Initialize a pointer for traversing str
    i = 0
    # Initialize a variable to record the length of the longest item in the list
    max_len = 0
    # Iterate through each element in the list and find the length of the longest item
    for item in list:
        # If the length of the element is greater than the length of the longest item, update the length of the longest item
        if len(item) > max_len:
            max_len = len(item)
    # When the pointer does not exceed the length of str, continue looping
    while i < len(str):
        # Initialize a variable to record the length of the longest match
        longest = 0
        # Iterate through each substring in str starting from the pointer, but not exceeding the length of the longest item
        for j in range(i + 1, min(i + max_len + 1, len(str) + 1)):
            # Get the current substring
            substring = str[i:j].upper()
            # If the substring exists in the list and its length is greater than the length of the longest match, update the length of the longest match.
            if binary_search(list, substring) and len(substring) > longest and str[i-1] == ' ' and str[j] == ' ':
                longest = len(substring)
        # If the length of the longest match is greater than 0, a match is found, replace it with uppercase, and update the pointer
        if longest > 0:
            if type == "functions":
                result += ' F_' + str[i:i + longest].upper() + ' '
            else:
                result += ' ' + str[i:i + longest].upper() + ' '
            i += longest
        # Otherwise, retain the original character and update the pointer
        else:
            result += str[i]
        i += 1
    # Return the modified string
    return result
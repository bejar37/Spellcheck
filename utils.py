
def is_vowel(char):
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        if char in vowels:
                return True

        return False

def change_case(char):
        if char.islower():
                char = char.capitalize()
        elif char.isalpha():
                char = char.lower()
        return char

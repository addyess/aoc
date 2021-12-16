from itertools import permutations

with open("day4.txt") as fin:
    ins = fin.read()


def no_repeat(phrase):
    words = phrase.split(" ")
    unique = list(set(words))
    return len(unique) == len(words)


def no_anagrams(phrase):
    words = phrase.split(" ")
    unique = set(words)
    for word in unique:
        for p in permutations(word):
            anagram = "".join(p)
            if anagram != word and anagram in unique:
                return False
    return True


phrases = ins.splitlines()
valid_phrase = [_ for _ in phrases if no_repeat(_)]
print(f"Result 1: {len(valid_phrase)}")

valid_phrase = [_ for _ in phrases if no_repeat(_) and no_anagrams(_)]
print(f"Result 2: {len(valid_phrase)}")

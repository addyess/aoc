from itertools import combinations
from collections import defaultdict

with open("day21.txt") as f_in:
    ins = [_.strip() for _ in f_in]


class Food:
    @classmethod
    def parse(cls, lines):
        return [cls(line) for line in lines]

    def __init__(self, line):
        head, tail = line.strip(')').split('(contains ')
        self.allergens = set(tail.split(', '))
        self.ingredients = set(head.split())

    def remove_defs(self, defs):
        for a, i in defs.items():
            self.allergens.discard(a)
            self.ingredients.discard(i)


# ins = """
# mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
# trh fvjkl sbzzf mxmxvkd (contains dairy)
# sqjhc fvjkl (contains soy)
# sqjhc mxmxvkd sbzzf (contains fish)
# """.strip().splitlines()

foods = Food.parse(ins)
all_allergens = set(_ for food in foods for _ in food.allergens)
all_ingredients = set(_ for food in foods for _ in food.ingredients)
definite = {}
definite_not = defaultdict(set)

while True:
    w_def = dict(definite.items())
    for pair in combinations(foods, 2):
        a, b = pair
        shared_allergens = a.allergens & b.allergens - set(w_def.keys())
        if shared_allergens:
            shared_ingredients = a.ingredients & b.ingredients - set(w_def.values())
            diff_ingredients = a.ingredients - b.ingredients
            if len(shared_allergens) == len(shared_ingredients) == 1:
                definite[shared_allergens.pop()] = shared_ingredients.pop()
            for a in shared_allergens:
                definite_not[a] |= diff_ingredients

    for f in foods:
        f.remove_defs(definite)
        if len(f.allergens) == len(f.ingredients) == 1:
            definite[f.allergens.pop()] = f.ingredients.pop()
        for a, i in definite_not.items():
            if a in f.allergens:
                remaining = f.ingredients - i
                if len(remaining) == 1:
                    definite[a] = remaining.pop()
    if w_def == definite:
        break

assert len(definite) == len(all_allergens)
non_alergens = all_ingredients - set(definite.values())
print(f"Result 1: {len([i for f in foods for i in f.ingredients])}")
dangerous = ",".join([i for a, i in sorted(definite.items())])
print(f"Result 2: {dangerous}")

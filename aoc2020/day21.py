from itertools import combinations
from collections import defaultdict


class Food:
    def __init__(self, line):
        head, tail = line.strip(')').split('(contains ')
        self.allergens = set(tail.split(', '))
        self.ingredients = set(head.split())

    def remove_defs(self, defs):
        for a, i in defs.items():
            self.allergens.discard(a)
            self.ingredients.discard(i)


with open("day21.txt") as f_in:
    foods = [Food(line.strip()) for line in f_in]
all_allergens = set(_ for food in foods for _ in food.allergens)
all_ingredients = set(_ for food in foods for _ in food.ingredients)
w_def, definite, definite_not = None, {}, defaultdict(set)

while w_def != definite:
    w_def = dict(definite.items())
    for food_a, food_b in combinations(foods, 2):
        shared_allergens = food_a.allergens & food_b.allergens - set(w_def.keys())
        if shared_allergens:
            shared_ingredients = food_a.ingredients & food_b.ingredients - set(w_def.values())
            diff_ingredients = food_a.ingredients - food_b.ingredients
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

assert len(definite) == len(all_allergens)
print(f"Result 1: {len([i for f in foods for i in f.ingredients])}")
print(f"Result 2: {','.join([i for a, i in sorted(definite.items())])}")

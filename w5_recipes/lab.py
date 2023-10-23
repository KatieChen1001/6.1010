"""
6.101 Lab 6:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    recipe_book = {}
    # loop through recipes
    for recipe in recipes: 
        category, name, info = recipe
        # if is compound
        if category == "compound": 
            # if compound not in dictionary 
            if name not in recipe_book.keys(): 
                # add it
                recipe_book[name] = [info] 
                # if there's only one way to make a burger, 
                # then that way of making it will be in list of list
                # [[('bread', 2), ('cheese', 1), ('lettuce', 1), ('protein', 1), ('ketchup', 1)]]
            # if compound in dictionary
            else:     
                # if the ways of making compound has not been logged
                if info != recipe_book[name]: 
                    # add it
                    recipe_book[name].append(info)          

    return recipe_book

def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_costs = {}

    for recipe in recipes: 
        category, name, cost = recipe
        if category == "atomic": 
            if name not in atomic_costs.keys(): 
                atomic_costs[name] = cost
    
    return atomic_costs


def lowest_cost(recipes, food_item):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    # create recipe_book and atomic_cost
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    
    # def breakdown_compound() - recursive funtion
    def breakdown_compound(food_item):
        
        # base case: we get to atomic
        if food_item in atomic_costs.keys():
            return atomic_costs[food_item]
        
        # recursive case: 
        elif food_item in recipe_book.keys(): # we have got a compound! 
            # if there's more than one way to make compound
            ways_to_make_food_item = recipe_book[food_item]
            
            possible_costs = []
            for way in ways_to_make_food_item: 
                # way should be a list of tuples
                cost = 0
                for new_item, num in way:
                    unit_cost = breakdown_compound(new_item)
                    cost += unit_cost * num

                possible_costs.append(cost)
                    
            return min(possible_costs)

        else: 
            return float("inf")
    
    res = breakdown_compound(food_item)
    if res == float("inf"): 
        return None 
    else: 
        return res

def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    raise NotImplementedError


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    raise NotImplementedError


def cheapest_flat_recipe(recipes, food_item):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    raise NotImplementedError


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of 
    ingredient recipes.
    """
    raise NotImplementedError


def all_flat_recipes(recipes, food_item):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    raise NotImplementedError


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!

    # recipe_book = make_recipe_book(example_recipes)
    # print({key: value for key, value in recipe_book.items() if len(value) > 1})

    # atomic_costs = make_atomic_costs(example_recipes)
    # print(sum([value for key, value in atomic_costs.items()]))

    # cookie_recipes = [
    #     ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    #     ('compound', 'cookie', [('chocolate chips', 3)]),
    #     ('compound', 'cookie', [('sugar', 10)]),
    #     ('atomic', 'chocolate chips', 200),
    #     ('atomic', 'sugar', 5),
    #     ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    #     ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    #     ('atomic', 'vanilla ice cream', 20),
    #     ('atomic', 'chocolate ice cream', 30),
    # ]

    # print(lowest_cost(cookie_recipes, "cookie sandwich"))

    dairy_recipes_2 = [
        ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
        ('compound', 'cheese', [('milk', 1), ('time', 1)]),
        ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
        ('atomic', 'milking stool', 5),
        ('atomic', 'cutting-edge laboratory', 1000),
        ('atomic', 'time', 10000),
    ]

    print(lowest_cost(dairy_recipes_2, 'cheese'))
    # pass


import json
import codecs
import re
import itertools

def load_cocktail_dict(path):
    # read the cocktail database
    with codecs.open(path, 'r', encoding='utf-8') as f:
        res = json.load(f)

    # clean-up ingredients and delete everything not needed for the task
    # (e.g. the instructions and required quantities).
    for key in res.keys():
        ingredients = [normalize_string(k) for k in res[key]['ingredients'].keys()]
        # after normalisation, some ingredients may occur multiple times
        # => use a set to make them unique
        res[key] = set(ingredients)
    return res

# remove various kinds of 'noise' from the ingredient strings
def normalize_string(string):
    # This function uses 'regular expression' techniques to
    # clean-up strings, but simpler approaches will also work.
    string = string.lower()                    # only lower case
    string = str(re.sub('\(.*\)', '', string)) # remove brackets and their contents
    string = str(re.sub(',.*', '', string))    # remove everything after a comma
    for k in list(', :(*\''):
        string = string.replace(k, '')         # remove special chars
    return string


# some manual replacements which cannot be done by generic string manipulations
def manual_normalizations(cocktail_dict):

    # helper function: replace ing1 with ing2
    def replace_ingredient(cocktail_dict, ing1, ing2):

        for ingredients in cocktail_dict.values():
            try:
                ingredients.remove(ing1)
                # this is only reached if remove() did not raise an exception
                ingredients.add(ing2)
            except:
                pass  # continue if ing1 was not in ingredients

    replace_ingredient(cocktail_dict,'ananas-schnitz','ananas')
    replace_ingredient(cocktail_dict,'babyananas','ananas')
    replace_ingredient(cocktail_dict,'champagnerodertrockenersekt','sekt')
    replace_ingredient(cocktail_dict,'crushedice','eiswürfel')
    replace_ingredient(cocktail_dict,'eigelb','ei')
    replace_ingredient(cocktail_dict,'eiweiß','ei')
    replace_ingredient(cocktail_dict,'erdbeer','erdbeeren')
    replace_ingredient(cocktail_dict,'erdbeere','erdbeeren')
    replace_ingredient(cocktail_dict,'läuterzucker','zucker')
    replace_ingredient(cocktail_dict,'meersalz','salz')
    replace_ingredient(cocktail_dict,'melonegeschält','melone')
    replace_ingredient(cocktail_dict,'milch-schaum','milch')
    replace_ingredient(cocktail_dict,'natur-joghurt','joghurt')
    replace_ingredient(cocktail_dict,'orange','orangen')
    replace_ingredient(cocktail_dict,'orangenlimonade','fanta')
    replace_ingredient(cocktail_dict,'orangenschale','orangen')
    replace_ingredient(cocktail_dict,'orangenscheibe','orangen')
    replace_ingredient(cocktail_dict,'redbull','energydrink')
    replace_ingredient(cocktail_dict,'rohrzucker','zucker')
    replace_ingredient(cocktail_dict,'saftundzuckergemischt','saft')
    replace_ingredient(cocktail_dict,'saftvontropischenfrüchten','saft')
    replace_ingredient(cocktail_dict,'sahneersatz','sahne')
    replace_ingredient(cocktail_dict,'schokoladenraspel','schokolade')
    replace_ingredient(cocktail_dict,'schokoladenstreusel','schokolade')
    replace_ingredient(cocktail_dict,'schokostreusel','schokolade')
    replace_ingredient(cocktail_dict,'schokoriegel','schokolade')
    replace_ingredient(cocktail_dict,'süßesahne','sahne')
    replace_ingredient(cocktail_dict,'vanillemark','vanilleschote')
    replace_ingredient(cocktail_dict,'zitronensaft','zitrone')
    replace_ingredient(cocktail_dict,'zitronenschale','zitrone')
    replace_ingredient(cocktail_dict,'zuckerrohrsirup','zuckersirup')
    return cocktail_dict

# collect all ingredients
def all_ingredients(cocktail_dict):
    ingredients = set()
    for i in cocktail_dict.values():
        ingredients |= i   # compute union of all ingredient sets
    return ingredients

# determine the inverted dictionary
def cocktails_inverse(recipes):
    inv = {}
    for cocktail, ingredients in recipes.items():
        for i in ingredients:
            try:
                # append cocktail if ingredient is already known
                inv[i].append(cocktail)
            except KeyError:
                # otherwise, create a new entry
                inv[i] = [cocktail]
    return inv

# write the dictionnary dic to the file 'file_name'
def write_dic_to_json(dic, file_name):

    with open(file_name, 'w') as file:
        # 'sort_keys' makes it easier to check the result
        json.dump(dic, file, sort_keys=True)

# delete every ingredient from ignore_list in this dictionary
def remove_ingredients(cocktail_dict, ignore_list):

    for ignore in ignore_list:
        for ingredients in cocktail_dict.values():
            try:
                ingredients.remove(ignore)
            except:
                pass  # continue if 'ignore' was not in ingredients
    return cocktail_dict

# delete every ingredient from ignore_list in 'ingredients'
def ignore_ingredients(ingredients, ignore_list):

    for ig in ignore_list:
        try:
            ingredients.remove(ig)
        except:
            pass

# return a list of possible cocktails for the available_ingredients
def possible_cocktails(inverse_recipes, recipes, available_ingredients):

    # find recipes containing any of the available ingredients
    cocktails = set()
    for ingredient in available_ingredients:
        cocktails |= set(inverse_recipes[ingredient])

    # only keep cocktails that do not need additional stuff
    available_set = set(available_ingredients)
    result = []
    for cocktail in cocktails:
        if recipes[cocktail].issubset(available_set):
            result.append(cocktail)

    return result

# remove all cocktails requiring more than 'limit' ingredients
def limit_to(recipes, limit):
    for key in list(recipes.keys()):
        if len(recipes[key]) > limit:
            del recipes[key]
    return recipes

# Insert all ingredients into buckets such that:
#  * ingredients in the same bucket are mutually exclusive,
#    i.e. never occur in the same cocktail
#  * ingredients in each bucket are sorted by decreasing priority,
#    i.e. by decreasing number of cocktails containing them
# Argument 'ingredients' must be an array of tuples (ingredient, priority)
# and must be sorted in decreasing order of priorities.
def bucket_ingredients(inv_recipes, ingredients):
    buckets = []

    # process ingredients by decreasing priority
    for k in ingredients:
        ing0 = k[0]               # the current ingredient
        cock0 = inv_recipes[ing0] # cocktails containing ing0

        # find the first bucket where ing0 can be inserted
        for b in buckets:
            mutual_exclusive = True
            for ing1 in b: # check with every ingredient in that bucket
                if not cock0.isdisjoint(inv_recipes[ing1]):
                    mutual_exclusive = False # there is a common cocktail
                    break                    # => ing0 cannot be in b
            if mutual_exclusive:  # no common cocktail
                b.append(ing0)    # => ing0 goes into b
                ing0 = None
                break
        if ing0 is not None:        # no suitable bucket found
            buckets.append([ing0])  # => create a new one

    return buckets

# find 5 ingredients that allow for the maximum number of cocktails
def optimal_ingredients(recipes, inv_recipes):

    # keep only ingredients contained in at least 11 cocktails
    # and sort by decreasing priority
    ingredients = [(i, len(c)) for i, c in inv_recipes.items() if len(c) >= 11]
    ingredients.sort(key=lambda x: x[1], reverse=True)

    print('Vorselektion für Optimierung: %d Cocktails und %d Zutaten.' %
          (len(recipes), len(ingredients)))

    # turn the elements of inv_recipes into sets to speed-up subsequent computations
    for k, c in inv_recipes.items():
        inv_recipes[k] = set(c)

    buckets = bucket_ingredients(inv_recipes, ingredients)
    print('%d Buckets gefunden\n' % len(buckets))

    max_count = 0
    # create all combinations of 5 buckets, starting with the highest priority ones
    for bucket_comb in itertools.combinations(buckets, 5):
        # create all combinations of 5 ingredients, one from each of the selected buckets
        for ingr in itertools.product(*bucket_comb):
            # determine number of possible cocktails and keep the best combination
            res = possible_cocktails(inv_recipes, recipes, ingr)
            if len(res) > max_count:
                optimal = ingr
                max_count = len(res)
                print('Aus', optimal, 'kann man %d Cocktails mixen.' % len(res))
    return optimal

def main():
    #a)
    recipes = load_cocktail_dict('cocktails.json')
    recipes = manual_normalizations(recipes)
    ingredients = all_ingredients(recipes)

    #print('Anzahl der Zutaten:', len(ingredients))

    #b)
    # get inverse dic and save to disc
    inv_recipes = cocktails_inverse(recipes)


    write_dic_to_json(inv_recipes, "cocktails_inverse.json")

    a = ["sahne", "grapefruitsaft", "wodka", "milch", "limettensaft",'bier', "cola", "holunderbeersirup",
        'cocktailkirsche',
        'ei',
        'eiswürfel',
        'essig',
        'fruchtsaft',
        'kekse',
        'milch',
        'mineralwasser',
        'nutella',
        'olive',
        'paprikapulver',
        'pfeffer',
        'rosmarin',
        'sahne',
        'saft',
        'salz',
        'salzstangen',
        'schnaps',
        'süßigkeiten',
        'tee',
        'waffeln',
        'wasser',
        'wodka',
        'zimt',
        'zitrone',
        'zwiebel',
        'zucker',
        "zitrone",
        "limette",
        'öl',
        "whisky"]

    possible = possible_cocktails(inv_recipes, recipes, a)
    print(possible)
    # determine how often each ingredient is needed and
    # sort in descending order
    ingredient_count = [(i, len(c)) for i, c in inv_recipes.items()]
    ingredient_count.sort(key=lambda x: x[1], reverse=True)

    #print('Die 15 gebräuchlichsten Zutaten:')
    #for k in ingredient_count[:15]:
        #print('  %s: %d' % k)
    #print('\n')

    #c)
    # ignore_list contains ingredients that are always on hand
    # or are not essential for the cocktail
    ignore_list = [
        'bier',
        'cocktailkirsche',
        'ei',
        'eiswürfel',
        'essig',
        'fruchtsaft',
        'kekse',
        'milch',
        'mineralwasser',
        'nutella',
        'olive',
        'paprikapulver',
        'pfeffer',
        'rosmarin',
        'sahne',
        'saft',
        'salz',
        'salzstangen',
        'schnaps',
        'sekt',
        'süßigkeiten',
        'tee',
        'waffeln',
        'wasser',
        'wodka',
        'zimt',
        'zitrone',
        'zwiebel',
        'zucker',
        'öl',
        "weißer rum",
        "zitronensaft"]

    # remove contents of ignore_list and recalculate inverse dict
    recipes = remove_ingredients(recipes, ignore_list)
    inv_recipes = cocktails_inverse(recipes)
    desired_ingredients = ['genever', 'pfeffer', 'mett', 'zwiebel']
    # filter ingredient list (remove stuff from ignore_list)
    ignore_ingredients(desired_ingredients, ignore_list)

    #print('Mögliche Cocktails für %r:' % desired_ingredients)
    #for cocktail in possible_cocktails(inv_recipes, recipes, desired_ingredients):
        #print(cocktail) # the Metthattan!
    #print('\n')

    #d)
    # limit to cocktails with at most 5 ingredients and recalculate inverse dict
    recipes = limit_to(recipes, 5)
    inv_recipes = cocktails_inverse(recipes)

    #optimal = optimal_ingredients(recipes, inv_recipes)
    #res = possible_cocktails(inv_recipes, recipes, optimal)
    #print('\nDie optimalen Zutaten sind:', optimal)
    #print('Zusammen mit den immer vorhandenen Zutaten aus der \'ignore_list\' kann man\ndamit %d Cocktails mixen:' % len(res))
    #print(res)


if __name__ == "__main__":
    main()
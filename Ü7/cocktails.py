import json

def all_ingredients(recipes):
    ingredients = []
    for cocktail in recipes:
        for x in recipes[cocktail]["ingredients"]: #Läuft alle Einträge durch
            x = normalize_string(x)
            if x not in ingredients:
                ingredients.append(x)
    #print(ingredients)
    #print(len(ingredients)-1)  Aufgabe a) = 6091
    return ingredients


def normalize_string(s):
    s = s.lower()
    if "," in s:
        new_word = s.split(",")
        s = new_word[0]
    if "(" in s:
        new_word = s.split("(")
        s = new_word[0]
    return s

def cocktails_inverse(recipes):
    inverse_recipe = {}
    for cocktail in recipes:
        for x in recipes[cocktail]["ingredients"]: # Läuft alle Einträge durch
            x = normalize_string(x)
            if x in inverse_recipe:                     # Existiert schon?
                inverse_recipe[x].append(cocktail)
            else:
                inverse_recipe[x] = [cocktail]
    #print(inverse_recipe)
    return inverse_recipe

def all_ignore(ignore_list, inverse_recipes):
    temp = []
    for word in ignore_list:
        word = normalize_string(word)
        if word in inverse_recipes:
            temp.append(word)
        else:
            continue

    return temp

def possible_cocktails(inverse_recipes, available_ingredients,recipes, ignore_list):
    ni = []
    available_cocktail = []
    ignore = all_ignore(ignore_list, inverse_recipes)
    needed = []

    for word in available_ingredients:  #Nutzlose Ingredients ausfiltern
        word = normalize_string(word)
        if word in inverse_recipes and word not in ignore and word not in ni:
            ni.append(word)

    for ingredients in inverse_recipes:  # Alle Rezepte durchgehen und passende (falls benötigte Zutaten in verfügbaren
                                         # Zutaten drin) Cocktails zurückgeben.
        for cocktail in inverse_recipes[ingredients]:
            temp = []
            for word in recipes[cocktail]["ingredients"]:
                word = normalize_string(word)
                if word not in ignore:
                    temp.append(word)
                else:
                    continue

            for i in range(len(temp)):
                if temp[i] in ni:
                    needed.append(temp[i])
                    if i == len(temp) - 1:
                        if cocktail not in available_cocktail:
                            available_cocktail.append(cocktail)
                        else:
                            continue
                    else:
                        i += 1
                        continue
                else:
                    break
    #print()
    #print(f"Sie haben als Auswahl:")
    #for j in range(len(available_cocktail)):
        #print(available_cocktail[j])

    return available_cocktail

def best_ingredients(inverse_recipes, ignore_list):
    ignore = all_ignore(ignore_list, inverse_recipes)
    best_ingredients = []
    best_cocktails =[]
    vip_cocktail = []
    vip_ingredient = []
    temp = []

    for word in inverse_recipes:
        if len(inverse_recipes[word]) > 60 and word not in ignore:  #Hier finden wir die interessantesten Zutaten durch Quantität
            if word not in best_ingredients:
                best_ingredients.append(word)
                best_cocktails.append(inverse_recipes[word])  #und hier die Cocktails zu den Zutaten
            else:
                continue

    for k in range(len(best_cocktails[0])):  #Hier suchen wir die "größten" Schnittstellen der Zutaten Cocktails
        l = 0
        cocktail = best_cocktails[0][k]
        for j in range(len(best_cocktails)):
            if cocktail in best_cocktails[j]:
                l += 1
            else:
                continue
        if l > 4:  #4, da wir die 5 besten Zutaten suchen
            vip_cocktail.append(cocktail)

    for word in best_ingredients:  #Jetzt kommen sehr eckelhafte schleifen ,um genaue schnittmengen herauszufinden
        t = 0
        for u in range(len(vip_cocktail)):  #Filtern
            if vip_cocktail[u] in inverse_recipes[word]:
                vip_ingredient.append(word)
            else:
                continue

###################################################################################################################
    #Tl;dr bis hier ist alles nur "geschickt" filtern.
###################################################################################################################
        
        for k in range(len(vip_ingredient)):  #Häufigkeit von ingredients in vip_ingredients feststellen
            if t >= 3:
                if vip_ingredient[k] not in temp:
                    temp.append(vip_ingredient[k])
                else:
                    continue
            if vip_ingredient[k] == word:
                t +=1


    return temp

if __name__ == "__main__":
    with open("cocktails.json", encoding="utf-8") as f:
        recipes = json.load(f)

    ingredients = all_ingredients(recipes)
    inverse_recipes = cocktails_inverse(recipes)
    with open("ignore_list.txt", encoding="utf-8") as f:
        ignore_list = f.read().split("\n")

    available_ingredients0 = ["Sahne", "Grapefruitsaft", "Zitronensaft", "Rum", "Wodka", "Milch", "Orangensaft",
     "weißer Rum", "dunkler Rum", "Limettensaft"]
    available_ingredients = available_ingredients0 + ignore_list
    print(available_ingredients)

    available_ingredients1 = possible_cocktails(inverse_recipes, available_ingredients,recipes, ignore_list)
    print(available_ingredients1)

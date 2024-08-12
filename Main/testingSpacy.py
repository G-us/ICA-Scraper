def contains_gluten(ingredient):
    # Define the words to search for
    gluten_words = ["vete", "gluten", "korn"]
    # Define the words that indicate gluten-free
    gluten_free_words = ["glutenfri", "gluten-free", "gluten free"]

    # Check if any gluten-free indicator is in the ingredient
    if any(gluten_free_word in ingredient.lower() for gluten_free_word in gluten_free_words):
        return False

    # Check if any gluten-containing word is in the ingredient
    if any(gluten_word in ingredient.lower() for gluten_word in gluten_words):
        return True

    return False

def check_ingredients(ingredients_list):
    # Split the ingredients list by commas
    ingredients = ingredients_list.split(',')

    # Check each ingredient
    flagged_ingredients = [ingredient.strip() for ingredient in ingredients if contains_gluten(ingredient)]

    return flagged_ingredients

# Example usage
ingredients_list = "mjöl, vatten, glutenfri vete, glutenfri bröd, korn, socker"
flagged = check_ingredients(ingredients_list)
print("Flagged ingredients containing gluten:", flagged)
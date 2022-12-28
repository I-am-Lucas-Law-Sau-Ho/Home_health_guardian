import requests
import sqlite3 as sql
import json
import urllib
from random import randint

FILENAME = "test_recipe_03.db"
con = sql.connect(FILENAME)
C = con.cursor()

# ID set is used to ensure all recipes have unique ID
IDS = {-1}
APP_ID = "YOUR APP ID"
API_KEY = "YOUR API KEY"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'


"""
============================================================================
RECIPE APP:
============================================================================
"""
def main():
    """
    This program allows the user to search for recipes online using the
    Edamam API. It also allows the user to save lookup info for favorite
    recipes into a database. Finally, the user can look up saved recipes.
    """
    print()
    command = ''
    while command.lower() != 'q':
        print("1) Find New Recipe")
        print("2) Search Saved Recipes")
        command = input("\t>> ")
        print()
        if command == '1':
            query_recipes()
        elif command == '2':
            search_my_recipes()
    C.close()


"""
============================================================================
FIND NEW RECIPES:
============================================================================
"""

def query_recipes():
    """
    Search and select recipe to view from API.
    """    
    response = None
    success = False
    index = 0
    while not success:
        print("Please enter a keyword")
        key_word = input("\t>> ")
        data = make_request(get_url_q(key_word))
        data = data['hits']
        if len(data) > 0:
            success = True
        else:
            print(f'0 results for "{key_word}"')
            input("")
    index = display_recipe_labels(data, index)
    print(f"   Select Recipe # (1-{index})\n   (enter 'm' to see more)")
    select = select_from_index(index) 
    # Allows user to request 20 more recipes with same keyword
    if select == 'm' and index == 20:
        _from = 20
        to = 40
        data2 = make_request(get_url_q(key_word, _from, to))
        data2 = data2['hits']
        index = display_recipe_labels(data2, index)
        # join the data of both requests together
        data += data2
        #selection has not yet been made
        select = -1     
    select_recipe(data, index, select)

def select_recipe(data,max_index,select):
    """
    Select & save unsaved recipe.
    """
    # If select == -1, no selection has been made
    invalid = True
    while invalid:
        if select == -1:
            select = select_recipe_from_index(max_index)
        if select == 'm':
            display_recipe_labels(data,0)
            select = select_recipe_from_index(max_index)
        if select == 'q':
            print()
            return
        try:
            select = int(select)
            invalid = False
        except ValueError:
            invalid = True
            select = -1

    recipe_response = data[select]
    recipe = recipe_response["recipe"]
    curr_recipe = filter_response(recipe)

    display_recipe_dict(curr_recipe)
    if input("Would you like to save? (y/n) ") == 'y':
        save_recipe(curr_recipe)
    else:
        print()
        print("1) Select another recipe")
        print("2) Main menu")
        command = input("\t>> ")
        if command == '1':
            select_recipe(data,max_index,-1)
        else:
            print()

def display_recipe_labels(data, index):
    """
    Displays all recipe labels from a result of request.
    Returns the max index of list of recipes.
    """
    print()
    for recipe in data:
        index += 1
        print(f"   {index})", recipe['recipe']['label'])
    print()
    return index

def save_recipe(curr_recipe):
    """
    Saves recipe info in database of saved recipes.
    """
    id = -1
    if id in IDS:
        id = randint(100,999)  
    # Saves ID, URI, and label to database
    C.execute("INSERT into recipes (id, uri, label) values (?, ?, ?)", (id,curr_recipe["uri"], curr_recipe["label"]))
    # Displays label to confirm correct entry
    C.execute("SELECT label FROM recipes WHERE label = ?",(curr_recipe["label"],))
    result = C.fetchall()
    print(f"    You are saving: '{result[0][0]}'")
    if input("Confirm (y/n): ").lower() == "y":
        con.commit()
    print("SAVED")
    input()
    print()


"""
============================================================================
SELECT SAVED RECIPE:
============================================================================
"""

def search_my_recipes():
    """
    Search DB of saved recipes.
    """
    print("Saved:")
    print("---------------------------------------------")
    C.execute("SELECT label, id FROM recipes")
    result = C.fetchall()

    i = 0
    for recipe in result:
        i += 1
        print(f"   {i}) {recipe[0]}")
    print("---------------------------------------------")
    print()
    select_recipe_saved(result, i)

def select_recipe_saved(data, max_index):
    """
    Uses the index of the list of saved recipes to select recipe ID
    """
    select = ""
    while type(select) != type(0):
        select = select_recipe_from_index(max_index)
    print()
    print(f"Opening: {data[select][0]}...")
    id = data[select][1]
    display_saved_recipe(id)

def display_saved_recipe(id):
    """
    Displays recipe with given ID.
    """
    recipe = make_request_by_uri(id)
    display_recipe_dict(recipe)

def make_request_by_uri(id):
    """
    Makes a request based on saved URI. Param ID is used
    to retrieve URI from database.
    Returns selected recipe as a dictionary.
    """
    C.execute(f"SELECT uri FROM recipes WHERE id = ?",(id,))
    uri = C.fetchall()[0][0]
    uri = urllib.parse.quote_plus(uri)
    url = get_url_r(uri)
    data = make_request(url)[0]
    return filter_response(data)


"""
============================================================================
SELECT/DISPLAY:
============================================================================
"""

def select_recipe_from_index(max_index):
    print(f"   Select Recipe # (1-{max_index})")
    return select_from_index(max_index)

def select_from_index(max_index):
    select = -1
    while select <= 0 or select > max_index:
        select = input("\t>> ")
        if select.lower() == 'q':
            return 'q'
        elif select.lower() == 'm':
            return 'm'
        try:
            select = int(select)
        except ValueError as e:
            print("Input must be an integer!")
            select = -1
    return select-1

def filter_response(recipe):
    """
    Takes response object and returns dictionary with readable 
    recipe data
    """
    curr_recipe = {
        "ingredients_line" : recipe["ingredientLines"],
        "ingredients" : recipe["ingredients"],
        "label" : recipe["label"],
        "url" : recipe["url"],
        "uri" : recipe["uri"]}
    return curr_recipe

def display_recipe_dict(curr_recipe):
    """
    Displays dictionary curr_recipe.
    Dictionary curr_recipe keys include: 
        - "ingredients_line"
        - "ingredients"
        - "label"
        - "url"
    """
    print()
    print("====================================================")
    print(f"{curr_recipe['label']}:")
    print("----------------------------------------------------")
    for line in curr_recipe["ingredients_line"]:
        print(f"    - {line}")
    print()
    print(f"Directions: {curr_recipe['url']}")
    print("====================================================")
    input()


"""
============================================================================
EDIT SAVED RECIPES:
   Future additions include:
      - Option to add recipe directions to DB
      - Option to remove recipe from DB
      - Add your rating out of 5 stars
      - Prioritize/sort/search recipes based on rating
============================================================================
"""

def add_directions(text):
    """
    Adds directions to recipe table.
    """
    pass

def delete_saved_recipe(recipe_id):
    """
    Removes selected recipe from database.
    """
    pass

def add_star_rating(recipe_id, rating):
    """
    Adds rating out of 5 to recipe
    """
    pass



"""
============================================================================
MAKE REQUESTS:
============================================================================
"""

def make_request(url):
    """
    Returns a request response from a given URL.
    """
    response = requests.get(url)
    data = response.json()
    return data

def get_url_q(key_word,_from=0,to=20):
    url = URL + f'&q=${key_word}&to={to}&from={_from}'
    return url

def get_url_r(uri):
    return URL + f'&r={uri}'


main()

# Uncomment for development assistance.

# def display_keys(recipe):
#     """
#     Used for development: traversing json data and dictionaries
#     """
#     for i in recipe:
#         print(i)
#         input()
    

"""
All constants used for dialysis project
accumulated in one file for easier accessibility
and cleaner code.
""" 

# Window settings and all colors used in project
WINDOW_TITLE = "Dialysis Nutrition Information By Sheung Wo Street Boy God"
MAIN_WINDOW_SIZE = "1200x800"
MAIN_WINDOW_COLOR = "#bedddc"
MAIN_FRAME_COLOR = "#f4efeb"
GOOD_FOOD_COLOR = "#9be281"
BAD_FOOD_COLOR = "#f9a08b"
BTN_COLOR = "#e5c5c8"

# Guidelines Category
# => Daily Intake Content
DAILY_NUTR_LEFT = ["Calories", "Salt", "Protein", "Potassium", "Phosphorous", "Liquid"]
DAILY_NUTR_RIGHT = [
    "30cal/kg per day",
    "5-6g per day (including Sodium)",
    "1,2g/kg per day",
    "2000-2500mg per day",
    "1000-1400mg per day",
    "500ml + residual excretion/24h",
]

# => Recommended Foods List
GOOD_LIST_LEFT = [
    "Zucchini, Cucumbers",
    "Lemons, Lime",
    "Blueberries",
    "Apple, Pears",
    "Salads",
    "Couscous",
    "Lean Meat",
    "Most Fish",
    "Cauliflower",
    "Olive Oil, Butter",
    "Mushrooms",
]
GOOD_LIST_RIGHT = [
    "Radish, Celery",
    "Green Pepper",
    "Strawberries",
    "Carrots, Green Beans",
    "Cream",
    "Mozzarella",
    "Onion, Garlic",
    "Honey, Jam",
    "Eggs",
    "Watermelon",
    "Cooked Rice, Pasta",
]

# => Foods to Avoid List
BAD_LIST_LEFT = [
    "Potatoes",
    "Tee, Cola",
    "Tzatziki",
    "Avocados",
    "Olives, Pickles, Relish",
    "Canned Fish, Meat, Beans",
    "Smoked Fish or Meat",
    "Offal, Sausages, Salmon",
    "Processed Foods",
    "Ketchup, Mayonnaise",
    "Saturated Fat",
]
BAD_LIST_RIGHT = [
    "Chocolate",
    "Dried Fruits",
    "Marzipan",
    "Bananas, Kiwis",
    "Dates, Figs",
    "Canned Tomato Products/Juice",
    "Undiluted Fruit Juice",
    "Vegetable Juice",
    "Feta, Parmesan, Cheddar etc.",
    "Most Dairy Products",
    "Coconuts, Nuts",
]

# Tips and Tricks Category Content
SALT_CONTENT = [
    "- Season food after it's\n  cooked for more control",
    "- Don't use salt substitute!\n  Use alternatives instead",
    "- Alternatives are:\n  Basil, Cilantro, Garlic\n  Oregano, Mint, Chives\n  Lemon, Parsley, Sage",
]
PHOSPHOROUS_CONTENT = [
    "- Throw out cooking water\n  & change while cooking",
    "- Throw away canned\n  vegetables & meat juice",
    "- Soak diced vegetables\n  in  water before cooking",
    "- Dice or shred vegetables\n  with high  phosphorous\n  content",
]
ADDITIONAL_CONTENT = [
    "- Avoid eating animal skin\n  (poultry)",
    "- Try not to eat egss more\n  than 3x per week",
    "- Pre-fill your water bottle\n  for the entire day",
    "- Remember food contains\n  water as well!\n  (fruits, soup, ice cream)",
]

# API
API = "DEMO_KEY"

NUTRIENT_NAME = [
    "Protein",
    "Energy",
    "Phosphorus, P",
    "Potassium, K",
    "Sodium, Na",
]

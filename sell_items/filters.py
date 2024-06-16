BASIC_EGGS = [
    'BearCub', 'Cactus', 'Dragon', 'FlyingPig',
    'Fox', 'LionCub', 'PandaCub', 'TigerCub',
    'Wolf'
]

BASIC_POTIONS = [
    'Base', 'CottonCandyBlue', 'CottonCandyPink',
    'Desert', 'Golden', 'Red', 'Shade', 'Skeleton',
    'White', 'Zombie'
]

BASIC_FOOD = [
    'Chocolate', 'CottonCandyBlue', 'CottonCandyPink',
    'Fish', 'Honey', 'Meat', 'Milk', 'Potatoe', 'RottenMeat',
    'Strawberry'
]

def filter_items(items):
    """
    Filters the items list to only include the common eggs, potions, and food.
    """
    items['eggs'] = {k: v for k, v in items['eggs'].items() if k in BASIC_EGGS}
    items['hatchingPotions'] = {k: v for k, v in items['hatchingPotions'].items() if k in BASIC_POTIONS}
    items['food'] = {k: v for k, v in items['food'].items() if k in BASIC_FOOD}
    return items
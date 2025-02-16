import json

def load_material_prices(material_type):
    if material_type == "steel":
        with open('data/steel_prices.json', 'r') as f:
            material_prices = json.load(f)
    elif material_type == "wood":
        with open('data/wood_prices.json', 'r') as f:
            material_prices = json.load(f)
    elif material_type == "concrete":
        with open('data/concrete_prices.json', 'r') as f:
            material_prices = json.load(f)
    else:
        raise ValueError("Invalid material type")
    return material_prices

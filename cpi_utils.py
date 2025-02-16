import json
import pandas as pd

def load_cpi_data():
    with open('data/cpi_database.json', 'r') as f:
        cpi_data = json.load(f)
    return cpi_data

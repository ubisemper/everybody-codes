import argparse
import pandas as pd
import numpy as np

DATA_PATH = '../data/cameras-defb.csv'

def load_data(path_name):
    return pd.read_csv(path_name)
    
def search_data(name, path):
    data = load_data(path)
    
    data[["name", "Latitude" , "Longitude"]] = data["Camera;Latitude;Longitude"].str.split(';', expand=True)
    data.drop(["Camera;Latitude;Longitude"], axis=1, inplace=True)
    
    data = data[~data["name"].str.contains("ERROR")]
    
    data["ID"] = data["name"].str.extract('(\d+)')
    
    # Waarom hier voor gegaan? Langere tekens of
    data["GeoIdent"] = data["name"].str.extract('(?:(.+[A-Z]{3}|.*[0-9]{3}))')
    data["name"] = data["name"].str.split('(?:(.+[A-Z]{3}|.*[0-9]{3}))', expand=True)[2]
    
    data["name"] = data["name"].str.removeprefix('-')
    data["name"] = data["name"].str.strip('/ ')   
    
    if name == 'all':
        return data
    
    return data[data["name"].str.contains(name, case=False)]




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="name of the place. To return all instances type 'all'")
    args = parser.parse_args()
    
    data = search_data(name=args.name, path=DATA_PATH)
    
    for row in data.iterrows():
        print(f"{row[1][3]} | {row[1][4]} {row[1][0]} | {row[1][1]} | {row[1][2]}")
from flask import Flask
from matplotlib.artist import get
from CLI import search_data
import pandas as pd

name = 'all'
path = '../data/cameras-defb.csv'

app = Flask(__name__)

@app.route('/cam_data')

def get_cam_data(name=name, path=path):
    
    # data = search_data(name, path)
    try:
        data = search_data(name, path)
    except:
         print('Error in searching / Loading the data')
    
    return data.to_json(orient='records')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
from re import A
from turtle import pd
from flask import Flask, render_template
import requests
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

def process_data(data):
    parse_json = json.loads(data)
    data = pd.DataFrame.from_dict(parse_json, orient='columns')
    data['ID'] = data['ID'].astype('int')
    
    box1 = data.loc[data['ID'] % 3 == 0]
    box2 = data.loc[data['ID'] % 5 == 0]
    box3 = data.loc[(data['ID'] % 3 == 0) & (data['ID'] % 5 == 0)]
    
    idx1 = box1['ID'].values
    idx2 = box2['ID'].values

    idx = np.unique(np.concatenate((idx1, idx2)))
    
    box4 = data[~data['ID'].isin(idx)]
    
    lat, long = data['Latitude'], data['Longitude']
    print(lat)
    return box1, box2, box3, box4, lat, long

@app.route('/maps')
def map_view():
    response_API = requests.get('http://127.0.0.1:5001/cam_data')
    print(f'API response: {response_API.status_code}')
    data = response_API.text
    
    _,_,_,_, lat, long = process_data(data)
    # print(type(lat)
    long = long.astype(dtype='float32')
    lat = lat.astype(dtype='float32')
    long = long.tolist()
    lat = lat.tolist()
    
    return render_template('mapsView.html', lat=lat, long=long)
    

@app.route('/', methods=['GET', 'POST'])
def index():
    response_API = requests.get('http://127.0.0.1:5001/cam_data')
    print(f'API response: {response_API.status_code}')
    
    data = response_API.text
    box1, box2, box3, box4, _, _ = process_data(data)
    
    # print(box4.columns)
    
    headings = box4.columns
    data1 = box1.to_records(index=False)
    data2 = box2.to_records(index=False)
    data3 = box3.to_records(index=False)
    data4 = box4.to_records(index=False)
    
    return render_template('index.html', headings=headings, data1=data1,
                           data2=data2, data3=data3, data4=data4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
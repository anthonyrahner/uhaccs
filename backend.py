from flask import Flask, jsonify
import pandas as pd
import requests
from io import StringIO
import time
import os
from dotenv import load_dotenv
load_dotenv()
MAP_KEY = os.getenv('MAP_KEY')

app = Flask(__name__)

# Global cache variables
cached_data = None
last_fetch_time = 0
CACHE_DURATION = 10 * 60  # 10 minutes in seconds

def get_live_fires():
    global cached_data, last_fetch_time

    current_time = time.time()
    # Check if cache is still valid
    if cached_data is not None and (current_time - last_fetch_time) < CACHE_DURATION:
        return cached_data

    # Fetch new FIRMS data
    url = f'https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_NOAA20_NRT/USA_contiguous_and_Hawaii/1'
    response = requests.get(url)
    response.raise_for_status()

    # Read CSV into pandas
    df = pd.read_csv(StringIO(response.text))

    # Keep only the important fields
    df = df[['latitude', 'longitude', 'frp', 'confidence', 'acq_date', 'acq_time', 'daynight']]

    # Update cache
    cached_data = df.to_dict(orient='records')
    last_fetch_time = current_time

    return cached_data

@app.route('/api/fires')
def fires():
    data = get_live_fires()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

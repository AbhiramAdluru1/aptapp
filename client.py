import pandas as pd
import requests
import time

# Load the input CSV file
data = pd.read_csv('test.csv')

# Server URL
server_url = 'http://x22187898-apt-env.eba-bprbucmf.ap-south-1.elasticbeanstalk.com/predict'

# Send each packet of data to the server every 5 seconds
for index, row in data.iterrows():
    try:
        # Convert row to dictionary and send as JSON
        response = requests.post(server_url, json={'row': row.to_dict(), 'row_index': index})
        if response.status_code == 200:
            print(f"Network Packet {index + 1}: {response.json()['prediction']}")
        else:
            print(f"Network Packet {index + 1}: Error - {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        print(f"Network Packet {index + 1}: Exception - {str(e)}")
    time.sleep(5)

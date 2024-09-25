import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Scrape the webpage and find the file
def get_file_url():
    base_url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all table rows in the webpage
    rows = soup.find_all('tr')
    
    # Loop through the rows to find the one with the target timestamp
    target_timestamp = "2022-02-07 14:03"

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            file_name = cols[0].find('a').text
            last_modified = cols[1].text.strip()
            
            if last_modified == target_timestamp:
                print(f"File found: {file_name}")
                return base_url + file_name  # Build the full file URL

    return None

# Step 2: Download the file
def download_file(file_url):
    response = requests.get(file_url)
    file_name = file_url.split('/')[-1]

    with open(file_name, 'wb') as f:
        f.write(response.content)

    print(f"File downloaded: {file_name}")
    return file_name

# Step 3: Load CSV with Pandas and find highest HourlyDryBulbTemperature
def find_highest_temperature(file_name):
    df = pd.read_csv(file_name)
    
    # Assuming 'HourlyDryBulbTemperature' is the column name, adjust if needed
    max_temp = df['HourlyDryBulbTemperature'].max()
    max_temp_records = df[df['HourlyDryBulbTemperature'] == max_temp]

    print("Record(s) with the highest HourlyDryBulbTemperature:")
    print(max_temp_records)

def main():
    file_url = get_file_url()
    if file_url:
        file_name = download_file(file_url)
        find_highest_temperature(file_name)
    else:
        print("File not found for the specified timestamp.")

if __name__ == "__main__":
    main()
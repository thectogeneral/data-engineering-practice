import os
import requests
import zipfile
from io import BytesIO

# List of download URIs
download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",  # Invalid URL
]

# Function to download and extract zip files
def download_and_extract(uri):
    # Extract filename from URL
    filename = uri.split('/')[-1]

    try:
        print(f"Downloading {filename} ...")
        response = requests.get(uri)
        response.raise_for_status()  # Raise an error for invalid responses

        # Save zip file in memory
        zip_file = zipfile.ZipFile(BytesIO(response.content))

        # Extract all contents into the downloads folder
        zip_file.extractall("downloads")
        print(f"Extracted {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {filename}: {e}")

def main():
    # Step 1: Create the downloads directory if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Step 2: Download and extract each file
    for uri in download_uris:
        download_and_extract(uri)

if __name__ == "__main__":
    main()
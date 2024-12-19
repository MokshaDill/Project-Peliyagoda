import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the webpage containing the Excel file links
base_url = 'https://www.fisheries.gov.lk/web/index.php?option=com_content&view=article&id=42&Itemid=151&lang=en#january-2019'

# Custom download path
download_dir = r'C:\Users\moksh\OneDrive\Desktop\scrape fish data'
os.makedirs(download_dir, exist_ok=True)  # Create the folder if it doesn’t exist

# Send a GET request to the webpage
response = requests.get(base_url)
response.raise_for_status()  # Ensure the request was successful

# Parse the webpage content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links ending with '.xls' or '.xlsx'
excel_links = soup.find_all('a', href=lambda href: href and (href.endswith('.xls') or href.endswith('.xlsx')))

# Download each Excel file
for link in excel_links:
    excel_url = urljoin(base_url, link['href'])  # Get the full URL
    file_name = os.path.basename(excel_url)  # Extract the file name
    file_path = os.path.join(download_dir, file_name)  # Full path to save file

    # Skip download if the file already exists
    if os.path.exists(file_path):
        print(f'Skipping (already exists): {file_name}')
        continue

    # Download the file
    print(f'Downloading {excel_url}...')
    file_response = requests.get(excel_url)
    file_response.raise_for_status()

    # Save the file
    with open(file_path, 'wb') as file:
        file.write(file_response.content)
    print(f'Saved to {file_path}')

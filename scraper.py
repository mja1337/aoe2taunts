import requests
from bs4 import BeautifulSoup
import json

# Step 1: Fetch the webpage content
url = "https://ageofempires.fandom.com/wiki/Taunt"
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all relevant headlines and tables
headlines = soup.find_all(['h2', 'h3'])  # Find all h2 and h3 elements
tables = soup.find_all('table', class_='fandom-table')

# Check if any tables were found
if not tables:
    raise ValueError("Could not find any 'fandom-table' tables on the page.")

# Initialize a dictionary to store all taunts grouped by game versions and sub-categories
taunts_by_version = {}
current_version = ""
current_subcategory = ""

# Step 4: Iterate over each headline and corresponding table to extract taunts
for heading in headlines:
    if heading.name == 'h2' and heading.find('span', class_='mw-headline'):
        # Update the current game version when we encounter a main headline
        current_version = heading.get_text(strip=True).replace('[edit]', '').strip()
        current_subcategory = ""  # Reset subcategory when a new main category is found
        if current_version not in taunts_by_version:
            taunts_by_version[current_version] = {}

    elif heading.name == 'h3':
        # Update the current subcategory when we encounter a subheadline
        current_subcategory = heading.get_text(strip=True).replace('[edit]', '').strip()

    # Each table should correspond to the current main version and subcategory
    table_index = headlines.index(heading)
    if table_index < len(tables):
        # Ensure that a valid game version is set before processing a table
        if not current_version:
            print(f"Skipping table at index {table_index} due to missing main heading.")
            continue
        
        taunts = []
        for row in tables[table_index].find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            
            if len(columns) < 3:
                continue  # Skip rows that don't have enough columns
            
            taunt_number = columns[0].get_text(strip=True)
            taunt_description = columns[1].get_text(strip=True)
            
            # Extract the data-src URL from the audio-button class
            audio_button = columns[2].find('span', class_='audio-button')
            taunt_audio_url = ""
            if audio_button and 'data-src' in audio_button.attrs:
                taunt_audio_url = audio_button['data-src']
            
            # Only add taunt if it has a valid audio URL
            if taunt_audio_url:
                taunts.append({
                    'number': int(taunt_number),
                    'description': taunt_description,
                    'url': taunt_audio_url
                })
        
        if taunts:
            if current_subcategory:
                if current_subcategory not in taunts_by_version[current_version]:
                    taunts_by_version[current_version][current_subcategory] = taunts
                else:
                    taunts_by_version[current_version][current_subcategory].extend(taunts)
            else:
                if 'General' not in taunts_by_version[current_version]:
                    taunts_by_version[current_version]['General'] = taunts
                else:
                    taunts_by_version[current_version]['General'].extend(taunts)

# Step 5: Save the data to a JSON file
with open('aoe_taunts_by_version.json', 'w') as file:
    json.dump(taunts_by_version, file, indent=4)

print(f"Extracted taunts grouped by versions and subcategories and saved to aoe_taunts_by_version.json")

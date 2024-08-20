import pandas as pd
import json
import uuid
from datetime import datetime

# Load data from Excel
file_path = '/path/to/egage/Engage-Data-V1.0.xlsx'  # Update this path to the correct location

activities_df = pd.read_excel(file_path, sheet_name='Activities')
approaches_df = pd.read_excel(file_path, sheet_name='Approaches')
goals_df = pd.read_excel(file_path, sheet_name='Goals')
vulnerabilities_df = pd.read_excel(file_path, sheet_name='Vulnerabilities')

# Function to convert datetime to string, if it's not already a string
def datetime_to_string(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, str):
        return value  # Return the string as is
    else:
        return None  # Return None if it's neither a datetime nor a string

# Function to create elements for the galaxy
def create_elements(df, element_type):
    elements = []
    for _, row in df.iterrows():
        element = {
            "uuid": str(uuid.uuid4()),
            "value": f"{row['ID'] if 'ID' in df.columns else row['id']} - {row['name'] if 'name' in df.columns else ''}",  # Combine ID and name
            "description": row['short description'] if 'short description' in df.columns else row['description'],
            "meta": {
                "category": element_type,  # Add the category (e.g., Activity, Goal, Approach, Vulnerability)
                "long_description": row['long description'] if 'long description' in df.columns else '',
                "url": row['url'] if 'url' in df.columns else '',
                "created": datetime_to_string(row['created']),
                "last_modified": datetime_to_string(row['last modified']),
                "version": row['version'] if 'version' in df.columns else row['Version']  # Handle different versions
            }
        }
        elements.append(element)
    return elements

# Define the Galaxy structure
  "category": "engage",
  "description": "This galaxy contains all parts of the MITRE Engage framework, including Activities, Approaches, Goals, and Vulnerabilities.",
  "name": "MITRE Engage Framework",
  "source": "https://engage.mitre.org",
  "type": "mitre-engage",

galaxy = {
    "type": "mitre-engage",
    "uuid": str(uuid.uuid4()),  # Generate a unique UUID for the galaxy
    "name": "MITRE Engage Framework",
    "description": "This galaxy contains all parts of the MITRE Engage framework, including Activities, Approaches, Goals, and Vulnerabilities.",
    "source": "https://engage.mitre.org",
    "type": "mitre-engage",
    "values": []
}

# Add elements to the galaxy with appropriate categories
galaxy["values"].extend(create_elements(activities_df, 'Activity'))
galaxy["values"].extend(create_elements(approaches_df, 'Approach'))
galaxy["values"].extend(create_elements(goals_df, 'Goal'))
galaxy["values"].extend(create_elements(vulnerabilities_df, 'Vulnerability'))

# Convert the galaxy to JSON format
galaxy_json = json.dumps(galaxy, indent=4)

# Save the galaxy JSON to a file
with open('mitre_engage_framework_galaxy.json', 'w') as file:
    file.write(galaxy_json)

print("MISP Galaxy JSON has been created successfully.")

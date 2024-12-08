import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_name_list_synonyms(data, query):
    """
    Extract the name list and synonyms for a specific query from the API response.

    Args:
        data (dict): Parsed JSON response from the Cellosaurus API.
        query (str): The cell line query string.

    Returns:
        dict: A dictionary containing the identifier and its corresponding synonyms.
    """
    results = {}
    # Iterate over each cell line in the 'cell-line-list'
    for cell_line_entry in data.get('cell-line-list', []):
        # Find the identifier
        identifier = None
        synonyms = []
        for name_entry in cell_line_entry.get('name-list', []):
            if name_entry['type'] == 'identifier':
                identifier = name_entry['value']
            elif name_entry['type'] == 'synonym':
                synonyms.append(name_entry['value'])

        # Store the identifier and its synonyms if it matches the query
        if identifier.lower() == query.lower():
            results[identifier] = synonyms

    return results

def find_matching_rows(cell_lines, samples_df):
    """
    Matches rows in the samples DataFrame based on cell line names and synonyms, case-insensitively.

    Args:
        cell_lines (list): List of cell lines to query.
        samples_df (pd.DataFrame): DataFrame containing "cell_type" and "tissue" columns.

    Returns:
        pd.DataFrame: DataFrame with matched rows and an additional column for the identifier.
    """
    matched_rows = []

    # Normalize cell_lines to lowercase for case-insensitive matching
    normalized_cell_lines = [line.lower() for line in cell_lines]

    for query in normalized_cell_lines:
        url = f"https://api.cellosaurus.org/search/cell-line?q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            # Parse JSON response
            api_data = response.json()
            # Extract synonyms
            synonyms_data = extract_name_list_synonyms(api_data.get('Cellosaurus', {}), query)

            for identifier, synonyms in synonyms_data.items():
                # Combine identifier and synonyms into one list of query strings
                query_strings = [identifier.lower()] + [synonym.lower() for synonym in synonyms]

                # Match rows where cell_type contains any of the query strings (case-insensitively)
                for _, row in samples_df.iterrows():
                    if any(query_string in row['cell_type'].lower() for query_string in query_strings):
                        matched_row = row.to_dict()
                        matched_row['matched_identifier'] = identifier
                        matched_rows.append(matched_row)
        else:
            print(f"Failed to fetch data for {query}. HTTP Status Code: {response.status_code}")

    # Create a new DataFrame from the matched rows
    return pd.DataFrame(matched_rows)

# Input samples
samples_df = pd.read_csv('/Users/suryav/Downloads/screen-tsv-download.tsv', header=None, delimiter='\t')
samples_df.columns = ['cell_type','tissue']

# URL of the Protein Atlas Leukemia page
url = "https://www.proteinatlas.org/humanproteome/cell+line/leukemia"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the script tag containing the desired identifier
    script_tags = soup.find_all('script')
    for script in script_tags:
        # Look for the specific identifier in the script content
        if "var plot = $('#celline_prio_leukemia_LAML')" in script.text:
            # Extract the full line containing the scatterPlot data
            full_line = re.search(r"var plot = \$\('#celline_prio_leukemia_LAML'\)\.scatterPlot\((.*?)\);", script.text, re.DOTALL)
            # if full_line:
            full_line_text = full_line.group(1)  # Extract the full JSON-like data
            cell_lines = re.findall(r'"name":"(.*?)"', full_line_text)
            #Strip trailers
            cell_lines = [x.split(' ')[0].replace('\\','') for x in cell_lines]
            print('All Leukemia Cell Lines in Protein Atlas:',cell_lines)  
    
cell_lines = cell_lines[0:5]
cell_lines.append('jurkat e6.1')

# Find matching rows
matched_df = find_matching_rows(cell_lines, samples_df)

# Display the output DataFrame
print(matched_df)
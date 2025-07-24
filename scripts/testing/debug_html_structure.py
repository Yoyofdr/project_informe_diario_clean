#!/usr/bin/env python3
"""
Debug HTML structure to understand sections
"""

import requests
from bs4 import BeautifulSoup
import re

def debug_html_structure():
    """Debug the HTML structure for July 19"""
    fecha = "19-07-2025"
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/index.php?date={fecha}&edition=44202"
    
    print(f"Fetching: {url}")
    
    response = requests.get(url, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Save HTML for inspection
    with open('debug_july19.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print("\nHTML saved to debug_july19.html")
    
    # Look for any text containing "Norma" or section keywords
    print("\n=== Searching for section keywords ===")
    
    for text in soup.stripped_strings:
        text_upper = text.upper()
        if any(keyword in text_upper for keyword in ['NORMA', 'PARTICULAR', 'GENERAL', 'AVISO', 'DESTACADO']):
            if len(text) < 100:  # Avoid long document titles
                print(f"Found: '{text}'")
                
                # Find the parent element
                parent = None
                for elem in soup.find_all(string=text):
                    parent = elem.parent
                    break
                
                if parent:
                    print(f"  Parent tag: {parent.name}")
                    print(f"  Parent attrs: {parent.attrs}")
                    print()
    
    # Check table structure
    print("\n=== Table Structure ===")
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        print(f"\nTable {i+1}:")
        
        # Check for any row that might be a header
        all_rows = table.find_all('tr')
        for j, row in enumerate(all_rows[:10]):  # First 10 rows
            cells = row.find_all(['td', 'th'])
            if cells:
                first_cell = cells[0]
                text = first_cell.get_text(strip=True)
                
                # Check if this might be a section header
                if text and len(text) < 50:
                    bgcolor = first_cell.get('bgcolor', '')
                    colspan = first_cell.get('colspan', '')
                    class_attr = row.get('class', [])
                    
                    if bgcolor or colspan or not class_attr:
                        print(f"  Row {j+1}: '{text[:60]}...'")
                        print(f"    bgcolor: {bgcolor}, colspan: {colspan}, class: {class_attr}")

if __name__ == "__main__":
    debug_html_structure()
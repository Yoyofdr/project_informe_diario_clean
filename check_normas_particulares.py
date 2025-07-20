#!/usr/bin/env python3
"""
Check Normas Particulares section
"""

import requests
from bs4 import BeautifulSoup
import re

def check_normas_particulares(fecha, edition):
    """Check documents in Normas Particulares"""
    url = f"https://www.diariooficial.interior.gob.cl/edicionelectronica/normas_particulares.php?date={fecha}&edition={edition}"
    
    print(f"\nChecking Normas Particulares for {fecha}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Count documents
        content_rows = soup.find_all('tr', class_='content')
        pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$'))
        
        print(f"Documents found (tr.content): {len(content_rows)}")
        print(f"PDF links found: {len(pdf_links)}")
        
        # Show first few documents
        if content_rows:
            print("\nFirst few documents:")
            for i, tr in enumerate(content_rows[:5]):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    titulo = tds[0].get_text(strip=True)
                    print(f"  {i+1}. {titulo[:80]}...")
        
        return len(content_rows)
        
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Test recent dates
dates_to_check = [
    ("19-07-2025", "44202"),
    ("17-07-2025", "44200"),
    ("15-07-2025", "44199"),
    ("12-07-2025", "44197"),
]

total_missed = 0
for fecha, edition in dates_to_check:
    count = check_normas_particulares(fecha, edition)
    total_missed += count

print(f"\n=== TOTAL DOCUMENTOS EN NORMAS PARTICULARES: {total_missed} ===")
print("\nEstos documentos NO están siendo contados en el total actual!")
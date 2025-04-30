from bs4 import BeautifulSoup
import requests
import re

data = []
for num in range(1,11,1):
    res = requests.get(f'https://buyhatke.com/price-history-deals?page={num}')
    print(f'https://buyhatke.com/price-history-deals?page={num}')
    soup = BeautifulSoup(res.text, 'lxml')

    # Extracting all the anchor tags
    for a_tag in soup.find_all('a', class_='text-left'):
        href = a_tag.get('href')
      
        # Extract current price
        current_price_tag = a_tag.select_one('.font-semibold.text-base.md\\:text-lg')
        if current_price_tag and current_price_tag.sup:
        current_price_tag.sup.decompose()
        current_price = float(current_price_tag.get_text(strip=True).replace(',','') if current_price_tag else None)

        # Extract original price
        original_price_tag = a_tag.select_one('.line-through.text-gray-400.text-xs')
        if original_price_tag and original_price_tag.sup:
            original_price_tag.sup.decompose()
        original_price = float(original_price_tag.get_text(strip=True).replace(',','') if original_price_tag else None)

        # Storing items which have more than 45% off 
        if original_price>=10000 and (original_price//current_price)>=1.8:
            data.append([href, current_price, original_price])

with open ('text.txt', 'w') as file:
    file.write(str(data))

for item in data:
    link = item[0]
  

for item in data: 
    res = requests.get(item[0])
    soup = BeautifulSoup(res.text, 'lxml')


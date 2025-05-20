from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urlparse, parse_qs, unquote
from telegram import Telegram

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
        if original_price>=5000 and (original_price//current_price)>=1.8:
            data.append([href, current_price, original_price])

deals = []
# Extracting the actual web link
for item in data: 
    res = requests.get('https://buyhatke.com'+item[0])
    soup = BeautifulSoup(res.text, 'lxml')

    # Getting the final link and storing in deals
    link = soup.find('a', attrs={'aria-label': 'Buy button main card'})['href']
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)

    # Extract and decode the 'link' parameter
    raw_url = query_params.get('link', [None])[0]
    final_url = unquote(raw_url) if raw_url else None
    if 'amazon' in final_url:
        deals.append((final_url+'?tag=sumanth0bc-21', item[1], item[2]))
    else:
        deals.append((final_url, item[1], item[2]))

with open ('text.txt','w') as file:
    file.write(str(deals))


telegram_bot = Telegram()
for link, current_price, original_price in deals:
    if not link.startswith("http"):
        link = "https://" + link
    # webbrowser.open(link)
    telegram_bot.send_telegram_message(link, current_price, original_price)

import requests


class Telegram:
    def __init__(self):
        self.BOT_TOKEN = '8047092297:AAGBDKpdMTbB0bt46jK64mvnGSKsAoEz7QM'
        self.CHANNEL_USERNAME = '@DontWaitDeals'

    def send_telegram_message(self, link, current_price, original_price):
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"

        def escape(text):
            for ch in r'_*[]()~`>#+-=|{}.!':
                text = text.replace(ch, f'\\{ch}')
            return text
        
        message = f"{escape(link)}\n" \
                  f"Original price: *~{escape(str(original_price))}~*\n" \
                  f"Current price: *{escape(str(current_price))}*"
                  
        payload = {
            'chat_id': self.CHANNEL_USERNAME,
            'text': message,
            'parse_mode': 'MarkdownV2',  # or 'HTML' if you prefer HTML formatting
            'disable_web_page_preview': False  # set to True if you don't want link previews
        }

        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.text}")

# # Example message with an affiliate link
# message_text = """🔥 Check out this amazing deal:
# [Buy Now](https://your-affiliate-link.com) and get 20% off!"""

# send_telegram_message(message_text)

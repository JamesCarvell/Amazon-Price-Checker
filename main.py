from bs4 import BeautifulSoup
import requests
import smtplib
import personal_data

URL = "https://www.amazon.ca/Huggies-Overnites-Nighttime-Baby-Diapers/dp/B09VY6TR27/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
}
TARGET_PRICE = 20.00

# Get HTML page of Amazon item
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")
price_string = soup.find(id="sns-base-price").getText().split()[0]
price_float = float(price_string[1:])

if TARGET_PRICE >= price_float:
    with smtplib.SMTP(personal_data.MY_SMTP, port=personal_data.MY_PORT) as connection:
        connection.starttls()
        connection.login(user=personal_data.MY_FROM_EMAIL, password=personal_data.MY_PASSWORD)
        connection.sendmail(
            from_addr=personal_data.MY_FROM_EMAIL,
            to_addrs=personal_data.MY_TO_EMAIL,
            msg=f"Subject:Amazon Savings!\n\nThe Amazon item you're tracking @ {URL} has fallen below ${TARGET_PRICE}!"
        )

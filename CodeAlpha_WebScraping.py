import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # for cleaning price

# 🔹 Base URL of the website
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# 🔹 Headers to avoid being blocked
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 🔹 Conversion rate from GBP (£) to INR (₹)
CONVERSION_RATE = 105  # Example: 1 £ = 105 ₹

all_books = []

# 🔹 Function to get numeric rating from class
def get_rating(star_tag):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for cls in star_tag["class"]:
        if cls in ratings:
            return ratings[cls]
    return None

# 🔹 Loop through first 5 pages
for page in range(1, 6):
    print(f"Scraping Page {page}...")
    
    response = requests.get(BASE_URL.format(page), headers=HEADERS)
    response.encoding = 'utf-8'  # 🔹 Fix encoding issue
    
    if response.status_code != 200:
        print("Failed to fetch page")
        continue
    
    soup = BeautifulSoup(response.text, "lxml")
    books = soup.select(".product_pod")
    
    for book in books:
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").text.strip()
        
        # 🔹 Clean price text to remove any unwanted characters
        price_clean = re.sub(r"[^\d.]", "", price_text)
        price_inr = round(float(price_clean) * CONVERSION_RATE, 2)
        
        availability = book.select_one(".availability").text.strip()
        rating = get_rating(book.select_one(".star-rating"))
        link = book.h3.a["href"]
        
        book_data = {
            "Book Name": title,
            "Price (₹)": price_inr,
            "Rating (Stars)": rating,
            "Availability": availability,
            "Product Link": f"https://books.toscrape.com/catalogue/{link}"
        }
        
        all_books.append(book_data)
        
        # 🔹 Print in box format
        print("📚 Book Name    :", title)
        print("💰 Price       : ₹", price_inr)
        print("⭐ Rating      :", rating)
        print("📦 Availability:", availability)
        print("🔗 Link        :", f"https://books.toscrape.com/catalogue/{link}")
        print("="*60)
    
    time.sleep(1)  # Respect website

# 🔹 Convert all books to DataFrame
df = pd.DataFrame(all_books)

# 🔹 Save dataset to CSV
df.to_csv("books_dataset_inr.csv", index=False)

print("\n✅ Scraping Completed! Dataset saved as 'books_dataset_inr.csv'")

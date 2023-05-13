from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time

app = Flask(__name__, template_folder="./template")

def search_google_shopping(keyword: str, min_price: float):
    encoded_keyword = quote(keyword.encode('utf-8'))
    url = f"https://www.google.com/search?q={encoded_keyword}&tbm=shop&sxsrf=APwXEded34P6_oY3gHhglQec1dAjf0ve7Q:1683933969627&tbs=mr:1,price:1,ppr_min:{min_price},p_ord:p"

    options = Options()
    options.add_argument("--lang=en")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)  # Sayfanın tam olarak yüklenmesini beklemek için bir bekleme süresi ekleyin

    product_names = driver.find_elements(By.CSS_SELECTOR, "div.aULzUe")
    product_prices = driver.find_elements(By.CSS_SELECTOR, "span.kHxwFf")
    product_urls = driver.find_elements(By.CSS_SELECTOR, "a.shntl")

    products = []
    for i in range(min(20, len(product_names))):  # İlk 10 ürünü almak için döngüyü 10 kez veya ürün adedi kadar çalıştırın
        product_name = product_names[i].text
        product_price = product_prices[i].text
        product_url = product_urls[i].get_attribute("href")

        products.append({
            "product_name": product_name,
            "product_price": product_price,
            "product_url": product_url
        })

    driver.quit()
    return products

@app.route('/', methods=['GET', 'POST'])
def search_google_shopping_web():
    if request.method == 'POST':
        keyword = request.form.get('product_name')
        min_price = float(request.form.get('min_price'))
        products = search_google_shopping(keyword, min_price)
        return render_template('results.html', products=products)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

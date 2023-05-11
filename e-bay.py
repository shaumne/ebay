import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import re
from fuzzywuzzy import fuzz
import webbrowser

def get_ebay(input: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ebay.com/")

    search = driver.find_element(By.XPATH, "//input[@placeholder='Search for anything']")
    search.send_keys(input.lower())
    search.submit()

    driver.find_element(By.XPATH, "/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/button/span").click()
    driver.find_element(By.XPATH, "/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/span/ul/li[4]/a/span").click()

    titles = driver.find_elements(By.XPATH, "//span[@role='heading']")
    prices = driver.find_elements(By.XPATH, "//span[@class='s-item__price']")
    urls = driver.find_elements(By.XPATH, "//a[@class='s-item__link']")

    results = []
    for i in range(10):
        product_name = titles[i].text
        match = re.search(r'[0-9\.]+', prices[i].text)
        if match is None:
            continue
        product_price = float(match.group())
        product_url = urls[i].get_attribute('href')

        similarity = fuzz.token_set_ratio(input.lower(), product_name.lower())
        results.append((product_name, product_price, product_url, similarity))

    results.sort(key=lambda x: x[1])  # sort by price

    driver.quit()
    return results

def open_url(url):
    webbrowser.open(url)

def submit():
    product_name = entry.get().strip().lower()
    
    button.config(state="disabled")
    
    for i in table.get_children():
        table.delete(i)
    table.insert("", "end", values=("Please wait for the results...", "", "", ""))
    
    threading.Thread(target=search_ebay, args=(product_name,), daemon=True).start()

def search_ebay(product_name):
    results = get_ebay(product_name)

    for i in table.get_children():
        table.delete(i)

    min_price = float("inf")
    min_price_index = -1
    for i, (name, price, url, _) in enumerate(results, start=1):
        table.insert("", "end", values=(i, name, price, url))
        if price < min_price:
            min_price = price
            min_price_index = i

    if min_price_index != -1:
        table.tag_configure("highlight", background="yellow")
        table.tag_add("highlight", min_price_index-1)

root = tk.Tk()
root.title("eBay Lowest Price Finder")

frame1 = ttk.Frame(root)
frame1.pack()

label = ttk.Label(frame1, text="Product Name:")
label.pack(side="left")

entry = ttk.Entry(frame1)
entry.pack(side="left")

button = ttk.Button(frame1, text="Submit", command=submit)
button.pack(side="left")

frame2 = ttk.Frame(root)
frame2.pack()

table = ttk.Treeview(frame2, columns=("No", "Product Name", "Price", "URL"), show="headings")
table.heading("No", text="No")
table.heading("Product Name", text="Product Name")
table.heading("Price", text="Price")
table.heading("URL", text="URL")
table.pack()

table.bind("<Double-Button-1>", lambda event: open_url(table.item(table.selection())["values"][3]))

root.mainloop()


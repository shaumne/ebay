# eBay Lowest Price Finder
This Python script retrieves the 10 lowest-priced products on eBay based on a user-entered product name and displays them in a graphical user interface (GUI).

### Installation
To run this script, you need to install some dependencies. Make sure you have Python 3.6 or higher installed. You can use pip to install the required Python packages:
`pip install -r requirements.txt`

This script uses the Selenium WebDriver to perform automated actions in a web browser. You'll need an appropriate browser driver installed on your system to use WebDriver. This script is designed for the Google Chrome browser, so you'll need to download and install ChromeDriver on your system.

### Usage
When you run the script, a GUI window will open. Enter the name of the product you want to search for in the "Product Name" field and click the "Submit" button. The script will perform a search on eBay for the specified product and retrieve the 10 lowest-priced products. These products will be displayed in a table along with their names, prices, and URLs.

When you double-click on a URL in the table, the corresponding eBay page will open in your default web browser.
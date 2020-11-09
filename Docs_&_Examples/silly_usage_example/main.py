# Import necessary libraries
from goodreadsscraper import GoodReadsScraper
from selenium.webdriver.chrome.options import Options

# Set chrome driver options to replace GoodReadsScraper defaults
chrome_options = Options()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless")  # Uncomment to activate headless mode
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--disable-gpu') # Uncomment this line if running windows
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(
    "--blink-settings=imagesEnabled=false"
)  # Do not load images

# What follows is an usage example of GoodReadsScraper on a small 9 books list (aprox. 2 min. total run)
list_url = 'https://www.goodreads.com/list/show/131644.CBC_Canada_Reads_2019_Longlist'

if __name__ == '__main__':
    CBC2019_scraper = GoodReadsScraper(list_url, chrome_options)
    CBC2019_scraper.get_book_links()  # Scrape book URLs from list
    CBC2019_scraper.get_books()  # Scrape book information
    CBC2019_scraper.get_books_cover()  # Download books cover images
    CBC2019_scraper.get_books_price()  # Get book price from IberLibro store
    CBC2019_scraper.get_books_kindle_price()  # Get ebook price from Amazon Kindle store

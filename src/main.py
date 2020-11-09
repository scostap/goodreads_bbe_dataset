# Import necessary libraries
from goodreadsscraper import GoodReadsScraper
from selenium.webdriver.chrome.options import Options

# Set chrome driver options to replace GoodReadsScraper defaults
chrome_options = Options()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless") # Uncomment to activate
# chrome_options.add_argument('--disable-gpu') # Uncomment this line if running headless on windows
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(
    "--blink-settings=imagesEnabled=false"
)  # Do not load images

# What follows is the code used to created the BBE dataset published on Zenodo.
list_url = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'

if __name__ == '__main__':
    BBE_scraper = GoodReadsScraper(list_url, chrome_options)
    BBE_scraper.get_book_links()  # Scrape book URLs from GoodReads list
    BBE_scraper.get_books()  # Scrape book information
    BBE_scraper.get_books_cover()  # Download books cover images
    BBE_scraper.get_books_price()  # Get book price from IberLibro store
#   BBE_scraper.get_books_kindle_price()  # Not run on published BBE dataset


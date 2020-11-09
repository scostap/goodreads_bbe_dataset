# Import necessary libraries.
import os
import csv
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define default chrome driver options for GoodReadsScraper.
chrome_options = Options()
chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless") # Uncomment to run
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--disable-gpu') # Uncomment this line if running windows
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument(
    "--blink-settings=imagesEnabled=false"
)  # Do not load images


class GoodReadsScraper:
    """
    This is a class for scraping book information on a GoodReads (GR) list.

    Attributes:
        driver (WebDriver): The WebDriver used by selenium, will be initialized only when needed.
        book_links (list of dict): The list containing book urls, votes and scores taken from GR list.
        books (list of dict): The list of dictionarys containing book information scraped.
        broken (list of dict): The list of broken links in GR, useful to retry scraping.
        list_url (string): The URL of the target GR list to be scraped.
        chrome_options (Options): The driver options to be used by the WebDriver, including headless modes.
        robots_disallow (list of string): The list of URL disallowed in GR robots.txt
    """

    def __init__(self, list_url, driver_options=chrome_options):
        """
        The constructor for GoodReadsScraper class.

        :param list_url: The URL of the target GR list to be scraped.
        :param driver_options: The driver options to replace defaults (optional).
        """
        self.driver = ""
        self.book_links = []
        self.books = []
        self.broken = []
        self.list_url = list_url
        self.chrome_options = driver_options
        self.robots_disallow = self.__get_robots_disallow()

    # Define methods to scrape book information.
    def __get_book_id(self, string):
        book_id = string.split("/")[-1]
        return book_id

    def __get_title(self):
        title = self.driver.find_element_by_id("bookTitle").text
        return title

    def __get_series(self):
        series = self.driver.find_element_by_id("bookSeries").text.strip("()")
        return series

    def __get_author(self):
        author = self.driver.find_element_by_id("bookAuthors").text.replace("by ", "")
        return author

    def __get_rating(self):
        rating = str(
            self.driver.find_element_by_xpath('//span[@itemprop="ratingValue"]').text
        )
        return rating

    def __get_description(self):
        if (
            len(self.driver.find_elements_by_xpath('//*[(@id = "description")]//span'))
            > 1
        ):
            description = self.driver.find_elements_by_xpath(
                '//*[(@id = "description")]//span'
            )[1].get_attribute("innerText")
        elif (
            len(self.driver.find_elements_by_xpath('//*[(@id = "description")]//span'))
            == 1
        ):
            description = self.driver.find_elements_by_xpath(
                '//*[(@id = "description")]//span'
            )[0].get_attribute("innerText")
        else:
            description = ""
        return description

    def __get_language(self):
        try:
            language = self.driver.find_element_by_xpath(
                '//*[@itemprop="inLanguage"]'
            ).get_attribute("innerText")
        except NoSuchElementException:
            language = ""
        return language

    def __get_isbn(self):
        if len(self.driver.find_elements_by_xpath('//*[@itemprop="isbn"]')) != 0:
            isbn = self.driver.find_element_by_xpath(
                '//*[@itemprop="isbn"]'
            ).get_attribute("innerText")
        else:
            # When isbn is not informed
            isbn = "9999999999999"
        return isbn

    def __get_genres(self):
        genres = []
        for e in self.driver.find_elements_by_class_name("elementList"):
            try:
                genres.append(e.find_element(By.CLASS_NAME, "left").text)
            except NoSuchElementException:
                pass
        genres = [x.split(" > ")[1] if ">" in x else x for x in genres]
        return genres

    def __get_book_format(self):
        try:
            book_format = self.driver.find_element_by_xpath(
                '//*[@itemprop="bookFormat"]'
            ).get_attribute("innerText")
        except NoSuchElementException:
            book_format = ""
        return book_format

    def __get_edition(self):
        try:
            edition = self.driver.find_element_by_xpath(
                '//*[@itemprop="bookEdition"]'
            ).get_attribute("innerText")
        except NoSuchElementException:
            edition = ""
        return edition

    def __get_pages(self):
        try:
            pages = (
                self.driver.find_element_by_xpath('//*[@itemprop="numberOfPages"]')
                .get_attribute("innerText")
                .replace(" pages", "")
            )
        except NoSuchElementException:
            pages = ""
        return pages

    def __get_characters(self):
        characters = []
        for e in self.driver.find_elements_by_xpath(
            '//a[contains(@href, "/characters/")]'
        ):
            characters.append(e.get_attribute("innerText"))
        return characters

    def __get_publisher(self):
        try:
            element = (
                self.driver.find_element_by_xpath('(//div[@class="row"])[2]')
                .get_attribute("innerText")
                .split(" by ")
            )
            if len(element) == 2:
                publisher = element[1].split(" (f")[0]
            else:
                publisher = ""
        except NoSuchElementException:
            publisher = ""
        return publisher

    def __get_publish_date(self):
        try:
            element = (
                self.driver.find_element_by_xpath('(//div[@class="row"])[2]')
                .get_attribute("innerText")
                .split(" by ")
            )
            if len(element) == 2:
                publish_date = element[0].replace("Published ", "")
            else:
                publish_date = element[0].split("(")[0].replace("Published ", "")
        except NoSuchElementException:
            publish_date = ""
        return publish_date

    def __get_first_publish_date(self):
        try:
            publish_date = (
                self.driver.find_element_by_xpath('//div[@class="row"]/nobr')
                .get_attribute("innerText")
                .split("shed ")[1]
                .strip(")")
            )
        except NoSuchElementException:
            publish_date = ""
        return publish_date

    def __get_awards(self):
        awards = []
        for i in self.driver.find_elements_by_class_name("award"):
            awards.append(i.get_attribute("innerText"))
        return awards

    def __get_num_reviews(self):
        try:
            num_reviews = self.driver.find_element_by_xpath(
                '//meta[@itemprop="reviewCount"]'
            ).get_attribute("content")
        except NoSuchElementException:
            num_reviews = ""
        return num_reviews

    def __get_num_ratings(self):
        try:
            num_ratings = self.driver.find_element_by_xpath(
                '//meta[@itemprop="ratingCount"]'
            ).get_attribute("content")
        except NoSuchElementException:
            num_ratings = ""
        return num_ratings

    def __get_ratings_by_stars(self):
        try:
            ratings_by_stars = (
                self.driver.find_element_by_xpath(
                    '//script[@type="text/javascript+protovis"]'
                )
                .get_attribute("innerText")
                .split("[")[1]
                .split("]")[0]
                .split(", ")
            )
            ratings_by_stars = [int(r) for r in ratings_by_stars]
        except NoSuchElementException:
            ratings_by_stars = []
        return ratings_by_stars

    def __get_setting(self):
        setting = []
        for e in self.driver.find_elements_by_xpath('//a[contains(@href, "/places/")]'):
            if (
                e.find_element_by_xpath("following-sibling::*").get_attribute(
                    "innerText"
                )
                != ""
            ):
                setting.append(
                    e.get_attribute("innerText")
                    + " "
                    + e.find_element_by_xpath("following-sibling::*").get_attribute(
                        "innerText"
                    )
                )
            else:
                setting.append(e.get_attribute("text"))
        setting = [x.replace("\n", "") for x in setting]
        return setting

    def __get_cover_img_url(self):
        try:
            cover_img_url = self.driver.find_element_by_xpath(
                '//img[@id="coverImage"]'
            ).get_attribute("src")
        except NoSuchElementException:
            cover_img_url = ""
        return cover_img_url

    def __get_price(self, isbn):
        # Navigate to bookstore IberLibro and search by isbn
        self.driver.get("https://www.iberlibro.com/")
        box = self.driver.find_elements_by_xpath('//input[@class="form-control"]')
        box[3].click()
        box[3].send_keys(isbn)
        self.driver.find_element_by_xpath(
            '//button[@class="btn btn-abebooks btn-xs-block"]'
        ).click()

        # Wait for price to load to avoid crash
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element_by_class_name("srp-item-price")
            )
            price = (
                self.driver.find_element_by_class_name("srp-item-price")
                .text.split(" ")[1]
                .replace(",", ".")
            )
        except (NoSuchElementException, TimeoutException):
            price = ""
        return price

    def __get_kindle_price(self, title, author):
        # Navigate to bookstore and wait for complete load
        self.driver.get(
            "https://www.amazon.es/kindle-store-ebooks/b?ie=UTF8&node=818936031"
        )

        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element_by_id("twotabsearchtextbox")
            ).click()

            # Enter the title and author
            search = self.driver.find_element_by_xpath('//input[@class="nav-input"]')
            search.send_keys(title + " " + author)
            self.driver.find_element_by_xpath('//span[@aria-label="Ir"]').click()

            # Wait for price to load to avoid crash
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.find_element_by_class_name("a-price-whole")
            )

            # Retrieve price
            kindle_price = self.driver.find_element_by_class_name(
                "a-price-whole"
            ).text.replace(",", ".")
        except (NoSuchElementException, TimeoutException):
            kindle_price = ""
        return kindle_price

    def __get_robots_disallow(self):
        # Initialize driver
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # Get dissallowed urls from robots.txt
        try:
            self.driver.get("https://www.goodreads.com/robots.txt")
            robots_disallow = self.driver.find_element_by_xpath("//body").text.split(
                "\n"
            )
            robots_disallow = [
                line.replace("Disallow: ", "")
                for line in robots_disallow
                if "Disallow" in line
            ]
        except NoSuchElementException:
            robots_disallow = ""

        self.driver.close()
        return robots_disallow

    def __rem_disallowed_links(self):
        clean_list = []
        for link in self.book_links:
            if (
                link.get("bookUrl")
                .split(".com")[1]
                .split(".")[0]
                .split("_")[0]
                .split("-")[0]
                not in self.robots_disallow
            ):
                clean_list.append(link)
        return clean_list

    # Define methods to read from and write to csv
    def links_to_csv(self, file):
        """
        Saves scraped book links list (book_links) to csv file.
        :param file: The filename to be used.
        :returns: None
        """
        # Get headers
        keys = self.book_links[0].keys()

        # Write output
        with open(file, "w") as f:
            csv_writer = csv.DictWriter(f, keys, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(self.book_links)

    def csv_to_links(self, file):
        """
        Loads list books URLs, votes and scores previously exported by links_to_csv to book_links attribute.
        :param file: The file to be loaded.
        :returns: None
        """
        self.book_links = []
        # Read file
        with open(file, "rt") as f:
            csv_reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in csv_reader:
                self.book_links.append(row)

    def books_to_csv(self, file):
        """
        Saves the information of all books scrapped (books class attribute) to csv.
        :param file: The filename to be used.
        :returns: None
        """
        # Get headers
        keys = self.books[0].keys()

        # Write output
        with open(file, "w") as f:
            csv_writer = csv.DictWriter(f, keys, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(self.books)

    def csv_to_books(self, file):
        """
        Loads a csv containing previously scrapped books (to books class attribute).
        :param file: The file to be loaded.
        :returns: None
        """
        self.books = []
        # Read file
        with open(file, "rt") as f:
            csv_reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in csv_reader:
                self.books.append(row)

    # Define list link scraper method.
    def get_book_links(self):
        """
        Retrieves each book URL, votes and score from the given GoodReads list (list_url).
        :return: None
        """
        # Time control
        start_time = time.time()

        # Initialize driver
        driver = webdriver.Chrome(options=self.chrome_options)

        # Get list number of pages:
        driver.get(str(self.list_url))
        pages = driver.find_elements_by_xpath(
            '//div[@class="pagination"]//a[contains(@href, "/list/show")]'
        )
        if len(pages) != 0:
            pages = int(pages[-2].text)
        else:
            pages = 1

        # Get book URL, scores and votes
        for page in range(1, pages + 1):

            if page % 10 == 0:
                print("Retrieving links on page " + str(page))

            # Open target site
            if page != 1:
                driver.get(str(self.list_url) + "?page=" + str(page))

            # Wait for login popup and close (will open on second page)
            if page == 2:
                try:
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '(//img[@alt="Dismiss"])[2]')
                        )
                    ).click()
                except TimeoutException:
                    pass

            # Retrieve desired elements (ordered list of books)
            book_titles = driver.find_elements_by_class_name("bookTitle")
            score_votes = driver.find_elements_by_xpath(
                '//span[@class="smallText uitext"]'
            )

            # Extract book URL, score and votes for each element
            for i in range(len(book_titles)):
                votes = (
                    score_votes[i]
                    .find_elements_by_tag_name("a")[1]
                    .get_attribute("text")
                    .split(" p")[0]
                    .replace(",", "")
                )

                # Do not retrieve books with less than 1 vote
                if int(votes) > 0:
                    book_info = {
                        "bookUrl": book_titles[i].get_attribute("href"),
                        "score": score_votes[i]
                        .find_elements_by_tag_name("a")[0]
                        .get_attribute("text")
                        .split(": ")[1]
                        .replace(",", ""),
                        "votes": votes,
                    }
                    self.book_links.append(book_info)
                else:
                    break

        # Save links to file
        self.links_to_csv("links_" + str(self.list_url.split("/")[-1]) + ".csv")

        # Time control
        end_time = time.time()
        print("--- %s seconds ---" % (round(end_time - start_time, 2)))

        # Close driver
        driver.close()

    # Define method to scrape books
    def get_books(self, start_=0, end_=0):
        """
        Retrives information of each book on the given GoodReads list.
        :param start_: Position on book_links list to start scraping (useful after crashed) using 0 indexing.
        :param end_: Position on book_links list to stop scraping.
        :return: None
        """
        # Time control
        start_time = time.time()

        # Do not scrape books on robots_disallow:
        self.book_links = self.__rem_disallowed_links()

        # Do not try to scrape more books than links
        if end_ > len(self.book_links) or end_ == 0:
            end_ = len(self.book_links)

        # Initialize driver
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # Iterate over link list
        for i in range(start_, end_):
            # Navigate to book url
            self.driver.get(self.book_links[i].get("bookUrl"))

            # Print some progress
            if i % 500 == 0:
                print(i)
            elif i % 100 == 0:
                print(
                    " " + str(int((i - start_) * 100 / (end_ - start_))) + "% ", end=""
                )
            elif i % 10 == 0:
                print(".", end="")

            # Wait for login popup and close (will open on second page)
            if i == start_ + 1:
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '(//img[@alt="Dismiss"])[2]')
                        )
                    ).click()
                except TimeoutException:
                    pass

            # Skip broken pages
            if (
                self.driver.find_element_by_xpath("//head").get_attribute("innerText")
                == ""
            ):
                print("#", end="")
                self.broken.append(self.book_links[i].get)
                continue

            # Avoid common 502/504 crashes. Book title is always present, if not found an error occurred,
            # so retry and if no response, save and exit.
            for attempt in range(10):
                try:
                    title = self.__get_title()
                except NoSuchElementException:
                    print("\n ooops, try: " + str(i))
                    time.sleep(20 + attempt ** 2 * 20)
                else:
                    break
            else:
                print("Cannot finish scraping, saving progress.")
                self.books_to_csv("books_" + str(start_) + "_" + str(i - 1) + ".csv")
                self.links_to_csv("broken_links_" + str(i - 1) + ".csv")

            # Calculate derived attributes
            ratings_by_stars = self.__get_ratings_by_stars()
            num_ratings = sum(ratings_by_stars)
            if num_ratings > 0:
                liked_percent = int(
                    round(sum(ratings_by_stars[0:3]) * 100 / num_ratings, 0)
                )
            else:
                liked_percent = ""

            # Create book entry
            book = {
                "bookId": self.__get_book_id(self.book_links[i].get("bookUrl")),
                "title": title,
                "series": self.__get_series(),
                "author": self.__get_author(),
                "rating": self.__get_rating(),
                "description": self.__get_description(),
                "language": self.__get_language(),
                "isbn": self.__get_isbn(),
                "genres": self.__get_genres(),
                "characters": self.__get_characters(),
                "bookFormat": self.__get_book_format(),
                "edition": self.__get_edition(),
                "pages": self.__get_pages(),
                "publisher": self.__get_publisher(),
                "publishDate": self.__get_publish_date(),
                "firstPublishDate": self.__get_first_publish_date(),
                "awards": self.__get_awards(),
                "numRatings": self.__get_num_ratings(),
                "ratingsByStars": ratings_by_stars,
                "likedPercent": liked_percent,
                "setting": self.__get_setting(),
                "coverImg": self.__get_cover_img_url(),
                "bbeScore": self.book_links[i].get("score"),
                "bbeVotes": self.book_links[i].get("votes"),
            }
            self.books.append(book)

            # Partial save
            if i % 250 == 0:
                self.books_to_csv(
                    "partial_book_scrape_" + str(start_) + "_" + str(end_) + ".csv"
                )
                self.links_to_csv(
                    "partial_broken_links_" + str(start_) + "_" + str(end_) + ".csv"
                )

        # Save scraped books to file
        self.books_to_csv(
            "books_"
            + str(self.list_url.split("/")[-1])
            + "_"
            + str(start_)
            + "_"
            + str(end_)
            + ".csv"
        )
        if len(self.broken) != 0:
            self.links_to_csv(
                "broken_links_"
                + str(self.list_url.split("/")[-1])
                + "_"
                + str(start_)
                + "_"
                + str(end_)
                + ".csv"
            )

        # Delete partial save and empty files
        os.remove("partial_book_scrape_" + str(start_) + "_" + str(end_) + ".csv")
        os.remove("partial_broken_links_" + str(start_) + "_" + str(end_) + ".csv")

        # Time control
        end_time = time.time()
        print("--- %s seconds ---" % (round(end_time - start_time, 2)))

        self.driver.close()

    # Define method to get book prices
    def get_books_price(self):
        """
        Retrieves book price from IberLibro store.

        Will update existing books class attribute, so a GoodReads list should be scraped or a books list loaded
        (csv_to_books) before use.
        :return: None
        """
        # Time control
        start_time = time.time()

        # Initialize driver
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # Get price for each book on books
        for i in range(len(self.books)):
            isbn = self.books[i]["isbn"]  # Take ISBN from Goodreads books record

            # Print some progress
            if i % 100 == 0:
                print("Getting price #" + str(i))
            elif i % 10 == 0:
                print(".", end="")

            # Skip missing isbn
            if isbn != "9999999999999":
                # Skip if price already present
                if "price" not in self.books[i].keys():
                    self.books[i]["price"] = self.__get_price(isbn)

        # Save updated books to file
        self.books_to_csv("books_" + str(self.list_url.split("/")[-1]) + "_price.csv")

        # Time control
        end_time = time.time()
        print("--- %s seconds ---" % (round(end_time - start_time, 2)))

        self.driver.close()

    def get_books_kindle_price(self):
        """
        Retrieves Kindle ebook price from Amazon store.

        Will update existing books class attribute, so a GoodReads list should be scraped or a books list loaded
        (csv_to_books) before use.
        :return: None
        """
        # Time control
        start_time = time.time()

        # Initialize driver
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # Get price for each book on books
        for i in range(len(self.books)):
            author = self.books[i]["author"]
            title = self.books[i]["title"]

            # Print some progress
            if i % 100 == 0:
                print("Getting kindle price #" + str(i))
            elif i % 10 == 0:
                print(".", end="")

            # Skip if price already present
            if "kindle_price" not in self.books[i].keys():
                self.books[i]["kindle_price"] = self.__get_kindle_price(title, author)

        # Save updated books to file
        self.books_to_csv(
            "books_" + str(self.list_url.split("/")[-1]) + "_kindlePrice.csv"
        )

        # Time control
        end_time = time.time()
        print("--- %s seconds ---" % (round(end_time - start_time, 2)))

        self.driver.close()

    def get_books_cover(self):
        """
        Retrieves books covers to a img/ directory

        Will work on existing books class attribute, so a GoodReads list should be scraped or a books list loaded
        (csv_to_books) before use.
        :return: None
        """
        img_dir = "img"
        check_folder = os.path.isdir(img_dir)

        # If folder doesn't exist, then create it.
        if not check_folder:
            os.makedirs(img_dir)
            print("Creating folder: ", img_dir)

        else:
            print(img_dir, "folder already exists, saving images to folder.")

        # Download covers
        for book in self.books:
            if book.get("coverImg") != "":
                urllib.request.urlretrieve(
                    book.get("coverImg"), "img/" + book.get("bookId") + ".jpg"
                )
                # Set a respectful wait time
                time.sleep(2)

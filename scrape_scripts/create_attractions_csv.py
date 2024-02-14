import requests
from bs4 import BeautifulSoup
import asyncio
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


# =============================================================
# - Data provided has:
#       -> destination:    Netherlands, Noord-Holand, Amsterdam
#       -> dates:          10 Jan - 25 Jan (Wen - Thu)
#       -> people:         1 adult
# =============================================================

# url of most popular attractions
url = "https://www.booking.com/attractions/searchresults/nl/amsterdam.html?aid=397594&label=gog235jc-1DCAEoggI46AdICVgDaFCIAQGYAQm4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ArDuuaEGwAIB0gIkZmJhYjE4YzAtNDdhMy00MmY1LTk2NWItN2UzOTgyNTk1OWEx2AIE4AIB&start_date=2024-01-10&end_date=2024-01-25&source=search_box&sort_by=attr_book_score&lang=en-us&soz=1&lang_changed=1"
# Define the Chrome webdriver options
options = webdriver.ChromeOptions()
options.add_argument(
    "--headless"
)  # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver
# driver = Chrome(options=options)
driver = Chrome()
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)
driver.maximize_window()


driver.get(url)
time.sleep(20)


# after getting the page we need to click on the show more button to see additional attractions
# <button type="button" class="a83ed08757 c21c56c305 bf0537ecb5 f671049264 d2529514af af7297d90d">
#       <span class="e4adce92df">Show more</span>
# </button>
def scroll_to_bottom_of_page():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


scroll_to_bottom_of_page()
time.sleep(5)
# /html/body/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/button
buttons = driver.find_elements(
    By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/button"
)
if buttons:
    buttons[0].click()
else:
    raise IndexError
time.sleep(20)
# scroll_to_bottom_of_page()
# time.sleep(10)

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find <a> tag with specific attributes
attractions = soup.findAll("a", {"data-testid": "card"})

# Loop over the hotel elements and extract the desired data
attractions_data = []
for attraction in attractions:
    name_element = attraction.find("h4", {"data-testid": "card-title"})
    name = name_element.text.strip()

    # obviously still amsterdam
    location_element = attraction.find("div", {"class": "css-1utx3w7"})
    location = location_element.text.strip()

    description_element = attraction.find("div", {"class": "css-6k49yo"})
    if description_element:
        description = description_element.text.strip()
    else:
        description = None

    stars_element = attraction.find("span", {"class": "a53cbfa6de css-35ezg3"})
    if stars_element:
        stars = stars_element.text.strip()
    else:
        stars = None

    rating_element = attraction.findAll("span", {"class": "a53cbfa6de"})
    booking_user_ratings = None
    num_external_reviews = None
    if len(rating_element) >= 2:
        booking_user_ratings = rating_element[1].text.strip()
        if len(rating_element) == 3:
            num_external_reviews = rating_element[2].text.strip()

    has_free_cancelation_element = attraction.find(
        "div", {"class": "a53cbfa6de d068504c75 css-j786b1"}
    )
    if has_free_cancelation_element:
        has_free_cancelation = True
    else:
        has_free_cancelation = False

    duration_element = attraction.find("div", {"class": "a53cbfa6de css-j786b1"})
    if duration_element:
        duration = duration_element.text.strip()
    else:
        duration = None

    is_bestseller_element = attraction.find("span", {"class": "b30f8eb2d6"})
    if is_bestseller_element:
        is_bestseller = True
    else:
        is_bestseller = False

    price_element = attraction.find("div", {"class": "e1eebb6a1e css-13pzcpe"})
    price = price_element.text.strip()

    attractions_data.append(
        {
            "name": name,
            "location": location,
            "description": description,
            "stars": stars,
            "booking_user_ratings": booking_user_ratings,
            "num_external_reviews": num_external_reviews,
            "has_free_cancelation": has_free_cancelation,
            "duration": duration,
            "is_bestseller": is_bestseller,
            "price": price,
        }
    )

hotels = pd.DataFrame(attractions_data)
print(hotels.head)
hotels.to_csv("data/attractions.csv", header=True, index=False)

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def construct_dates():
    start_date = datetime(2024, 2, 1)  # year month day
    end_date = datetime(2025, 1, 31)

    date_range_list = []

    current_date = start_date
    while current_date <= end_date:
        start_date_str = current_date.strftime("%Y-%m-%d")
        next_day = current_date + timedelta(days=1)
        next_day_str = next_day.strftime("%Y-%m-%d")

        date_range_list.append([start_date_str, next_day_str])
        current_date += timedelta(days=1)

    print(date_range_list[:5])
    return date_range_list


def get_hotels(hotels, date):
    hotels_per_page = []
    for hotel in hotels:
        name_element = hotel.find("div", {"data-testid": "title"})
        name = name_element.text.strip()

        location_element = hotel.find("span", {"data-testid": "address"})
        location = location_element.text.strip()

        price_element = hotel.find(
            "span", {"data-testid": "price-and-discounted-price"}
        )
        if price_element:
            price = price_element.text.strip()
        else:
            raise Exception

        rating_stars_element = hotel.find("div", {"data-testid": "rating-stars"})
        if rating_stars_element:
            stars = len(rating_stars_element.find_all("span"))
        else:
            stars = None

        distance_from_center_element = hotel.find("span", {"data-testid": "distance"})
        distance_from_center = distance_from_center_element.text.strip()

        # here we have both how many reviews we have from the users and the avg score 1-10
        # the score is also classified by booking (Wonderful, Very Good, Good, etc.)
        rating_link_element = hotel.find("a", {"data-testid": "review-score-link"})
        if rating_link_element:
            num_external_reviews = rating_link_element.find(
                "div", {"class": "abf093bdfe f45d8e4c32 d935416c47"}
            ).text.strip()

            booking_user_ratings = rating_link_element.find(
                "div", {"class": "a3b8729ab1 e6208ee469 cb2cbb3ccb"}
            ).text.strip()

            avg_user_ratings_element = rating_link_element.find(
                "div", {"class": "a3b8729ab1 d86cee9b25"}
            )
            if avg_user_ratings_element:
                avg_user_ratings = avg_user_ratings_element.text.strip()
            else:
                avg_user_ratings = None
        else:
            num_external_reviews = None
            booking_user_ratings = None
            avg_user_ratings = None

        has_airport_taxi_element = hotel.find(
            "span", {"data-testid": "property-card-deal"}
        )
        if has_airport_taxi_element:
            airport_taxi = has_airport_taxi_element.text.strip()
        else:
            airport_taxi = "No airport taxi"

        sustainable_level_element = hotel.find(
            "span", {"data-testid": "badge-sustainability"}
        )
        if sustainable_level_element:
            travel_sustainable_level = sustainable_level_element.text.strip()
        else:
            travel_sustainable_level = None

        has_free_cancelation_element = hotel.find(
            "span", {"data-testid": "cancellation-policy-icon"}
        )
        if has_free_cancelation_element:
            has_free_cancelation = True
        else:
            has_free_cancelation = False

        hotels_per_page.append(
            {
                "name": name,
                "location": location,
                "price": price,
                "date": date,
                "stars": stars,
                "distance_from_center": distance_from_center,
                "num_external_reviews": num_external_reviews,
                "booking_user_ratings": booking_user_ratings,
                "avg_user_ratings": avg_user_ratings,
                "airport_taxi": airport_taxi,
                "travel_sustainable_level": travel_sustainable_level,
                "has_free_cancelation": has_free_cancelation,
            }
        )

    return hotels_per_page


def create_hotels_csv(hotels_data=[]):
    number_of_pages = 2

    try:
        for date in dates:
            print(len(hotels_data))
            print(date)

            for destination in destinations:
                print(destination)
                hotels_per_page = []

                for offset in range(number_of_pages):
                    offset = len(hotels_per_page) * offset
                    print("offset: ", offset)
                    params = {
                        "ss": destination,
                        "checkin": date[0],
                        "checkout": date[1],
                        "offset": offset,
                        "dest_type": dest_type,
                        "group_adults": group_adults,
                        "no_rooms": no_rooms,
                        "group_children": group_children,
                        "selected_currency": selected_currency,
                    }

                    response = requests.get(base_url, headers=headers, params=params)
                    soup = BeautifulSoup(response.text, "html.parser")
                    hotels = soup.findAll("div", {"data-testid": "property-card"})

                    hotels_per_page = get_hotels(hotels, date)
                    hotels_data += hotels_per_page

    except Exception as e:
        raise e

    finally:
        hotels = pd.DataFrame(hotels_data)
        print(hotels.head)
        hotels.to_csv("data/hotels_daily_final.csv", header=True, index=False)


# ===================================================================================================
# - (OLD) Time of executing: 27 Jan 2024 hotels_daily.csv - regarding Amsterdam and Mavrovo
#
# - Time of executing these queries: 27 Jan 2024 (hotels_daily_final.csv)
#        - according to new script (previous scripts were ran 8 Jan 2024, 20 Jan 2024)
#
# - About: This script creates a csv file that contains information about 1 night stays in
#         hotels available on booking.com regarding the 'destinations' and 'dates' provided.
#         The csv created contains these columns regarding the hotels: name, location,
#         price, date of stay (date), stars, distance from city center in km (distance_from_center),
#         number of external (user) reviews (num_external_reviews), bookigs classified rating
#         based on user reviews (booking_user_ratings), average user ratings (avg_user_ratings),
#         wether a taxi from the airport is available (airport_taxi),
#         sustainable travel options ranked from 0 to 3+ (travel_sustainable_level),
#         wether free cancelation is included in the deal (has_free_cancelation).
#
# - Data provided has:
#       -> destination:    Amsterdam, Netherlands + Antwerp, Belgium + Dortmund, Germany
#       -> dates:          01.02.2024 - 31.01.2025
#       -> people:         2 adults
#       -> offset:         items per page (25 in this case)
#       -> no_rooms:       1
#       -> currency:       MKD
# ===================================================================================================

if __name__ == "__main__":
    # default url without any/many query params
    base_url = "https://www.booking.com/searchresults.html?&lang=en-us&sb=1&src_elem=sb&src=index"
    dates = construct_dates()
    destinations = [
        "Amsterdam",
        "Antwerp%2C+Antwerpen+Province%2C+Belgium",
        "Dortmund%2C+North+Rhine-Westphalia%2C+Germany",
    ]
    dest_type = "city"
    group_adults = 2
    no_rooms = 1
    group_children = 0
    selected_currency = "MKD"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    create_hotels_csv()

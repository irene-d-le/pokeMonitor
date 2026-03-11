import requests   # make web requests
import time       # add delays between checks
import json       # read the data that comes back

TCIN = "95082118"


CHECK_DELAY = 20

# The API URL 
URL = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin=95082118&is_bot=false&store_id=1771&pricing_store_id=1771&has_pricing_store_id=true&has_financing_options=true&include_obsolete=true&visitor_id=019B773319C6020193877DF0D024B8F6&skip_personalized=true&skip_variation_hierarchy=true&channel=WEB&page=%2Fp%2FA-95082118"

# --------------------
# HEADERS
# --------------------
# This makes request look like it came from a real browser

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.target.com/"
}

# --------------------
# CHECK STOCK FUNCTION
# --------------------

def check_stock():
    try:
        # Make the request to Target's API
        response = requests.get(URL, headers=HEADERS)

        # request fail, print the error code and stop
        if response.status_code != 200:
            print("Request failed with status code: " + str(response.status_code))
            return

        # convert the response into a Python dict 
        data = response.json()

        # Dig into the JSON to find the stock status
        # Each [] means "go into this key"
        product = data["data"]["product"]
        title = product["item"]["product_description"]["title"]
        fulfillment = product["fulfillment"]

        # Check online stock status
        online_status = fulfillment["shipping_options"]["availability_status"]

        # Check in-store stock status (if available)
        store_status = "UNKNOWN"
        if "store_options" in fulfillment:
            store_status = fulfillment["store_options"][0]["availability_status"]

        print("Product: " + title)
        print("Online status: " + online_status)
        print("In-store status: " + store_status)
        print("---")

        if online_status == "IN_STOCK" or store_status == "IN_STOCK":
            print("*** IN STOCK! ***")

    except Exception as e:
        #print the error and keep going
        print("Something went wrong: " + str(e))


# --------------------
# MAIN LOOP
# --------------------

print("Starting stock monitor...")
print("Checking every " + str(CHECK_DELAY) + " seconds")
print("Press Ctrl+C to stop")
print("")

while True:
    check_stock()
    time.sleep(CHECK_DELAY)  # Wait before checking again
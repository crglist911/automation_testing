import requests
import time
import os

# --- Configuration ---
# Replace 'YOUR_API_KEY' with your actual Metals-API access key.
# You can also set it as an environment variable named METAL_API_KEY.
API_KEY = os.environ.get("METAL_API_KEY", "YOUR_API_KEY")

BASE_URL = "https://metals-api.com/api/latest"
SYMBOLS = "XAU,XAG,XCU"  # Gold, Silver, Copper
# For direct USD prices, the API might return them as USDXAU, USDXAG, etc.
# We will try to use those if available.

# --- Functions ---
def fetch_metal_prices(api_key, symbols_str):
    """Fetches metal prices from the Metals-API."""
    params = {
        'access_key': api_key,
        'base': 'USD',  # We want prices in USD
        'symbols': symbols_str
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
    except ValueError as e: # Handles JSON decoding errors
        print(f"Error decoding API response: {e}")
        return None

def display_prices(api_data):
    """Parses and displays the metal prices."""
    if not api_data or not api_data.get('success'):
        print("Failed to retrieve valid data from API.")
        if api_data and 'error' in api_data:
            print(f"API Error Code: {api_data['error'].get('code')}")
            print(f"API Error Info: {api_data['error'].get('info')}")
        return

    rates = api_data.get('rates', {})
    timestamp = api_data.get('timestamp')
    date = api_data.get('date')

    if timestamp:
        print(f"\nPrices as of: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))} (UTC)")
    elif date:
        print(f"\nPrices as of: {date}")
    else:
        print("\nLatest Prices:")

    # Define the metals and their expected keys in the API response
    # The API might provide direct USD prices like "USDXAU" or inverse rates like "XAU"
    metals_to_display = {
        "Gold": ["USDXAU", "XAU"],
        "Silver": ["USDXAG", "XAG"],
        "Copper": ["USDXCU", "XCU"] # Assuming XCU or USDXCU for copper
    }

    found_any_price = False
    for metal_name, symbol_keys in metals_to_display.items():
        price_found_for_metal = False
        for key_to_try in symbol_keys:
            if key_to_try in rates:
                price = rates[key_to_try]
                # If the key is like "XAU" (inverse rate when base is USD), calculate 1/price
                # If the key is like "USDXAU" (direct rate), use as is.
                # The documentation says: "When fetching metal rates with USD selected as the base currency ...
                # it is necessary to apply 1/value to the API response...
                # Furthermore, when USD serves as the base, the API response will include the USD Price
                # without requiring additional conversion. This can be identified, for example, as USDXAU."
                if not key_to_try.startswith("USD"):
                     # Avoid division by zero if rate is 0, though unlikely for metal prices
                    if price == 0:
                        print(f"  {metal_name} ({key_to_try}): Invalid rate (0)")
                        continue
                    price = 1 / price
                
                print(f"  {metal_name} ({key_to_try}): {price:.2f} USD")
                price_found_for_metal = True
                found_any_price = True
                break # Found price for this metal, move to next metal
        
        if not price_found_for_metal:
            print(f"  {metal_name}: Price not found in API response for symbols {symbol_keys}.")

    if not found_any_price:
        print("  No prices found for the requested metals in the API response.")
        print("  Available rates in response:", rates)


# --- Main Loop ---
if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY":
        print("Error: API_KEY is not configured.")
        print("Please replace 'YOUR_API_KEY' in the script with your actual Metals-API access key,")
        print("or set it as an environment variable named METAL_API_KEY.")
    else:
        print("Fetching metal prices every 30 seconds. Press Ctrl+C to stop.")
        try:
            while True:
                api_data = fetch_metal_prices(API_KEY, SYMBOLS)
                if api_data:
                    display_prices(api_data)
                else:
                    print("Skipping display due to fetch error.")
                
                print("\nWaiting for 30 seconds before next update...")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\nScript terminated by user.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

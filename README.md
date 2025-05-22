# Metal Price Fetcher

This script fetches and displays the current prices for Gold, Silver, and Copper every 30 seconds.

## Features

- Fetches prices for Gold (XAU), Silver (XAG), and Copper.
- Updates prices every 30 seconds.
- Displays prices in USD.

## Setup

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Get an API Key:**
    This script uses the [Metals-API](https://metals-api.com/) to fetch metal prices. You will need to sign up for a free API key on their website.
4.  **Configure API Key:**
    Open the `metal_prices.py` script and replace the placeholder `YOUR_API_KEY` with your actual Metals-API access key.

    ```python
    API_KEY = "YOUR_API_KEY"
    ```

## Usage

Run the script from your terminal:

```bash
python metal_prices.py
```

The script will then print the latest prices for Gold, Silver, and Copper, updating every 30 seconds.
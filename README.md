# Python Scraper Project Readme <br>

This repository contains a Python web scraper project that allows you to search for electronic items on a website. You can specify various options to customize your search, including the maximum and minimum price for the item and the brand name.

## Getting Started

Follow these steps to get started with the Python scraper project:

## 1. Clone the Repository

You can clone this project from GitHub using the following command:

bash
`git clone https://github.com/fcbohdan/scraperproject.git`

## 2. Install Requirements

Navigate to the project directory and install the required Python packages from the requirements.txt file. You can use pip for this:

bash <br>
`cd scraper-project` <br>
`pip install -r requirements.txt`

## 3. Run the Scraper

To run the scraper, use the main.py script with the --help option to view available options and their descriptions:

bash
`python main.py --help`
This will display the available options and their explanations.

Available Options
The scraper offers the following options to customize your search:

`-t, --max_price INTEGER:` Set the maximum price for the item you are searching for. Provide an integer value.

`-f, --min_price INTEGER:` Set the minimum price for the item you are searching for. Provide an integer value.

`-b, --brand` [apple|samsung|huawei|xiaomi|sony|lg|nokia|motorola|htc|asus|alcatel|google]: Specify the brand name of the item you are interested in. You must provide the brand name in lowercase.

**Example usage:**

bash
Copy code
`python main.py -t 500 -f 200 -b samsung`
This command will run the scraper with a maximum price of 500, a minimum price of 200, and a brand filter for "samsung."

Feel free to customize the options according to your preferences to search for electronic items that match your criteria.

Happy scraping!
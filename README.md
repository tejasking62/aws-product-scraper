# AWS Products Data Scraper Project

This project uses Selenium to scrape product information from the AWS products page, specifically the description, name, category, and tier type. The data is then saved into an Excel file for further analysis.

## Features
### aws_parse.py
- Uses **Selenium Webdriver** to automate the process of opening a browser and navigating to the AWS products page.
- Extracts product details such as category, name, description, and free tier type with thorough inspection of page.
- Iterates through multiple pages of results.
- Employs **Pandas** and **openpyxl** to save the collected data to an Excel file with custom formatting.

## Prerequisites

- Python 3.x
- Google Chrome browser installed
- ChromeDriver (managed automatically using `webdriver_manager`)

## Installation

Clone the repository:

```sh
git clone https://github.com/tejasking62/aws-product-scraper.git
cd aws-product-scraper

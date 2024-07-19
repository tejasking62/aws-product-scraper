import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook
import time
from datetime import datetime

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def collect_data(driver):
    # Locate the products container
    products_container = driver.find_element(By.CSS_SELECTOR, 'ul.aws-directories-container')

    # Find all product elements within the container
    products = products_container.find_elements(By.CSS_SELECTOR, 'li.lb-xbcol.m-showcase-card')

    products_data = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Loop through each product and extract the name and description
    for product in products:
        try:
            category = product.find_element(By.CSS_SELECTOR, 'div.m-category > span').text
            headline = product.find_element(By.CSS_SELECTOR, 'div.m-headline').text
            description = product.find_element(By.CSS_SELECTOR, 'div.m-desc').text
            tier = product.find_element(By.CSS_SELECTOR, 'div.m-flag').text
            
            
            if tier != '12 Months Free' and tier != 'Free Trial':
                tier = "Always Free"
            
            data = {
                "Product Category": category,
                "Product": headline,
                "Product Description": description,
                "Free Tier Type": tier,
                "Time Stamp" : timestamp
            }
            
            products_data.append(data)
        except Exception as e:
            print(f"Error extracting product details: {e}")
            
    return products_data

base_url = "https://aws.amazon.com/products/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=free-tier%23always-free%7Cfree-tier%2312-months-free%7Cfree-tier%23free-trial&awsf.tech-category=*all&awsm.page-aws-products-all=1"
driver.get(base_url)
time.sleep(5)

page_count = 1

try:
    container = driver.find_element(By.CSS_SELECTOR, 'div.m-cards-page-numbers.m-active')
    page_links = container.find_elements(By.TAG_NAME, 'a')
    for link in page_links:
        try:
            page_number = link.text
            if page_number.isdigit():
                page_count += 1
        except ValueError:
            continue
except Exception as e:
    print("Error")

all_products_data = collect_data(driver)

for i in range(2, page_count+1):
    url = base_url[:-1] + str(i)
    # Open the webpage
    driver.get(url)
    time.sleep(5)
    all_products_data.extend(collect_data(driver))


# Close the driver
driver.quit()

df = pd.DataFrame(all_products_data)
print(df)

file_name = 'aws_products.xlsx'

with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='AWS Products', index=False)

wb = load_workbook(file_name)
ws = wb['AWS Products']

ws.column_dimensions['A'].width = 30
ws.column_dimensions['B'].width = 35
ws.column_dimensions['C'].width = 60
ws.column_dimensions['D'].width = 15
ws.column_dimensions['E'].width = 20

# Save the changes to the workbook
wb.save(file_name)

# CASE [Select Age Group]
# WHEN "Under 5 pct" THEN [Under 5 pct]
# WHEN "5-9 Pct" THEN [5-9 Pct]
# WHEN "10-14 Pct" THEN [10-14 Pct]
# WHEN "15-19 Pct" THEN [15-19 Pct]
# WHEN "20-24 Pct" THEN [20-24 Pct]
# WHEN "25-29 Pct" THEN [25-29 Pct]
# WHEN "30-34 Pct" THEN [30-34 Pct]
# WHEN "35-39 Pct" THEN [35-39 Pct]
# WHEN "40-44 Pct" THEN [40-44 Pct]
# WHEN "45-49 Pct" THEN [45-49 Pct]
# WHEN "50-54 Pct" THEN [50-54 Pct]
# WHEN "55-59 Pct" THEN [55-59 Pct]
# WHEN "60-64 Pct" THEN [60-64 Pct]
# WHEN "65-69 Pct" THEN [65-69 Pct]
# WHEN "70-74 Pct" THEN [70-74 Pct]
# WHEN "75-79 Pct" THEN [75-79 Pct]
# WHEN "80-84 Pct" THEN [80-84 Pct]
# WHEN "85+ Pct" THEN [85+ Pct]
# END


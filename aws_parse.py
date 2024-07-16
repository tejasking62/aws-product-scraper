import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook
from openpyxl import Workbook
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

base_url = "https://aws.amazon.com/products/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&awsf.re%3AInvent=*all&awsf.Free%20Tier%20Type=free-tier%23always-free%7Cfree-tier%2312-months-free%7Cfree-tier%23free-trial&awsf.tech-category=*all&awsm.page-aws-products-all="
all_products_data = []

for i in range(1, 8):
    url = base_url + str(i)
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

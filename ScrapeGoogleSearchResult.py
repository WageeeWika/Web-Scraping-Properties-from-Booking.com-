import csv
import os
import time

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#####################################################
# PREPARATION THE NEED FOR SCRAPING
#####################################################
# Read data from Excel/CSV file using pandas -- Data_Properti_Kuta_1.csv (contoh .csv 25 data)
while True:
    print("Input file name (Excel/CSV):")
    file_name = input("=> ")
    file_ext = '.csv'
    file_path = file_name + file_ext  # Assuming the default extension is '.csv'

    if os.path.exists(file_path):
        print(f"File '{file_name}' exists. Proceeding...")
        break  # Break the loop when a valid file exists
    else:
        print(f"File '{file_name}' not found. Please enter a valid file name.")

data = pd.read_csv(file_path, delimiter=';', header=3)

# Call Chrome Driver
service = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Optimisasi untuk percepat loading search result/proses scraping
first_try = WebDriverWait(driver, 3)
second_try = WebDriverWait(driver, 5)

# Deklarasi Variable untuk Menghitung Kecepatan Scraping
start_time = time.time()
total_time = 0
sum_perloop_time = 0
perloop_time = 0
cnt = 0

#####################################################
# LOOP FOR SEARCHING EACH PROPERTY IN GOOGLE SEARCH ENGINE
#####################################################
# Loop through the data
for index, row in data.iterrows():
    start_prop_time = time.time()
    cnt = cnt + 1
    query = row[f'{data.columns[1]}']  # Kolom dari nama Property
    query2 = row[f'{data.columns[3]}']  # Kolom dari nama kota letak Property

    # Perform Google search
    driver.get(f"https://www.google.com/search?q={query}, {query2}, Bali dengan maps")
    print(f'# {cnt}.')
    print(f'Finding additional property data for "{query}"...')

    # Extract address and phone number from the search results using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        try:
            first_try.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[jsname="xQjRM"]')))
        except TimeoutException:
            second_try.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[jsname="xQjRM"]')))
            break
    except TimeoutException:
        # print("Phone Number not found!")
        pass
    address_el = soup.find('span', {'class': 'LrzXr'})
    list_address = soup.find('div', {'class': 'x3SAYd'})
    phone_el = soup.find('a', {'data-dtype': 'd3ph'})

    # Check if address and phone number elements are found
    if address_el:
        address = address_el.text
        if phone_el is not None:
            phone_number = phone_el.text
        else:
            phone_number = 'Phone number not found'
    elif list_address:
        btn_address = driver.find_element(By.CSS_SELECTOR, '[jsname="kj0dLd"]')
        driver.execute_script("arguments[0].scrollIntoView();", btn_address)
        driver.execute_script("window.scrollBy(0, -100);")
        btn_address.click()

        try:
            chk_address_el = first_try.until(EC.element_to_be_clickable((By.CLASS_NAME, 'LrzXr')))
        except TimeoutException:
            chk_address_el = second_try.until(EC.element_to_be_clickable((By.CLASS_NAME, 'LrzXr')))

        try:
            chk_phone_el = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-dtype="d3ph"]')))
        except TimeoutException:
            chk_phone_el = None

        elements = driver.find_elements(By.CLASS_NAME, 'fl')
        for element in elements:
            if ('Address' or 'Alamat') or ('Phone' or 'Telepon') in element.text:
                if chk_address_el and chk_phone_el is not None:
                    try:
                        address_el = driver.find_element(By.CSS_SELECTOR, '[class="LrzXr"]')
                    except NoSuchElementException:
                        address_el = 'Address not Found'
                    phone_el = driver.find_element(By.CSS_SELECTOR, '[data-dtype="d3ph"]')

                    if address_el:
                        if isinstance(address_el, str):
                            address = address_el
                        else:
                            address = address_el.text
                        if phone_el is not None:
                            phone_number = phone_el.text
                        else:
                            phone_number = 'Phone number not found'
                elif chk_address_el and chk_phone_el is None:
                    address_el = driver.find_element(By.CSS_SELECTOR, '[class="LrzXr"]')
                    if address_el:
                        address = address_el.text
                    phone_number = 'Phone number not found'
    else:
        address = 'Address not found'
        phone_number = 'Phone number not found'

    if address is not None and (phone_number is None or phone_number is not None):
        print(f'Additional data for "{query}" scraped!')
    else:
        print(f'{address} and {phone_number}')

    end_prop_time = time.time()
    perloop_time = end_prop_time - start_prop_time
    total_time += perloop_time
    print(f"Took {perloop_time:.2f} seconds\n")

    # Write scraped data back to the file
    data.at[index, 'Additional Detailed Address'] = address
    data.at[index, 'Phone Number'] = phone_number

#####################################################
# COUNT HOW LONG SCRAPING TAKE (In seconds)
#####################################################
# Get the current time after the loop completes
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
avg_per_prop = total_time / cnt
print(f"Time taken for scraping {cnt} additional property data: {elapsed_time:.2f} seconds\nwith an average {avg_per_prop:.2f} seconds per property")

#####################################################
# SAVE SCRAPED DATA INTO NEW .CSV FILE
#####################################################
# Prepare the filename for the updated CSV file
updated_file_path = 'Updated_' + file_path

# Check if a file with the similar name already exists
if os.path.exists(updated_file_path):
    # If the file exists, incrementally add numbers until finding a unique filename
    file_number = 1
    while True:
        updated_file_path = f'updated_v{file_number}_{file_path}'
        if not os.path.exists(updated_file_path):
            break
        file_number += 1

# Save the updated data to the CSV file
# data = data.replace('\n', '', regex=True)
data.to_csv(updated_file_path, index=False)

print(f'Additional data for all Property in "{file_path}" file updated successfully!')

# Close the browser
driver.quit()

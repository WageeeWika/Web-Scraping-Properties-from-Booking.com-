from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import subprocess
import locale
import requests
import csv
import re
import time

#####################################################
# CONFIGURE URL, CHROME DRIVER, BEAUTIFULSOUP
#####################################################
url = "https://www.booking.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/51.0.2704.64 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}
print("Opening Booking.com, Please wait...")
# Call Chrome Driver
service = Service('C:\Program Files\chromedriver.exe')
driver = webdriver.Chrome(service=service)
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
driver.get(url)

#####################################################
# CLOSE POPUP WINDOW
#####################################################
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="header-logo"]')))
print("Booking.com opened! \n")
try:
    popup_visible = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'eb33ef7c47'))
    )
    print("Closing popup window...")
    close_popup = popup_visible.find_element(By.CLASS_NAME, 'a83ed08757')
    close_popup.click()
    print("Popup Closed! \n")
except TimeoutException:
    # This block will be executed if the TimeoutException is raised
    print("Great! Any Popup did not appear :D Continuing with the rest of the code... \n")

#####################################################
# SELECT CURRENCY
#####################################################
try:
    btn_curr = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="header-currency-picker-trigger"]')))
    btn_curr.click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="All currencies"]')))
    time.sleep(1)
    print("Pilihan Mata Uang (Currency): ")
    print("1 = Indonesian Rupiah (IDR)")
    print("2 = U.S. Dollar (USD)")


    def currency():
        while True:
            try:
                number = int(input("Pilih Mata Uang (Currency) => "))
                if 1 <= number <= 2:
                    return number
                else:
                    print("Please enter a number between 1 and 2!")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 2!")

    currency = currency()
    if currency == 1:
        try:
            IDR = driver.find_element(By.XPATH, "//span[contains(text(),'Indonesian Rupiah')]")
            IDR.click()
            print("Indonesian Rupiah selected")
        except TimeoutException:
            print("Currency not found!")
    elif currency == 2:
        try:
            USD = driver.find_element(By.XPATH, "//span[contains(text(),'U.S. Dollar')]")
            USD.click()
            print("U.S. Dollar selected")
        except TimeoutException:
            print("Currency not found!")
    print()
except TimeoutException:
    print("Selecting Currency Failed! Continuing...")

# Ambil dan gunakan url terbaru karena terdapat update pada webpage
url = driver.current_url
driver.get(url)
time.sleep(2)

#####################################################
# SELECT LANGUAGE
#####################################################
print("Choosing Language...")
try:
    lang = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="header-language-picker-trigger"]')))
    lang.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="All languages"]')))
    time.sleep(1)
    print("Pilihan Bahasa: ")
    print("1 = Bahasa Indonesia")
    print("2 = Bahasa Inggris (English US)")
    lang1 = driver.find_element(By.XPATH, "//span[contains(text(),'Bahasa Indonesia')]")
    lang2 = driver.find_element(By.XPATH, "//span[contains(text(),'English (US)')]")


    def language():
        while True:
            try:
                number = int(input("Pilih bahasa => "))
                if 1 <= number <= 2:
                    return number
                else:
                    print("Please enter a number between 1 and 2!")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 2!")


    language = language()
    if language == 1:
        lang1.click()
        print(f"Language: Bahasa Indonesia selected!")
    elif language == 2:
        lang2.click()
        print(f"Language: English (US) selected!")
    else:
        print("Terjadi kesalahan! :(")
    print()
except TimeoutException:
    print("Choose language process failed! Continuing...")

# Ambil dan gunakan url terbaru karena terdapat update pada webpage
url = driver.current_url
driver.get(url)
time.sleep(2)

#####################################################
# PICK DATE
#####################################################
date_pick = driver.find_element(By.CSS_SELECTOR, f'[data-testid="searchbox-dates-container"]')
date_pick.click()
print("Pilihan tanggal booking: ")
print("1 = 1 Hari/Malam (Minggu ini, Bulan ini)")
print("2 = 1 Bulan (Bulan depan)")


def date_option():
    try:
        number = int(input("Pilih tanggal Booking => "))
        if 1 <= number <= 2:
            return number
        else:
            print("Please enter a number between 1 and 2!")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 2!")


date_opt = date_option()
print()
try:
    div_date = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="datepicker-tabs"]')))
    btn_flex = div_date.find_element(By.XPATH,
                                     "//body/div[@id='indexsearch']/div[2]/div[1]/form[1]/div[1]/div[2]/div["
                                     "1]/div[2]/div[1]/nav[1]/div[1]/ul[1]/li[2]/button[1]")
    btn_flex.click()
    if language == 2:
        weekend_id = "//div[contains(text(),'A weekend')]"
        month_id = "//div[contains(text(),'A month')]"
    else:
        weekend_id = "//div[contains(text(),'Selama akhir pekan')]"
        month_id = "//div[contains(text(),'Sebulan')]"

    if date_opt == 1:
        try:
            btn_weekend = div_date.find_element(By.CSS_SELECTOR, '[data-testid="flexible-dates-day"]')
            txt_btn_weekend = btn_weekend.find_element(By.XPATH, weekend_id)
            txt_btn_weekend.click()

            btn_when1 = div_date.find_element(By.XPATH,
                                              "//body/div[@id='indexsearch']/div[2]/div[1]/form[1]/div[1]/div["
                                              "2]/div[1]/div[2]/div[1]/nav[1]/div[2]/div[1]/div[1]/div[2]/div["
                                              "1]/div[3]/ul[1]/li[1]")
            btn_when1.click()
        except TimeoutException:
            print("Pick date failed! Continuing...")
    elif date_opt == 2:
        try:
            btn_month = div_date.find_element(By.CSS_SELECTOR, '[data-testid="flexible-dates-day"]')
            txt_btn_month = btn_month.find_element(By.XPATH, month_id)
            txt_btn_month.click()

            btn_when2 = div_date.find_element(By.XPATH,
                                              "//body/div[@id='indexsearch']/div[2]/div[1]/form[1]/div[1]/div["
                                              "2]/div[1]/div[2]/div[1]/nav[1]/div[2]/div[1]/div[1]/div[2]/div["
                                              "1]/div[3]/ul[1]/li[2]")
            btn_when2.click()
        except TimeoutException:
            print("Pick date failed! Continuing...")
    submit = driver.find_element(By.XPATH,
                                 "//body/div[@id='indexsearch']/div[2]/div[1]/form[1]/div[1]/div[2]/div["
                                 "1]/div[2]/div[1]/nav[1]/div[2]/div[1]/div[2]/button[1]")
    submit.click()
except TimeoutException:
    print("Pick Date Failed! Continuing...")

#####################################################
# FIND CITY
#####################################################
search_field = driver.find_element(By.XPATH, "//input[@id=':re:']")
search_field.click()
filled_text = search_field.get_attribute('value')

if filled_text is not None:
    search_field.send_keys(Keys.SHIFT + Keys.HOME)
    search_field.send_keys(Keys.BACKSPACE)

print("Cari lokasi...")
find_places = input('=> ')
search_field.send_keys(find_places)

# Pilih list pertama dari hasil pencarian
print(f"Finding property in '{find_places}'...")
time.sleep(2)
search_list = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'autocomplete-result-0')))
search_list.click()
btn_search = driver.find_element(By.XPATH, "//body/div[@id='indexsearch']/div[2]/div[1]/form[1]/div[1]/div["
                                           "4]/button[1]")
btn_search.click()

# Untuk mengambil url terbaru
url = driver.current_url
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
driver.get(url)

WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="header-logo"]')))
print(f"Data property in '{find_places}' found! \n")

#####################################################
# CLOSE POPUP WINDOW
#####################################################
# close popup window jika ada yang muncul
try:
    popup_visible = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'eb33ef7c47'))
    )
    print("Closing popup window...")
    close_popup = popup_visible.find_element(By.CLASS_NAME, 'a83ed08757')
    close_popup.click()
    print("Popup Closed! \n")
except TimeoutException:
    # This block will be executed if the TimeoutException is raised
    print("Great! Any Popup did not appear :D Continuing with the rest of the code... \n")

#####################################################
# SORTING PROPERTI LIST
#####################################################
# Percobaan pengulangan pada sort list properti, karena kadang berjalan lancar dan kadang tidak
print("Sorting Property...")
try:
    time.sleep(2)
    sort = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="sorters-dropdown-trigger"]')))
    sort.click()

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="sorters-dropdown"]')))
    select_sort = driver.find_element(By.CSS_SELECTOR, f'[data-id="review_score_and_price"]')
    select_sort.click()
    time.sleep(1)

    max_attempts = 3
    attempts = 0
    while attempts < max_attempts:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="title-link"]')))
            print("Property List Sorted! \n")
            break
        except TimeoutException:
            attempts += 1
            print(f"Attempt {attempts} failed")
            time.sleep(1)
    else:
        print("Max attempts reached. Could not complete the operation :(")
except TimeoutException:
    print("Sort property failed! Continuing... \n")

print("Scraping Data...")

# Untuk mengambil url terbaru
url = driver.current_url
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
driver.get(url)

#####################################################
# SCRAPING DATA PROPERTY LOOPING PER PAGE (25 Properties)
#####################################################
data = []
location_date = []

lokasi_sumProperti = soup.find('div', {'class': 'efdb2b543b e4b7a69a57'}).text
pn = 0
no_prop = 0


def pages():
    try:
        number = int(input("Masukkan total halaman yang ingin diambil datanya => "))
        if 1 <= number <= 200:
            return number
        else:
            print("Please enter a number between 1 and 200!")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 200!")


total_page = pages()
while pn < total_page:
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{pn + 1}')]")))

        pn += 1
        print(f"Scraping Page {pn}...")

        next_url = driver.current_url
        if url != next_url:
            response = requests.get(next_url, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        properties = soup.find_all('div', {'data-testid': 'property-card'})

        driver.get(next_url)
        header_title = 'header-logo'
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{header_title}"]')))

        for prop in properties:
            title2prop = prop.find('h4', {'class': 'abf093bdfe e8f7c070a7'})
            title2prop = title2prop.text if title2prop else "No other Description"

            div_avail = prop.find_all('div', {'data-testid': 'availability-single'})
            div_prop = prop.find_all('div', {'class': 'aca0ade214 c9835feea9 c2931f4182 d79e71457a f02fdbd759'})

            # Ini bagian Detail harga dan lama tinggal/booking
            for avail_sect in div_avail:
                dates = avail_sect.find('div', {'data-testid': 'flexible-dates'}).text
                det_dates = avail_sect.find('div', {'data-testid': 'price-for-x-nights'}).text
                price = avail_sect.find('span', {'data-testid': 'price-and-discounted-price'}).text
                if currency == 1 and (language == 1 or language == 2):
                    cleaned_price = price.replace('\xa0', '').replace('Â', '').replace(',', '').replace('.', '')
                    price_value = int(cleaned_price.replace('Rp', ''))
                    locale.setlocale(locale.LC_ALL, 'Indonesian')
                elif currency == 2 and (language == 1 or language == 2):
                    price_value = int(re.search(r'\d+', price).group())
                    locale.setlocale(locale.LC_ALL, 'en-US.UTF-8')
                formatted_price = locale.currency(price_value, grouping=True)
                group_date = f"{dates} / {det_dates}"

            for prop_sect in div_prop:
                no_prop += 1
                title1prop = prop_sect.find('div', {'data-testid': 'title'}).text
                alamat = prop_sect.find('span', {'data-testid': 'address'}).text
                # alamat2 = alamat2.text
                div_score = prop_sect.find_all('a', {'data-testid': 'review-score-link'})

                if language == 2:
                    new_prop_text = 'New to Booking.com'
                else:
                    new_prop_text = 'Baru bergabung dengan Booking.com'

                new_prop = prop_sect.find('span', {'class': 'b30f8eb2d6'}, string=new_prop_text)
                if div_score and (new_prop is not None or new_prop is None):
                    for sc in div_score:
                        reviews = sc.find('div', {'class': 'abf093bdfe f45d8e4c32 d935416c47'}).text
                        rating = sc.find('div', {'class': 'a3b8729ab1 d86cee9b25'})
                        if rating is not None:
                            rating = rating.text
                        else:
                            rating = "Rating based on other travel sites (Rating can also be seen in Kualitas)"
                        kualitas = sc.find('div', {'class': 'a3b8729ab1 e6208ee469 cb2cbb3ccb'})
                        if kualitas.text.strip() == "Review score":
                            kualitas = "Less than Good :("
                        else:
                            kualitas = kualitas.text
                        if new_prop is not None:
                            new_prop = "NEW Property!"
                        else:
                            new_prop = "Been a while"
                        # data.append([no_prop, title1prop, title2prop, alamat, reviews, rating, kualitas, new_prop, group_date, cleaned_price])
                elif new_prop or new_prop is None:
                    reviews = "No reviews yet!"
                    rating = "No rating yet!"
                    kualitas = "None (Based on Rating)"
                    if new_prop is not None:
                        new_prop = "NEW Property!"
                    else:
                        new_prop = "Been a while"
                data.append(
                    [no_prop, title1prop, title2prop, alamat, reviews, rating, kualitas, new_prop, formatted_price])

        print(f"Page {pn} Done! {no_prop} data Scraped!")
        time.sleep(2)

        try:
            next_page_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(),'{pn + 1}')]")))
            next_page_button.click()
        except TimeoutException:
            print("Next page not found!")

    except TimeoutException:
        print("Maximum page reached...")
        break

location_date.append([lokasi_sumProperti, group_date])

driver.quit()
print()
print(f"Finished! \n{no_prop} Data Property(s) Received! \nFrom a total of {pn} page(s) \n")
time.sleep(1)

#####################################################
# SAVE SCRAPED DATA INTO CSV FILE
#####################################################
# Simpan data dalam file CSV
print("Creating .csv file and input recieved data...")
time.sleep(1)

print("### Masukkan nama daerah (Untuk nama file CSV): ")
daerah = input("=> ")
file_name = f'Data_Properti_{daerah}.csv'
with open(file_name, 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Location and Total Property:', 'Detail Dates / Occupancy:'])
    writer.writerows(location_date)
    writer.writerow('')
    writer.writerow(
        ['No.', 'Title/Desc. (1) Property', 'Title/Desc. (2) Property', 'Address', 'Total Reviews', 'Rating Property',
         'Score Quality', 'Property Status in Booking.com', 'Property Price (Based on Detail Dates and Occupancy)'])
    writer.writerows(data)
print("File created and Data Scraping process done!")


#####################################################
# DECIDE WHETHER USER WANTS THE ADDITIONAL DATA PROPERTY OR NOT (this will execute the second File (BookingCom2nd.py))
#####################################################
def run_second_script():
    decision = input("Do you want to run the second script? (yes/no): ")
    python_executable = 'C:/Users/TUFortresss/AppData/Local/Programs/Python/Python310/python.exe'
    script_path = 'BookingCom2nd.py'
    if decision.lower() == 'yes':
        subprocess.run([python_executable, script_path])
    else:
        print("Exiting...")


if __name__ == "__main__":
    run_second_script()

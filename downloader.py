from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from csv import DictReader, DictWriter
import os
import io
import csv
import time

# type image folder path and download folder path here
image_path = r'C:\Users\J\Documents\GitHub\rawpixel_downloader\images'
download_path = r'C:\Users\J\Documents\GitHub\rawpixel_downloader\downloads'


def run_downloader():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False}
        )

    driver = webdriver.Chrome(options=chrome_options, executable_path=r'C:\Users\J\Documents\GitHub\rawpixel_downloader\chromedriver.exe')
    driver.set_window_size(1200, 900)
    driver.get('https://www.rawpixel.com/user/login?destination=daily-inspiration')

    try:
        # You will have 2 minutes to solve the Captcha manually. Editable with number below.
        element = WebDriverWait(driver, 6000).until(
            ec.presence_of_element_located((By.XPATH, "//span[text()='My Account']"))
        )
        print('successfully solved captcha')
        with io.open("info.csv", mode="w", encoding="utf-8") as fd:
            fieldnames = ["title", "url", "filename"]
            writer = csv.DictWriter(fd, fieldnames=fieldnames)
            writer.writeheader()
            read_csv(driver)
    except Exception as e:
        print(e)


def read_csv(driver):
    urls_info = []
    # open file in read mode
    with open('urls.csv', 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            if row['title'] != 'title' and len(row) >= 2:
                urls_info.append({'title': row['title'], 'url': row['url']})
            else:
                continue
    # Type starting file number here
    image_no = len(os.listdir(image_path))+1
    print(image_no)
    for obj in urls_info:
        image_string = str(image_no).zfill(4)
        title = obj['title']
        url = obj['url']
        filename = f'{image_string}.png'
        image_no += 1
        # Lists current files in downloads folder
        current_files = os.listdir(download_path)
        # function downloads and waits for it to complete
        download_from(driver, title, url, filename, current_files)
        # moves and renames file to images folder
        added = list(set(os.listdir(download_path)).difference(set(current_files)))
        print(f"file {added[0]} downloaded - copying")
        os.rename(fr'{download_path}\{added[0]}', rf'{image_path}\{filename}')
        # Ensures file is in images folder before continuing. Checks every 10 sec
        while filename not in os.listdir(image_path):
            print("waiting for image file")
            time.sleep(10)
        # Writes to csv
        with io.open("info.csv", mode="a", encoding="utf-8") as fd:
            info = [title, url, filename]
            fieldnames = ["title", "url", "filename"]
            writer = csv.DictWriter(fd, fieldnames=fieldnames)
            writer.writerow({'title': title, 'url': url, 'filename': filename})
            print(f'{info} downloaded and added to file')


def download_from(driver, title, url, filename, current_files):
    driver.get(url)
    time.sleep(3)
    try:
        # waits for download button
        element = WebDriverWait(driver, 3).until(
            ec.presence_of_element_located((By.XPATH, "//button[contains(@class, 'download')]"))
        )
        try:
            download_button = driver.find_element_by_xpath("//button[contains(@class, 'download')]")
            download_button.click()
            driver.execute_script("arguments[0].click();", download_button)
            waiting_for_file = True
            # Check download has appeared
            while True:
                time.sleep(5)
                # check for new files in download folder ever 5 sec
                added = list(set(os.listdir(download_path)).difference(set(current_files)))
                print(f"added:{added}")
                if not added:
                    return True
                # checks files are not .crdownload file type - i.e finished downloading
                elif added[0].split(".")[-1] == "jpg":
                    print("downloaded ---- ")
                    return False
        except Exception as err:
            print(err)
    except Exception as e:
        print(e)


run_downloader()



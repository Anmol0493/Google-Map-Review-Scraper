from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from helper_class import *
from selenium_driver import *
import time, json

class DETAILS():

    def __init__(self):

        self.helper = Helper()

        with open('Details.json', 'r', encoding='utf-8') as d:
            self.details = json.load(d)

        with open('All_Listings_Aus.json', 'r', encoding='utf-8') as listing:
            self.urls = json.load(listing)

        with open("done_urls_Aus.json", 'r', encoding='utf-8') as idu:
            self.done = json.load(idu)

        self.selenium_driver = selenium_with_proxy()


    def get_details(self, url):

        try:

            if url not in self.done:

                details = {"name": "",
                "category": "",
                "phone": "",
                "email": "",
                "website": "",
                "rating": "",
                "total_reviews": "",
                "url": url,
                }

                driver = self.selenium_driver.get_driver()
                driver.maximize_window()
                driver.get(url)
                print(url)

                try:
                    accept_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button')
                    if accept_button:
                        accept_button.click()
                except Exception:
                    pass

                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb')))

                try:
                    details["name"] = driver.find_element(By.ID, 'searchbox').get_attribute('aria-label')
                except NoSuchElementException:
                    pass

                rating_tag = self.helper.get_text_from_tag(driver.find_element(By.CSS_SELECTOR, 'div.fontBodyMedium.dmRWX'))
                rating_tag_text = rating_tag.split('(')
                details["rating"] = rating_tag_text[0].replace('\n', '')
                details["total_reviews"] = rating_tag_text[1].replace(')', '')

                try:
                    details['website'] = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']").get_attribute("href")
                except NoSuchElementException:
                    pass

                phone_button = driver.find_element(By.CSS_SELECTOR, 'button[data-tooltip="Copy phone number"]')
                details['phone'] = phone_button.get_attribute("data-item-id").split(":")[-1]

                self.details.append(details)
                print(len(self.details))

                with open('Details.json', 'w', encoding='utf-8') as o:
                    json.dump(self.details, o, indent=4)

                self.done.append(url)

                with open("done_urls_Aus.json", 'w', encoding='utf-8') as d:
                    json.dump(self.done, d, indent=4)
        
        except Exception as e:
            # print(e)
            print(f'skipping {url}')


    def main(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.get_details, self.urls)



if __name__ == '__main__':
    # DETAILS().get_details("https://www.google.com/maps/place/Melbourne+Centre+For+Dentistry/data=!4m7!3m6!1s0x6ad668e1fccc0827:0x5e8f7d0106e93223!8m2!3d-37.8974233!4d145.0050123!16s%2Fg%2F11bzshj8fq!19sChIJJwjM_OFo1moRIzLpBgF9j14?authuser=0&hl=en&rclk=1")
    DETAILS().main()
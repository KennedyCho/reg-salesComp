# scrape() function courtesy of https://github.com/scrapehero-code/amazon-scraper

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


import csv

import random

driver = webdriver.Chrome(ChromeDriverManager().install())

def scrape_search_results(page_num):
    print("Start Page " + str(page_num))
    # list of all prod web elements on search page 
    try: 
        # driver.get(search_url)
        # WebDriverWait(driver,10).until(expected_conditions.visibility_of_element_located((By.XPATH,"//div/h2/a[@class='a-link-normal a-text-normal']")))
        # print('time pass')
        initial_url_list = driver.find_elements_by_xpath("//div/h2/a[@class='a-link-normal a-text-normal']")
        
        print("# of Prod "+str(len(initial_url_list)))

        for i in range(len(initial_url_list)):
            # print(2)
            prod_info = []
            
            updated_url_list = driver.find_elements_by_xpath("//div/h2/a[@class='a-link-normal a-text-normal']")
            # print(3)
            prod_info += [updated_url_list[i].text, updated_url_list[i].get_attribute("href")]
            # print(4)

            updated_url_list[i].click()
            driver.implicitly_wait(random.randint(2,5))

            # scrape product info
            prod_info += scrape_prod_page()

            with open("amazon_results.csv", "a", newline='') as csv_file: 
                results_writer = csv.writer(csv_file)
                results_writer.writerow(prod_info)

            driver.back()

    # except NoSuchElementException as elmErr: 
    #     print('no no element'+str(elmErr))
    # except TimeoutException as timeBad: 
    #     print(str(timeBad))
    # except StaleElementReferenceException as stale: 
    #     print(str(stale))
    except: 
        print('err')
        pass


    print('Finished Page '+ str(page_num))
    

def scrape_prod_page():
    prod_info = []

    try: 
        # get product price 
        price = driver.find_element_by_xpath("//td[@class='a-span12']/span[1]").text
        
    except: 
        price = ['']

    # try: 
    #     prod_extra_info = driver.find_elements_by_xpath("//table[@id='productDetails_detailBullets_sections1']/tbody/tr")
    #     for i in prod_extra_info: 
    #         # print(i.text)
    #         if "Item model number" in i.text: 
    #             print('found model num')
    #             model = [i.text[18:]]
    #             break
    #         elif "Customer Reviews" in i.text: 
    #             break     
    # except: 
    #     model = ['']

    # add to product info list 
    prod_info = [price]
    try: 
        # check for protection plans
        driver.find_element_by_xpath("//*[contains(text(), 'Add a Protection Plan:')]")

        # get plan info 
        plans = driver.find_elements_by_xpath("//a[@id='mbbPopoverLink']")
        for plan in plans: 
            prod_info += [plan.text]
        
        plan_prices = driver.find_elements_by_xpath("//span[@class='a-label a-checkbox-label']/span[@class='a-color-price']")
        for price in plan_prices: 
            prod_info += [price.text]
        
        print('Found')
    finally:
        return prod_info
        

def search_amazon(item):
    driver.get('https://www.amazon.com')
    # driver.get('https://www.amazon.com/s?k=Sony&ref=nb_sb_noss')

    search_box = driver.find_element_by_id('twotabsearchtextbox').send_keys(item)
    search_button = driver.find_element_by_id("nav-search-submit-text").click()

    driver.implicitly_wait(5)
    for i in range(10): 
        try:
            scrape_search_results(i)
            driver.implicitly_wait(random.randint(2,5))
            driver.find_element_by_xpath('//*[@class="a-pagination"]/li[@class="a-last"]').click()
            
        except NoSuchElementException:
            print('no find next page button')

    # driver.implicitly_wait(3)

    driver.quit()

    print("---DONE---")

search_amazon('Sony speaker') # <------ search query goes here.


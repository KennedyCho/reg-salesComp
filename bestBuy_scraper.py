# scrape() function courtesy of https://github.com/scrapehero-code/amazon-scraper

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import csv

import random

driver = webdriver.Chrome(ChromeDriverManager().install())

def scrape_search_results(page_num):
    
    # list of all prod web elements on search page 
    try: 
        print('Start page '+str(page_num))
        initial_url_list = driver.find_elements_by_xpath("//h4[@class='sku-header']/a")

        print("# of Prod "+ str(len(initial_url_list)))
        # len(initial_url_list)
        for i in range(len(initial_url_list)): 
            prod_info = []
            
            updated_url_list = driver.find_elements_by_xpath("//h4[@class='sku-header']/a")

            prod_info += [updated_url_list[i].text, updated_url_list[i].get_attribute("href")]

            updated_url_list[i].click()
            driver.implicitly_wait(random.randint(2,5))

            # scrape product info
            prod_info += scrape_prod_page()
            # print(prod_info)
            with open("bestBuy_results.csv", "a", newline='') as csv_file: 
                results_writer = csv.writer(csv_file)
                results_writer.writerow(prod_info)

            driver.back()
    except: 
        print("wrong")
        # pass


    print('Finished Page '+ str(page_num))
    

def scrape_prod_page():
    prod_info = []

    # get product price 
    price = driver.find_element_by_xpath("//div[@class='priceView-hero-price priceView-customer-price']/span[1]").text

    model = driver.find_element_by_xpath("//div[@class='model product-data']/span[2]").text
    # add to product info list 
    prod_info = [model, price]
    try: 
        # check for protection plans
        driver.find_element_by_xpath("//*[@class='shop-warranty-selector']")

        # get plan info 
        plans = driver.find_elements_by_xpath("//div[@class='warranty-short-name']/span")
        for plan in plans: 
            prod_info += [plan.text]
        
        
        plan_prices = driver.find_elements_by_xpath("//div[@data-context='warranty-selector']/div/div[@class='single-price single-bold']/div/div/span[1]")

        # plan_prices = driver.find_elements_by_xpath("//div[@class='priceView-hero-price priceView-customer-price']/span[1]")
        for price in plan_prices: 
            prod_info += [price.text]
        
        print('Found')
    finally:
        return prod_info
        

def search_bestBuy(item):
    driver.get('https://www.bestbuy.com/')
    driver.implicitly_wait(5)

    # close modal 
    driver.find_element_by_xpath("//button[@class='c-close-icon  c-modal-close-icon']").click()
    driver.implicitly_wait(5)

    try: 
        search_box = driver.find_element_by_xpath("//input[@id='gh-search-input']").send_keys(item)
    except: 
        search_box = driver.find_element_by_xpath("//input[@class='search-input']").send_keys(item)

    search_button = driver.find_element_by_class_name("header-search-button").click()

    driver.implicitly_wait(5)
    for i in range(10): 
        try:
            scrape_search_results(i)
            
            driver.find_element_by_xpath('//div/a[@class="sku-list-page-next"]').click()
            
        except NoSuchElementException:
            # num_page = driver.find_element_by_class_name('sku-list-page-next').click()
            pass

    # driver.implicitly_wait(3)

    driver.quit()

    print("---DONE---")

search_bestBuy('Sony speaker') # <------ search query goes here.


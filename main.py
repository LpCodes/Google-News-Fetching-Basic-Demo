from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def search_news(searchstring):
    # this will auto handel driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    Website = "https://www.google.com/"  # website we are going to open

    # The driver.get method will navigate to a page mentioned by the URL. You need to specify the full URL.

    driver.get(Website)

    print(driver.title, driver.current_url)
    # console_logs = driver.get_log('browser')

    # for i in console_logs:
    #     print(i['message'])

    # driver.execute_script("alert('d')")

    driver.maximize_window()
    search_bar = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[" "2]/input",
    )
    search_bar.clear()
    search_bar.send_keys(searchstring)
    googlesearchbutton = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div[3]/form/div[1]/div[1]/div[" "3]/center/input[1]",
    )
    googlesearchbutton.click()
    sleep(1)
    print(driver.title, driver.current_url)

    newstab = driver.find_element(
        by=By.XPATH, value='//*[@id="hdtb-msb"]/div[1]/div/div[2]/a'
    )
    newstab.click()
    sleep(1)
    print(driver.title, driver.current_url)

    url = driver.current_url
    response = driver.page_source

    html_soup = BeautifulSoup(response, "html.parser")
    sleep(1)
    # print(html_soup.prettify())
    news_div = html_soup.find_all("div", class_="xuvV6b BGxR7d")
    # first_div = news_div[0]
    All_div = news_div
    # print(first_div.prettify())
    Newstitle = []  # List to store name of the product
    Source = []  # List to store price of the product
    summarynews = []  # List to store rating of the product
    date = []
    for i in All_div:
        news_source = i.find("div", class_="CEMjEf NUnG9d")
        print(news_source.get_text())
        Source.append(news_source.get_text())
        heading = i.find("div", class_="mCBkyc y355M ynAwRc MBeuO nDgy9d")
        print(heading.get_text())
        Newstitle.append(heading.get_text())
        summary = i.find("div", class_="GI74Re nDgy9d")
        print(summary.get_text())
        summarynews.append(summary.get_text())
        time = i.find("div", class_="OSrXXb ZE0LJd")
        date.append(time.get_text())
        print(time.get_text())

    df = pd.DataFrame(
        {
            "News": Newstitle,
            "News Source": Source,
            "Summary": summarynews,
            "Date Published": date,
        }
    )
    df.to_csv("GoogleNews.csv", index=False, errors="ignore")

    print("Done")

    driver.quit()


search_news("india post")

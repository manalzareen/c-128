from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Webdriver
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    try:
        page= requests.get(hyperlink)
        soup= BeautifulSoup(page.contenet , "html.parser")
        temp_list=[]
        for  tr_tag in soup.find_all("tr", attrs =  {"class"  : "fact_row" }):
            all_tags = tr_tag.find_all("td")
            for i in all_tags:
                try:
                    temp_list.append(i.find_all("div" , attrs = { "class" : "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

planet_df_1 = pd.read_csv("updated_scraped_data.csv")
# Call method
for index, row in planet_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row["hyperlink"])
    print(f"Data Scraping at hyperlink {index+1} completed")

#print(new_planets_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_planets_data:
    replaced = []
    for i in row:
        i = i.replace("\n" , "")
        replaced.append(i)
    scraped_data.append(replaced)
print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

from selenium import webdriver
from selenium.webdriver.common.by import By
# module to wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random   

# Create driver with proxy
def create_driver_with_proxy(proxy):
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')  # Set the proxy server
    chrome_options.add_experimental_option("detach", True)
    # Update the path to your ChromeDriver if necessary
    #service = Service('/path/to/chromedriver')

    driver = webdriver.Chrome(options=chrome_options)
    return driver
# Create driver witout proxy
def create_driver_without_proxy():
    chrome_options = webdriver.ChromeOptions()

    # Add option so browser is kept open
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # set driver 
    driver = webdriver.Chrome(options=options)
    return driver

def create_driver_with_proxy_socks(proxy_address):
    chrome_options = Options()

    # Add SOCKS proxy configuration
    chrome_options.add_argument(f'--proxy-server=socks4://{proxy_address}')

    chrome_options.add_experimental_option("detach", True)
    # Path to your ChromeDriver
    #service = Service('/path/to/chromedriver')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# List of proxies http
proxies = [ "http://5.182.34.194:80", "http://5.182.34.77:80", "http://5.182.34.194:80" ]
# List of socks 4 proxies
proxies_socks4 = ["92.204.135.37:52015", "194.195.122.51:1080", "92.204.135.37:39861", "92.205.110.47:59307"]
#driver = create_driver_with_proxy(proxies[0])
#driver = create_driver_without_proxy()
# 
#driver = create_driver_with_proxy_socks("92.204.135.37:52015")
#
page_index = 11

data = pd.DataFrame(columns=['Name', 'Website', 'Description'])

while page_index <= 20:
    #time.sleep(random.uniform(1, 20)) 
    site2 = f"https://en.paperjam.lu/guide?page={str(page_index)}&refinementList%5Bkind%5D%5B0%5D=Soci%C3%A9t%C3%A9"

    driver=create_driver_without_proxy()
    # if page_index > 0 and page_index < 10 :
    #     driver=create_driver_without_proxy()
    # elif page_index >=10 and page_index < 20:
    #     driver= create_driver_with_proxy_socks(proxies_socks4[0])
    #
    # elif page_index >=20 and page_index < 30:
    #     driver= create_driver_with_proxy_socks(proxies_socks4[1])
    # elif page_index >=30 and page_index < 40:
    #     driver= create_driver_with_proxy_socks(proxies_socks4[2])
    # elif page_index >=40 and page_index < 50:
    #     driver= create_driver_with_proxy_socks(proxies_socks4[3])
    # elif page_index >=50 and page_index < 60:
    #     driver= create_driver_without_proxy()
    driver.get(site2)
    # Cookie PopUp Handling
    try:
        cookie_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'))
    )
        cookie_popup.click()
    except Exception as e:
        print('No Pop up here') 
    

    # Locate all elements with the class 'company-card__content'
    company_cards = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CLASS_NAME, "company-card__content"))
)
    # The trick if to fetch twice to account for DOM variation?
    # Fetch all company cards initially
    company_cards = driver.find_elements(By.CLASS_NAME, "company-card__name")
    all_company_info = []

    for index, card in enumerate(company_cards):
        company_info = []

        # Locate all elements with the class 'company-card__name'
        company_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "company-card__name"))
    )
        # Re-fetch the company cards on each iteration to avoid stale references
        company_cards = driver.find_elements(By.CLASS_NAME, "company-card__name")
        card = company_cards[index]  # Access the current card

        # Click on the current card to navigate to the company Card
        card.click()
        # scrapping logic on paperjam site of company    
        # we get the name from the cards
        name = driver.find_element(By.CLASS_NAME, "guide-introduction-card__info__title").text
        company_info.append(name)
        # Locate the list containing the guide info
        guide_list = driver.find_element(By.CLASS_NAME, "guide-info__list")

        # Find all <a> tags within the list
        links = guide_list.find_elements(By.TAG_NAME, "a")

        # Extract and print the href attribute for each link
        linkslist = []
        for link in links:
            href = link.get_attribute("href")
            # Check if href starts with http or https, and does not contain excluded substrings
            if href and href.startswith(("http://", "https://")) and not any(excluded in href for excluded in ["flickr","linkedin","twitter", "facebook", "instagram", "youtube", "tiktok"]):

                ''.join(linkslist)
                linkslist.append(href)
        try:
            company_info.append(linkslist[0])    
        
        except:
            company_info.append(None)
    # get the description of the company

        # try block to check if data is present
        try:
            # Locate the guidePrincipalInfo section
            guide_info_description = driver.find_element(By.CLASS_NAME, "guide-info__description")
            # text_content = guide_principal_info.text  
            text_content = guide_info_description.text
            company_info.append(text_content)
        except Exception as e:
            print("no description")
            company_info.append(None)
            
        print(company_info)
        # convert list into 2d list
        company_info = [company_info]
        # convert the array to a DataFrrame and append it
        new_rows = pd.DataFrame(company_info, columns=["Name", "Website", "Description"])
        data = pd.concat([data, new_rows], ignore_index=True)
        #all_company_info.append(company_info)

        driver.back()
    driver.quit()

    #df = pd.DataFrame(all_company_info, columns=["Name", "Website", "Description"])
    page_index+=1
# Initialize headers for df
data.to_excel("output2.xlsx")
print(data)


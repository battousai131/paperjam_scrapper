from selenium import webdriver
from selenium.webdriver.common.by import By
# module to wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# Add option so browser is kept open
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
# set driver 
driver = webdriver.Chrome(options=options)
# Paperjam url with only companies ticked
#
page_index = 1
site = "https://en.paperjam.lu/guide?refinementList%5Bkind%5D%5B0%5D=Soci%C3%A9t%C3%A9"


while page_index <= 10:
    
    site2 = f"https://en.paperjam.lu/guide?page={str(page_index)}&refinementList%5Bkind%5D%5B0%5D=Soci%C3%A9t%C3%A9"
    driver.get(site2)
    try:
        cookie_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="onetrust-accept-btn-handler"]'))
    )
        cookie_popup.click()
    except Exception as e:
        print('No Pop up here') 
# Locate all elements with the class 'company-card__content'
    company_cards = driver.find_elements(By.CLASS_NAME, "company-card__content")

# The trick if to fetch twice to account for DOM variation?
# Fetch all company cards initially
    all_company_info = []

    for index, card in enumerate(company_cards):
        company_info = []
        company_cards = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "company-card__name"))
    )


        # Re-fetch the company cards on each iteration to avoid stale references
        company_cards = driver.find_elements(By.CLASS_NAME, "company-card__name")
        card = company_cards[index]  # Access the current card

        # Click on the current card to navigate
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

                linkslist.append(href)
                ''.join(linkslist)
            #implement quick check if link list is not 3
        company_info.append(linkslist)    
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
        #print(company_info)
        all_company_info.append(company_info)
        driver.back()
        
    page_index+=1
# Initialize headers for df
df = pd.DataFrame(all_company_info, columns=["Name", "Website", "Description"])
df.to_excel("output_1_10.xlsx")
print(df)
driver.quit()


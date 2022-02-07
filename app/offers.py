#!/usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from mail import send_email
from gspread_library import get_data_from_gsheet
import time
import os


YOUR_SPREADSHEET_LINK = os.environ.get('SPREADSHEET')
# instantiate a chrome options object so you can set the size and headless preference
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

# driver = webdriver.Chrome(options=chrome_options)

def get_remote_driver():
    # Set host to externally accessible web server address
    # host = socket.gethostbyname(socket.gethostname())
    # Instantiate the remote WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    selenium = webdriver.Remote(
        #  Set to: htttp://{selenium-container-name}:port/wd/hub
        #  In our example, the container is named `selenium`
        #  and runs on port 4444
        "http://selenium:4444/wd/hub",
        options=chrome_options
    )
    selenium.implicitly_wait(5)
    return selenium

if __name__ == "__main__":
    print("getting remote driver...")
    driver = get_remote_driver()
    driver.get("https://leagueoflegends.fandom.com/es/wiki/Ofertas")
    #Wait 5 seconds until page load
    time.sleep(5)
    print("getting data from spreadsheet...")
    skins = get_data_from_gsheet(YOUR_SPREADSHEET_LINK)

    print("looking for skings at the page...")
    foundIt = False
    found_skins = []
    for skin in skins:
        try:
            xpath = f'//div[@data-champion="{skin["champion"]}" and contains(@data-skin,"{skin["skin"]}")]'
            if driver.find_element_by_xpath(xpath).is_displayed():
                # Take a screenshot just once
                if foundIt == False:
                    string = f'''document.evaluate(`{xpath}`,
                                        document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).
                                        singleNodeValue.scrollIntoView({{block:"center"}});'''
                    driver.execute_script(string)
                    driver.save_screenshot('screenshot.png')
                    foundIt = True
                found_skins.append(skin)
        except Exception as e:
            pass

    # Send me the screenshot and the list of found skins if we got someone
    if foundIt == True:
        send_email(found_skins)
        print('checa your email julio :3')
    else:
        print("""None skin was found :'(""")
    driver.close()
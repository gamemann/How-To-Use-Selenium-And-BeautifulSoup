from base.cmdline import ParseCmdLine, PrintCmdLine
from base.driver import SetupDriver
from base.utils import ExitProgram

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

def main():
    print("Starting simple-image-collector...")

    # Parse command line arguments.
    print("Parsing arguments...")
    
    try:
        cmd = ParseCmdLine()
    except Exception as e:
        print("Failed to parse command line due to exception.")
        print(e)
        
        ExitProgram(1)
        
    # Check if we need to print command line options.
    if cmd["list"]:
        PrintCmdLine(cmd)
        
        ExitProgram(0)
        
    # Map command line arguments to variables.
    binary = cmd["binary"]
    ua = cmd["ua"]
    site = cmd["site"]
        
    # Setup Selenium driver.
    print("Setting up Selenium driver...")
    
    try:
        driver = SetupDriver(binary, ua)
    except Exception as e:
        print("Failed to setup Selenium driver...")
        print(e)
        
        ExitProgram(1)
        
    # Parse website.
    print(f"Parsing website '{site}'...")
    
    try:
        driver.get(site)
    except Exception as e:
        print(f"Failed to parse website '{site}'...")
        print(e)
        
        ExitProgram(1, driver)
        
    # Wait until images are loaded using WebDriverWait and wait until elements with class name 'image-row' are visible.
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, "image-row"))
        )
    except Exception as e:
        print(f"Failed to locate elements with 'image-row' class name within 10 seconds. Make sure you're using 'testwebsite01'...")
        print(e)
        
        ExitProgram(1, driver)
        
    # Parse web page with BeautifulSoup4.
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print("Failed to parse website's contents using BeautifulSoup4...")
        print(e)
        
        ExitProgram(1, driver)
    
    # Parse each 'image-row' element and extract the source of the first 'img'.    
    imgUrls = []
    
    try:
        # Retrieve all 'div' tags with class set 'image-row'.
        rows = soup.findAll("div", class_="image-row")
        
        if not rows or len(rows) < 1:
            print("Failed to parse image rows. 'rows' is falsey or has a length of 0.")
            
            ExitProgram(1, driver)
            
        # Loop through each element.
        for row in rows:
            # Retrieve the first img element and check.
            img = row.find("img")
            
            if not img:
                print("Failed to parse image. 'img' is falsey.")
                
                continue
            
            # Retrieve source.
            src = img.get("src")
            
            if not src:
                print("Failed to parse image. 'src' is falsey.")
                
                continue
            
            # Append to image URLs.
            imgUrls.append(src)
        
        # Print the image URLs we've found.
        print("Found the following image URLs.")
        
        for url in imgUrls:
            print(f"\t- {url}")
    except Exception as e:
        print("Failed to parse image rows due to exception.")
        print(e)
        
        ExitProgram(1, driver)
        
    print("Exiting...")
    
    ExitProgram(0, driver)
    
if __name__ == "__main__":
    main()
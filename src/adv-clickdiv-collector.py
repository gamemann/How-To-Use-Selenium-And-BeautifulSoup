from base.cmdline import ParseCmdLine, PrintCmdLine
from base.driver import SetupDriver
from base.utils import ExitProgram

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

def main():
    
    print("Starting adv-clickdiv-collector...")

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
        
        ExitProgram()
        
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
        
    # Wait until clickable dividers are loaded using WebDriverWait and wait until elements with class name 'clickDiv-row' are visible.
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, "clickDiv-row"))
        )
    except Exception as e:
        print(f"Failed to locate elements with 'clickDiv-row' class name within 10 seconds. Make sure you're using 'testwebsite01'...")
        print(e)
        
        ExitProgram(1, driver)
        
    # We need to click all clickable dividers now before parsing through BeautifulSoup4.
    try:
        # Find elements in Selenium with class name 'clickDiv-row'.
        rows = driver.find_elements(By.CLASS_NAME, "clickDiv-row")
        
        # Check.
        if not rows or len(rows) < 1:
            print("Failed to parse clickable div rows. 'rows' is falsey or has a length of 0.")
            
            ExitProgram(1, driver)
            
        # Loop through each element found.
        for row in rows:
            # Click the element.
            row.click()
    except Exception as e:
        print("Failed to click clickable dividers due to exception.")
        print(e)
        
        ExitProgram(1, driver)
        
    # Parse web page with BeautifulSoup4.
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print("Failed to parse website's contents using BeautifulSoup4...")
        print(e)
        
        ExitProgram(1, driver)
    
    # Parse each 'clickDiv-row' element, click it, and extract the clickable divider's title and hidden contents.    
    clickDivs: list[dict[str, str]] = []
    
    try:
        # Retrieve all 'div' tags with class set 'clickDiv-row'.
        rows = soup.findAll("div", class_="clickDiv-row")
        
        if not rows or len(rows) < 1:
            print("Failed to parse clickable div rows. 'rows' is falsey or has a length of 0.")
            
            ExitProgram(1, driver)
            
        # Loop through each element.
        for row in rows:
            # Parse first 'h2' tag and check.
            h2 = row.find("h2")
            
            if not h2:
                print("Failed to parse clickable div. 'h2' is falsey.")
                
                continue
            
            # Extract text from 'h2' tag as title.
            title = h2.text
            
            # Extract the first 'div' tag.
            div = row.find("div")
            
            if div is None:
                print("Failed to parse clickable div. 'div' is falsey.")
                
                continue
            
            # Extract text from 'div' tag as contents.
            contents = div.text
            
            # Append to clickable dividers list.
            clickDivs.append({
                "title": title,
                "contents": contents
            })
            
        # Print the clickable dividers we've found.
        print("Found the following clickable dividers.")
        
        for index, clickDiv in enumerate(clickDivs):
            print(f"\ClickDiv #{index + 1}")
            print(f"\t\tTitle => {clickDiv['title']}")
            print(f"\t\tDescription => {clickDiv['contents']}")
    except Exception as e:
        print("Failed to clickable div rows due to exception.")
        print(e)
        
        ExitProgram(1, driver)
        
    print("Exiting...")
    
    ExitProgram(0, driver)
    
if __name__ == "__main__":
    main()
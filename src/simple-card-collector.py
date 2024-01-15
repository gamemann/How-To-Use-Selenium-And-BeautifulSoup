from base.cmdline import ParseCmdLine, PrintCmdLine
from base.driver import SetupDriver
from base.utils import ExitProgram

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

def main():
    print("Starting simple-card-collector...")

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
        
    # Wait until cards are loaded using WebDriverWait and wait until elements with class name 'card-row' are visible.
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_any_elements_located((By.CLASS_NAME, "card-row"))
        )
    except Exception as e:
        print(f"Failed to locate elements with 'card-row' class name within 10 seconds. Make sure you're using 'testwebsite01'...")
        print(e)
        
        ExitProgram(1, driver)
        
    # Parse web page with BeautifulSoup4.
    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print("Failed to parse website's contents using BeautifulSoup4...")
        print(e)
        
        ExitProgram(1, driver)
    
    # Parse each 'card-row' element and extract the card's title and description.    
    cards: list[dict[str, str]] = []
    
    try:
        # Retrieve all 'div' tags with class set 'card-row'.
        rows = soup.findAll("div", class_="card-row")
        
        if not rows or len(rows) < 1:
            print("Failed to parse card rows. 'rows' is falsey or has a length of 0.")
            
            ExitProgram(1, driver)
            
        # Loop through each element.
        for row in rows:
            # Retrieve the first 'h2' tag which represents the card title.
            h2 = row.find("h2")
            
            if not h2:
                print("Failed to parse card. 'h2' is falsey.")
                
                continue
            
            # Extract text from 'h2' tag as title.
            title = h2.text
            
            # Retrieve the first 'p' tag which represents the card description.
            p = row.find("p")
            
            if not p:
                print("Failed to parse card. 'p' is falsey.")
                
                continue
            
            # Extract text from 'p' tag as description.
            description = p.text
            
            # Add to cards list.
            cards.append({
                "title": title,
                "description": description
            })
        
        # Print the cards we've found.
        print("Found the following cards.")
        
        for index, card in enumerate(cards):
            print(f"\tCard #{index + 1}")
            print(f"\t\tTitle => {card['title']}")
            print(f"\t\tDescription => {card['description']}")
    except Exception as e:
        print("Failed to parse card rows due to exception.")
        print(e)
        
        ExitProgram(1, driver)
        
    print("Exiting...")
    
    ExitProgram(0, driver)
    
if __name__ == "__main__":
    main()
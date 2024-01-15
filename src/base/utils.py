from sys import exit

from selenium.webdriver import Firefox

def ExitProgram(ret: int = 0, driver: Firefox = None):
    if driver:
        driver.quit()
        
    exit(ret)
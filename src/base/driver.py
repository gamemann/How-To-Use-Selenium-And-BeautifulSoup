from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox

def SetupDriver(binary: str, ua: str) -> Firefox:
    # Initialize options.
    opts = Options()
    
    # Set headless and no sandbox flags.
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    
    # Set user agent.
    opts.set_preference("general.useragent.override", ua)
    
    # Create service.
    service = Service(executable_path = binary)
    
    # Create driver.
    driver = Firefox(
        options = opts,
        service = service
    )
    
    return driver
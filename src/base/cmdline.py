import argparse

def ParseCmdLine() -> dict[str, any]:
    # Initialize argument parser.
    parser = argparse.ArgumentParser()
    
    # Add binary argument.
    parser.add_argument("-b", "--binary",
        help = "The path to the Geckodriver binary file.",
        default = "/usr/bin/geckodriver" 
    )
    
    # Add site argument.
    parser.add_argument("-s", "--site",
        help = "The full URL of the website to parse and extract information from.",
        default = "http://localhost:3000"
    )
    
    # Add user agent argument.
    parser.add_argument("-u", "--ua",
        help = "The web browser's user agent to use when sending requests",
        default = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"                    
    )
    
    # Add list argument.
    parser.add_argument("-l", "---list",
        help = "Prints the command line values and exits.",
        default = False                    
    )
    
    # Parse all arguments.
    args = parser.parse_args()
    
    # Return arguments in dict.
    return {
        "binary": args.binary,
        "site": args.site,
        "ua": args.ua,
        "list": args.list
    }
    
def PrintCmdLine(cmd: dict[str, any]):
    print("Command Line")
    
    print(f"\tBinary => {cmd['binary']}")
    print(f"\tSite => {cmd['site']}")
    print(f"\tUser Agent => {cmd['ua']}")
    
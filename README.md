This repository will show how to use [Selenium](https://www.selenium.dev/) paired with [Beautiful Soup (V4)](https://pypi.org/project/beautifulsoup4/) in Python (3+) to parse and extract data from websites. I've included example(s) of using JavaScript as well (e.g. button clicks to open menus and then extract more hidden data). I also plan on making blog articles under [Deaconn](https://deaconn.net/) using these examples in the future!

These tools are commonly used with web browser automation, web scraping, and development tests. Additionally, you can use the combination of these tools in other projects such as creating a follow bot (obviously using at your own risk)!

## What Is Selenium & Beautiful Soup?
**Selenium** is a powerful tool for controlling web browsers through programs and performing browser automation/tasks. A driver is included for most web browsers and a wide range of programming languages are supported!

**Beautiful Soup** is a Python library for pulling data out of HTML and XML files. It parses anything you give it, and does the tree traversal stuff for you!

## Requirements & Setup
I've created and tested the programs made in this repository on a Debian 12 virtual machine I have running on one of my [home servers](https://github.com/gamemann/Home-Lab?tab=readme-ov-file#two-powerball). While I don't have specific instructions for setting up this repository on non-Debian/Ubuntu-based systems, there shouldn't be many changes you need to make to the instructions below. In fact, it may be easier since you may not have to worry about your OS's package manager handling the Python installation.

### Debian/Ubuntu-Based Systems
Debian/Ubuntu-based systems typically use the `apt` package manager to manage the server's Python installation and its libraries. This is fine in most cases, but sometimes there are packages that aren't included with `apt` and when using the `pip` or `pip3` commands to install the package, you'll receive an error like below.

```bash
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

You could pass the `--break-system-packages` flag to the `pip` or `pip3` commands, but as stated in the error, this risks breaking packages in your global Python installation. A solution to this is using virtual Python environments which is detailed below.

If you do want to use `apt` to manage the packages, you can install Selenium and BeautifulSoup4 using the command below.

```bash
sudo apt install -y python3-bs4 python3-selenium
```

### Virtual Python Environments
I personally recommend creating a virtual Python environment so that you don't risk breaking your Python installation if you need to install a package that isn't included in the `apt` package manager. It is pretty easy to create a virtual environment as well. In our case, we can do so by using the command below.

```bash
python3 -m venv venv/
```

This will create a `venv/` directory in your current working directory. Afterwards, you will want to source `venv/bin/activate` and then you will be able to use the `pip` or `pip3` commands to install the required packages.

```bash
source venv/bin/activate
```

I've also included a `requirements.txt` file which allows you to easily install the required packages using the `pip` or `pip3` commands. You may use the command below.

```bash
pip3 install -r requirements.txt
```

**Note** - The `requirements.txt` file includes `beautifulsoup4` (version `4.12.2`) and `selenium` (version `4.16.0`). There may be updates available to these packages, but these are the versions I've made this repository with.

### Firefox & Geckodriver
In this repository, we use Selenium's Firefox driver paired with [geckodriver](https://github.com/mozilla/geckodriver). I'd recommend heading to the [releases page](https://github.com/mozilla/geckodriver/releases) and downloading the latest. Otherwise, you can use the version I've tested below.

```bash
# Download version '0.34.0' for Linux 64-bit.
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz

# Uncompress and extract the file using the 'tar' command.
tar -xzvf geckodriver-v0.34.0-linux64.tar.gz

# Move to '/usr/bin' using sudo/root.
sudo mv geckodriver /usr/bin
```

You'll also want to download Firefox. You can do so using `apt` below.

```
sudo apt install -y firefox-esr
```

## Website Setup & Running
The website we've made to test the Python programs utilize [React](https://react.dev/) and [Node.js](https://nodejs.org/en). The website's source code is located in the [`site/`](./site) directory.

### Requirements
You will need to install **Node.js** and **NPM** onto your system. You can read [this guide](https://nodejs.org/en/download/package-manager/) on how to install these packages using a package manager. You can use the following command to install Node.js and NPM using the `apt` package manager. However, I did want to note that the standard repositories included in the `apt` package manager are fairly old (stable), but they should work for the websites in this repository.

```bash
sudo apt install -y nodejs npm
```

### Installing Packages
After installing Node.js and NPM, you can change your directory to our website using the `cd site/` command and run the following to install the needed packages via NPM.

```bash
npm install
```

Afterwards, you can run the following command to start the web development server.

```bash
npm start
```

By default, the website should be listening at [http://localhost:3000](http://localhost:3000). However, if you want to change the bind IP or port, you can set the `HOST` and `PORT` environmental variables. Here's an example.

```bash
HOST=0.0.0.0 PORT=3001 npm start
```

If you use a different host or port, please make sure to specify this in the Python program's command line. Read **Command Line Usage** for more information.

## Command Line Usage
Each Python program utilizes [`src/base/cmdline.py`](./src/base/cmdline.py) to parse the command line arguments. Arguments are listed below.

* `-b --binary` - The path to the Geckodriver binary file (default => `/usr/bin/geckodriver`).
* `-s --site` - The full URL of the website to parse and extract information from (default => `http://localhost:3000`).
* `-u --ua` - The web browser's user agent to use when sending requests (default => `Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0`).

## Programs
All Python programs are located in the [`src/`](./src) directory. You may execute them using the following command. Please make sure you have the website started in another terminal!

```bash
python3 src/<program>.py
```

Here's a list of programs we've made so far!

### [`simple-image-collector.py`](./src/simple-image-collector.py)
This Python program parses our website and extracts all image sources inside of elements with the class name `image-row`.

The expected output is the following.

```bash
$ python3 src/simple-image-collector.py 
Starting simple-image-collector...
Parsing arguments...
Setting up Selenium driver...
Parsing website 'http://localhost:3000'...
Found the following image URLs.
        - /images/testimage01.png
        - /images/testimage02.png
        - /images/testimage03.png
        - /images/testimage04.png
Exiting...
```

### [`simple-card-collector.py`](./src/simple-card-collector.py)
This Python program parses our website and extracts the title and description of all elements with the class name `card-row`. The title is found inside of the `<h2>` tag while the description is found inside of the `<p>` tag inside the card row element.

The expected output is the following.

```bash
$ python3 src/simple-card-collector.py 
Starting simple-card-collector...
Parsing arguments...
Setting up Selenium driver...
Parsing website 'http://localhost:3000'...
Found the following cards.
        Card #1
                Title => Card Title #1
                Description => This is the description of card #1!
        Card #2
                Title => Card Title #2
                Description => This is the description of card #2!
        Card #3
                Title => Card Title #3
                Description => This is the description of card #3!
Exiting...
```

### [`adv-clickdiv-collector.py`](./src/adv-clickdiv-collector.py)
This Python program parses our website, clicks all the dividers with the class name `clickDiv-row`, and then extracts the divider's title and hidden content. This is a more advanced example since it uses JavaScript to click buttons.

The expected output is the following.

```bash
$ python3 src/adv-clickdiv-collector.py
Starting adv-clickdiv-collector...
Parsing arguments...
Setting up Selenium driver...
Parsing website 'http://localhost:3000'...
Found the following clickable dividers.
        ClickDiv #1
                Title => Clickable Div #1
                Description => These are the hidden contents of clickable div #1!
        ClickDiv #2
                Title => Clickable Div #2
                Description => These are the hidden contents of clickable div #2!
        ClickDiv #3
                Title => Clickable Div #3
                Description => These are the hidden contents of clickable div #3!
        ClickDiv #4
                Title => Clickable Div #4
                Description => These are the hidden contents of clickable div #4!
Exiting...
```

## Credits
* [Christian Deacon](https://github.com/gamemann)
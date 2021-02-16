### Download Script

This script takes a list of rawpixel urs in the form of a .csv file and downloads
the image from each.

# Installation

+ Use command (on pycharm) to install dependencies: 

$ py -m pip install -r requirements.txt

+ Ensure that the correct version of chromedriver is in the program files

Can be downloaded from https://chromedriver.chromium.org/downloads

+ Ensure Rawpixel username and password are entered correctly 

+ Enter image file path and path to default downloads folder

## Operation of Script

+ The script will take urls from the urls.csv file required fields being 'title' and 'url'

+ If script has previously downloaded images can enter number for first image filename where prompted in script

+ Initially will open site to log in page and enter username and password and clicklogin.

+ User must manually click login and solve any captcha when prompted. 

+ From here the script will navigate to urls from file, download image, save a copy in the images file and update 'info.csv' with details of filename, title and url for each.

NOTE: After repeated prompting for solving of google CAPTCHA site may block login attempt,
DO NOT RUN REPEATEDLY within small timeframe. The extent and persistence of site blacklisting is not yet known.
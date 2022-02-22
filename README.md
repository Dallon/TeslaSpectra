Tesla Spectra mainly runs on Python!:D

The website is built with Django and the programs that populate the website are built with Python using Selenium as the webscraper. Originally intended as a blog about tesla news the website now is in building stages hopefully to become a hub of news information about Tesla from all over the web such as reddit, twitter, the US Patent Office, tesla news outlets and various tesla websites.

Now on a Debian Linux server and managing the scripts with Crontab, the next step is to separate our website workflow from the computational requirements of our webscrapers. To do that I've created an AWS S3 bucket which will be the connecting repository between the website server. 

The webscrapers connect to local files which are  written to after scraping has taken place and then those files uploaded to overwrite the JSON files in the bucket with new info. The website likewise connects to local JSON files which are written to from the bucket hosted files and then displayed.

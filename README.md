TeslaSpectra is a RESTful website mainly run on Python!

The website(In Development) is built with Django and the programs that populate the website are webscrapers built with Python. Originally intended as a blog about tesla news the website now is in building stages hopefully to become a hub of news information about Tesla from all over the web such as reddit, twitter, the US Patent Office, tesla news outlets etc.

The website and the webscrapers are now on separate Linux virtual machines both connecting to an amazon S3 "hot storage" bucket. The Bucket contains json files which hold the scraped information. Through Boto3, a Python module designed to allow manipulation of files in S3, the scrapers populate local JSON files on Linux VM1 and then replace corresponding JSON files in the S3 bucket. Likewise when a call to the webpage is made the json file in S3 is downloaded into the local JSON file on Linux VM2 which is then displayed as part of the webpage.


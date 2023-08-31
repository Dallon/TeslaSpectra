TeslaSpectra was a RESTful website mainly run on Python!

The website was built with Django and the programs that populate the website are built with Python(Selenium) based web scrapers. Originally intended as a blog about tesla news the website turned into a little automation project. 

The website and the webscrapers are were hosted on separate Linux container instances both connecting to an amazon S3 "hot storage" bucket. The Bucket contained JSON files which hold the scraped information. Through boto3, a Python module designed to allow manipulation of files in S3, the scrapers populate local JSON files on Linux container instance1 and then replace corresponding JSON files in the S3 bucket. Likewise when a call to the webpage is made the json file in S3 is downloaded into the local JSON file on Linux container instance2 which is then displayed as part of the webpage.


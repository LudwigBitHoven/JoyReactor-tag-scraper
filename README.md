# What is joyreactor?
joyreactor.cc is a website for hosting different images. Hosted images are grouped by tags like 'cats', 'anime', 'food', which could intersect with each other
# What is the purpose of the project
The purpose is to allow anyone to scrape images from the website by a specified tag and range. Images could be used for a machine learning or image processing purposes, as well as they could be used for the simple collecting and fulfilling curiosity
# How it works?
Website implements page-based pagination. Serial numbers are assigned to pages and they represent ids `https://joyreactor.cc/tag/MidJourney/66`. I use python's requests and beatifulsoup packages to scrape the data.
# What are the results?
The toxicity in the particularly chosen Vk group is following a normal distribution. 84% of comments were left by the male users. There is no obvious correlation between the neutrality and 'skipness' 
of a message for the dostoevsky library ('skip' is the value showing how hard it was for the dostoevsky model to classify the sentiment). Despite being 15% of the total comments, comments left by 
female users tend to be more positive in the scraped data (roughly by 8 percent more positive). Also, there is no correlation between the amount of comments of a user and the mean value of their toxicity.
# To improve
- Introduce better transliteration
- Migrate visualization from matplotlib to plotly
- Introduce a scraper for getting comments from the chosen Vk group
- Chum up the scraper and the analyzer

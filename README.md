# What is joyreactor?
joyreactor.cc is a website for hosting different images. Hosted images are grouped by tags like 'cats', 'anime', 'food', which could intersect with each other
# What is the purpose of the project
The purpose is to allow anyone to scrape images from the website by a specified tag and range. Images could be used for the machine learning or image processing purposes, as well as they could be used for the simple collecting, researches on the internet culture (there are tons of posts dated by 2009 and earlier) and fulfilling of curiosity
# How it works?
Website implements page-based pagination. Serial numbers are assigned to pages to represent their ids. Each topic have certain range of pages inside of it. To illustrate here is the URL for the content associated with the MidJourney topic `https://joyreactor.cc/tag/MidJourney/66` and as you could guess there are exactly 66 pages of posts on the topic (at least at the moment of writing this text 02/05/2024). Each page has exactly 10 posts with an unfixed amount of media inside. Based on that, I firstly set the range of pages and the topic by the name of the tag. These parameters form the pages, which are then collected by threaded requests and beatifulsoup. For each collected page beatifulsoup extracts the classes `prettyPhotoLink` (or `image` for more older posts) containing direct links to images. Then these images are collected by requests and saved in the relative path `images/ThreadScrape/scraped_{tag_name}_{count}.jpeg`.
# To improve
- Do something with characters in the hexadecimal format being ignored in cmd. `sys.argv` ignores the `%` separator for the characters and something like `https://joyreactor.cc/tag/%D0%98%D0%B3%D1%80%D1%8B` in the argument won't work as it will be mistakengly interpreted as `https://joyreactor.cc/tag/98B3808B`
- Check whether threading gives any benefits in spite of substantial delay between requests. Is it enough to make saving fast enough? Is it enough for the requests to work in the background without blocking the main thread?
- Introduce watermark deletion before saving
- Test on older Python versions
- Test on really big ranges
- Add saving videos in webm format
# In future
- Set it up as a web-service
- Add docker

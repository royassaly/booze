# booze

Purpose:

Getting Scotch prices from the LCBO (Liquor Control Board of Ontario) and SAQ (Société des alcools du Québec). Perfect for those living on the border like Ottawa.

If you know nothing technical, then let me save you some time. If you want to buy:

1. Spirits: SAQ
2. Wine: LCBO
3. Beer: Anywhere in Quebec is cheaper than Ontario.

Or, just open the file "scotch.csv" in any spreadsheet software or text editor.

Technical Workings:

If you are interested in how this works, Scrapy from (Scrapy.org) is a tool that allows you to read a website and extract, or scrape the information that you need. After you scrape it, you can save it to .CSV (Excel friendly), JSON, or any other database. The sky is the limit really.

For this particular interest, a .CSV file will do. This opens nicely in Excel or any other spreadsheet program and let's you see what the LCBO and SAQ have for Scotch, and how much the prices are. Generally speaking, the selection is greater in the SAQ, and the prices are cheaper. A summary of how this code works is:

1. Scrape the LCBO website for Scotch name, price and URL.

$scrapy crawl lcbo -o lcbo.csv

2. Scrape the SAQ website for Scotch name, price and URL.

$scrapy crawl saq -o saq.csv

3. Join the two .CSV files together, removing the header from the 2nd file.

$sed 1d saq.csv > saqnoheader.csv

$cat lcbo.csv saqnoheader.csv > scotch.csv

4. Open the "scotch.csv", sort by title (name of Scotch) and go find your Scotch!

To run the above in one command, clone this project, or download it, and run the command runScotch.sh.

Don't forget to:

$chmod +x runScotch.sh

$./runScotch.sh

if it doesn't work.

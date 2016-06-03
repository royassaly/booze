#/bin/sh
rm saq.csv
rm lcbo.csv
rm saqnoheader.csv
cd /Users/roy/Google\ Drive/code/scraping/booze
scrapy crawl lcbo -o lcbo.csv
scrapy crawl saq -o saq.csv
sed 1d saq.csv > saqnoheader.csv
cat lcbo.csv saqnoheader.csv > scotch.csv



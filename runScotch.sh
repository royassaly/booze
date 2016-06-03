#/bin/sh
rm scotch.csv
cd ./booze
rm saq.csv
rm lcbo.csv
rm saqnoheader.csv
scrapy crawl lcbo -o lcbo.csv
scrapy crawl saq -o saq.csv
sed 1d saq.csv > saqnoheader.csv
cat lcbo.csv saqnoheader.csv > scotch.csv
mv scotch.csv ../

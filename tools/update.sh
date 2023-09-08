mkdir -p ./src/data/csv
mkdir -p ./src/data/json

python ./tools/scrapingTable.py;

node ./tools/convertCsvToJson.js;
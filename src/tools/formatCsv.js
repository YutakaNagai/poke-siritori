import csv from "csvtojson";
import fs from "fs";
import log4js from "log4js";

const targetFileName = "poke";
const csvFilePath = `src/data/csv/${targetFileName}.csv`;
const jsonFilePath = `src/data/json/${targetFileName}.json`;

const logger = log4js.getLogger();
logger.level = "all";

csv()
  .fromFile(csvFilePath)
  .then((rows) => {
    rows = rows.map((row) => {
      return row;
    });
    fs.writeFile(jsonFilePath, JSON.stringify(rows, null, 2), (err) => {
      if (err) {
        logger.warn(`An error occured in generated ${jsonFilePath}.`);
        throw err;
      }
      logger.info("JSON generated.");
    });
  });

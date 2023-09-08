import csv from "csvtojson";
import fs from "fs";
import log4js from "log4js";

const logger = log4js.getLogger();
logger.level = "all";

const targetFileNameList = [
  "poke",
  "tokusei",
  "waza_1",
  "waza_2",
  "waza_3",
  "waza_4",
  "waza_5",
  "waza_6",
  "waza_7",
  "waza_8",
  "waza_9",
  "waza_pae",
  "waza_pla",
];

for (const targetFileName of targetFileNameList) {
  const csvFilePath = `src/data/csv/${targetFileName}.csv`;
  const jsonFilePath = `src/data/json/${targetFileName}.json`;

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
}

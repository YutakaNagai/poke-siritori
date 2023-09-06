import csv
import requests
from bs4 import BeautifulSoup

# スクレイピング後のcsvファイル名とスクレイピング対象のURLを持ったリスト
urlList = [
    [
        "poke",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E4%B8%80%E8%A6%A7",
    ],
    [
        "waza_1",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%B8%80%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_2",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%BA%8C%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_3",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%B8%89%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_4",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%9B%9B%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_5",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%BA%94%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_6",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%85%AD%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_7",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%B8%83%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_pae",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E3%83%94%E3%82%AB%E3%83%96%E3%82%A4)",
    ],
    [
        "waza_8",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E5%85%AB%E4%B8%96%E4%BB%A3)",
    ],
    [
        "waza_pla",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(Pok%C3%A9mon_LEGENDS_%E3%82%A2%E3%83%AB%E3%82%BB%E3%82%A6%E3%82%B9)",
    ],
    [
        "waza_9",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%82%8F%E3%81%96%E4%B8%80%E8%A6%A7_(%E7%AC%AC%E4%B9%9D%E4%B8%96%E4%BB%A3)",
    ],
    [
        "tokusei",
        "https://wiki.xn--rckteqa2e.com/wiki/%E3%81%A8%E3%81%8F%E3%81%9B%E3%81%84%E4%B8%80%E8%A6%A7",
    ],
]

print("\033[34m" + "[INFO]: Scraping Start." + "\033[0m")
for urlSet in urlList:
    try:
        response = requests.get(urlSet[1])

        soup = BeautifulSoup(response.content, "html5lib")

        table = soup.findAll("table")[0]
        rows = table.findAll("tr")
        # 文字化け回避のためShift-JISで保存
        with open(
            "src/util/csv/%s.csv" % (urlSet[0]), "w", encoding="cp932"
        ) as file:
            writer = csv.writer(file)
            for row in rows:
                csvRow = []
                for cell in row.findAll(["td", "th"]):
                    # cp932に変換不可な文字を置換
                    csvRow.append(cell.get_text().replace("\u2014", ""))
                print(csvRow)
                writer.writerow(csvRow)
        print(
            "\033[34m"
            + "[INFO]: The file '%s.csv' was successfully created."
            % (urlSet[0])
            + "\033[0m"
        )
    except:
        import traceback

        print(
            "\033[31m"
            + "[ERROR]: An error occured in creating '%s.csv'" % (urlSet[0])
            + "\033[0m"
        )
        traceback.print_exc()

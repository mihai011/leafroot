from bs4 import BeautifulSoup
from tqdm import tqdm
import cfscrape
import csv
from concurrent.futures import ThreadPoolExecutor


def get_html(scraper, base_url):

    return scraper.get(base_url).content

def find_airport_code_city(code):

    base_url = "https://www.nationsonline.org/oneworld/IATA_Codes/IATA_Code_{}.htm".format(
        code[0])

    try:
        scraper = cfscrape.create_scraper()
        data = get_html(scraper, base_url)
        soup = BeautifulSoup(data, features="html.parser")
        table_rows = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('summary')
                               and tag['summary'] == "IATA Airport-Codes {}".format(code[0])).find_all("tr")

        for row in table_rows:
            cells = row.find_all("td")
            if cells[0].get_text() == code:
                return code, cells[1].get_text()

    except Exception:
        return code, False
    
    return code, False


def search(codes):

    code_cities = {}
    with ThreadPoolExecutor(max_workers=24) as executor:
        for res in list(tqdm(executor.map(lambda code: find_airport_code_city(code), codes), total=len(codes))):
            code_cities[res[0]] = res[1]
        

    return code_cities


if __name__ == '__main__':

    airport_codes = []
    with open('/workspace/scripts/data.csv', newline='') as csvfile:
        data_reader = csv.reader(csvfile, delimiter=',')
        next(data_reader)
        for row in data_reader:
            airport_codes.append(row[2])

    responses = search(airport_codes)
    not_found = 0
    for code in responses.keys():
        if responses[code] == False:
            not_found += 1

    print(not_found)

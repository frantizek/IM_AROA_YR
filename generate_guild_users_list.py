import re
import requests
from bs4 import BeautifulSoup
import csv

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines

def search_telegram_user(user_name, dict_of_users):
    if user_name in dict_of_users.keys():
        print("match")
        return "https://t.me/{}".format(dict_of_users[user_name].replace("@", ""))
    else:
        return " "

def main():
    users = []
    d_users = {}
    filename = "IM_AROA_YR.txt"
    lines = read_file(filename)
    for line in lines:
        user_data = line.strip().split(" ", 1)
        users.append(user_data)
        d_users[user_data[1].lower()] = user_data[0].lower()

    print(users)

    csv_header = ['Usuario swgoh', 'Codigo aliado', 'comando kryat', 'Usuario Telegram' ]

    with open('gremio_aroa.csv', 'w', encoding="UTF8", newline='') as f:
        writer = csv.writer(f, delimiter=',')

        # write the header
        writer.writerow(csv_header)

        # This is the current url used at swgoh.gg for the guild
        # The page is usually refreshed so we will used to extract the guild members
        im_aroa_yr_url = "https://swgoh.gg/g/pTtJHHuYQcSMinxQXXZJgA/"

        page = requests.get(im_aroa_yr_url, timeout=10, verify=True)

        soup = BeautifulSoup(page.content, "html.parser")

        table = soup.find('table')

        headers = [header.text for header in table.find_all('th')]
        results = [{headers[i]: cell for i, cell in enumerate(row.find_all('td'))}
                   for row in table.find_all('tr')]

        for result in results:
            if "Name" in result.keys():
                # print(result['Name'])
                tag_converted_to_str = str(result['Name'])
                username_swgoh = re.search(r'<div><strong>(.*?)</strong></div>', tag_converted_to_str).group(1)
                allycode_swgoh = re.search(r'<a href="/p/(.*?)/">', tag_converted_to_str).group(1)
                kryat = "/krayt max allycode: {}".format(allycode_swgoh)
                telegram = search_telegram_user(username_swgoh.lower(), d_users)

                # write the data
                writer.writerow([username_swgoh, allycode_swgoh, kryat, telegram])

    # close the file
    f.close()


if __name__ == "__main__":
    main()

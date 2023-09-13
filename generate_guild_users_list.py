"""Imports needed to complete the script tasks.""" 
import re
import csv
import requests
from bs4 import BeautifulSoup


def read_file(filename):
    """Open the file in read mode, returns the lines."""
    with open(filename, "r", encoding="utf-8") as this_file:
        lines = this_file.readlines()
    return lines

def search_telegram_user(user_name, dict_of_users):
    """Using the dictionary, return the link with the user."""
    if user_name in dict_of_users.keys():
        return f"https://t.me/{dict_of_users[user_name].replace('@', '')}"
    else:
        return " "

def main():
    """Lets create a list with the latest guils members."""
    d_users = {}
    filename = "IM_AROA_YR.txt"
    lines = read_file(filename)
    for line in lines:
        user_data = line.strip().split(" ", 1)
        d_users[user_data[1].lower()] = user_data[0].lower()

    csv_header = ['Usuario swgoh', 'Codigo aliado', 'comando kryat', 'Usuario Telegram' ]

    with open('gremio_aroa.csv', 'w', encoding="UTF8", newline='') as this_file:
        writer = csv.writer(this_file, delimiter=',')

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
                tag_converted_to_str = str(result['Name'])
                username_swgoh = re.search(r'<div><strong>(.*?)</strong></div>', tag_converted_to_str).group(1)
                allycode_swgoh = re.search(r'<a href="/p/(.*?)/">', tag_converted_to_str).group(1)
                kryat = f"/krayt max allycode: {allycode_swgoh}"
                telegram = search_telegram_user(username_swgoh.lower(), d_users)

                # write the data
                writer.writerow([username_swgoh, allycode_swgoh, kryat, telegram])

    # close the file
    this_file.close()


if __name__ == "__main__":
    main()

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
        return dict_of_users[user_name].replace('@', '')
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

    csv_header = ['Codigo de aliado', 'Usuario en SWGOH', 'Usuario en Telegram', 'comando kryat en Discord']

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

        acode_l = []
        uswgoh_l = []
        telegram_l = []
        message_me_l = []
        kryat_l = []

        headers = [header.text for header in table.find_all('th')]
        results = [{headers[i]: cell for i, cell in enumerate(row.find_all('td'))}
                   for row in table.find_all('tr')]

        for result in results:
            if "Name" in result.keys():
                tag_converted_to_str = str(result['Name'])
                username_swgoh = re.search(r'<div><strong>(.*?)</strong></div>',
                                            tag_converted_to_str).group(1)
                allycode_swgoh = re.search(r'<a href="/p/(.*?)/">', tag_converted_to_str).group(1)
                kryat = f"/krayt max allycode: {allycode_swgoh}"
                telegram = search_telegram_user(username_swgoh.lower(), d_users)
                
                acode_l.append(allycode_swgoh)
                uswgoh_l.append(username_swgoh)
                telegram_l.append(telegram)
                message_me_l.append(f"https://t.me/{telegram}")
                kryat_l.append(kryat)

                # write the data
                writer.writerow([allycode_swgoh, username_swgoh, telegram, kryat])



    # close the file
    this_file.close()

    import plotly.graph_objects as go

    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'

    fig = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Ally Code</b>','<b>Username SWGOH</b>','<b>Telegram User</b>','<b>Send Telegram Message</b>','<b>Kryat command</b>'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left','center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
        acode_l,
        uswgoh_l,
        telegram_l,
        message_me_l,
        kryat_l],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*50],
        align = ['left', 'center'],
        font = dict(color = 'darkslategray', size = 11)
        ))
    ])

    fig.show()


if __name__ == "__main__":
    main()

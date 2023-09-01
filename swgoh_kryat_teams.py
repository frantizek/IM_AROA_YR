from urllib.request import Request, urlopen
from urllib.error import URLError
import re




with open('aroa_current.html') as f:
    while True:
        line = f.readline()
        if not line:
            break

        if '<a href=\"/p/' in line:
            # print(line.strip())
            # print(re.findall(r'\d', line))
            print(re.search(r'(\d{9})', line).group())
            # print("/krayt max allycode: {}".format(re.search(r'(\d{9})', line).group()))
            # swgoh_gg_profile_url = "https://swgoh.gg/p/{}/".format(re.search(r'(\d{9})', line).group())
            # print(swgoh_gg_profile_url)
            #
            # req = Request(swgoh_gg_profile_url)
            # try:
            #     response = urlopen(req)
            # except URLError as e:
            #     if hasattr(e, 'reason'):
            #         print('We failed to reach a server.')
            #         print('Reason: ', e.reason)
            #     elif hasattr(e, 'code'):
            #         print('The server couldn\'t fulfill the request.')
            #         print('Error code: ', e.code)
            # else:
            # # everything is fine
            #
            #     print(response)
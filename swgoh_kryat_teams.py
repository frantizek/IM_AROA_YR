import re
import requests
from bs4 import BeautifulSoup


# This is the current url used at swgoh.gg for the guild
# The page is usually refreshed so we will used to extract the guild members
im_aroa_yr_url = "https://swgoh.gg/g/pTtJHHuYQcSMinxQXXZJgA/"

# request_site = Request(im_aroa_yr_url, headers={"User-Agent": "Mozilla/5.0"})
# webpage = urlopen(request_site).read()
# print(webpage)



# with open('aroa_current.html') as f:
#     while True:
#         line = f.readline()
#         if not line:
#             break

#         if '<a href=\"/p/' in line:
#             print(line.strip())
#             print(re.findall(r'\d', line))
#             print(re.search(r'(\d{9})', line).group())
#             print("/krayt max allycode: {}".format(re.search(r'(\d{9})', line).group()))


#             swgoh_gg_profile_url = "https://swgoh.gg/p/{}/".format(re.search(r'(\d{9})', line).group())

#             request_site = Request(swgoh_gg_profile_url, headers={"User-Agent": "Mozilla/5.0"})
#             webpage = urlopen(request_site).read()
#             print(webpage[:500])
            



page = requests.get(im_aroa_yr_url)

soup = BeautifulSoup(page.content, "html.parser")

for a in soup.find_all('a', href=True):
    print("Found the URL:", a['href'])

results = soup.find('a', href=True)
print(results.prettify())


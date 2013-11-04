__author__ = 'frodo'
from bs4 import BeautifulSoup
import requests
import re

counts = dict()
url = "http://www.codechef.com/rankings/ACMKGP13"
regex = "/users/acmkg13tm"
prefix = "http://www.codechef.com/teams/view/acmkg13tm"
contestMarker = "Contest : ACMKGP13"

minQuestions = 2

with open("list.txt", "w") as file:
    soup = BeautifulSoup(requests.get(url).text)
    for link in soup.find_all('a'):
        if re.match(regex, link.get('href')):
            id = link.get('href')[16:]
            page = str(requests.get(prefix + id).text)

            # number of solutions
            conMark1 = page.index("<table>",page.index(contestMarker))
            conMark2 = page.index("</table>", conMark1) + 8
            innerSoup = BeautifulSoup(page[conMark1:conMark2])
            innerSoup.prettify()
            if innerSoup.text.count(":")//2 < minQuestions:
                continue

            # name of college
            mark1 = "<td><b>Institution:</b></td>"
            index1 = page.index(mark1)+len(mark1)+5
            mark2 = "</td>"
            index2 = page.index(mark2,index1)
            name = page[index1:index2]
            counts[name] = counts.get(name, 0) + 1
            #print(name + " -> " + str(counts[name]))
    for key in counts:
        file.write(key + " -> " + str(counts[key]) + "\n")


import urllib.request
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, site, date):
        self.site = site
        self.date = date.strip()

    def checkdate(self):
        date=self.date.split('.')
        for n in date:
            if not n.isdigit():
                return False
        self.date=".".join(date)
        return True

    def scrape(self):
            page = urllib.request.urlopen(self.site)
            html = page.read()
            parser = "html.parser"
            sp = BeautifulSoup(html, parser)
            k=0
            list = []
            for tag in sp.find_all('td'):
                if self.date in sp.find_all('td')[k].get_text():
                    for i in range(1, 6):
                            #print(sp.find_all('td')[k+i])
                            if len(sp.find_all('td')[k+i].get_text())>2:
                                list.append(str(i)+" - "+sp.find_all('td')[k+i].get_text())
                                if sp.find_all('td')[k+i].next.name == "table":
                                    k+=3
                    list="\n".join(list)
                    break
                k+=1
            if len(list)>0:
                return list
            else:
                return "В этот день нет пар."

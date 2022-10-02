import beautifulsoup4
import requests
import sys

class Search():
    def __init__(self, query):
        self.query = query
        self.url = "https://www.google.com/search?q={}".format(self.query)
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
        self.response = requests.get(self.url, headers=self.headers)
        self.soup = beautifulsoup4.BeautifulSoup(self.response.text, "html.parser")
        self.results = self.soup.find_all("div", class_="g")

    def print_results(self):
        for result in self.results:
            title = result.find("h3").text
            url = result.find("cite").text
            description = result.find("span", class_="st").text
            print(title)
            print(url)
            print(description)
            print()
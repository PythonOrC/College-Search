from bs4 import BeautifulSoup
import requests
import re
import sys
import SearchExceptions
import warnings


class Search:
    def __init__(self, file_addr):
        self.COLLEGE_URL_PATTERN = re.compile(r"^/college\/.*")
        self.PAGE = "&page="
        self.results = set()
        self.import_file(file_addr)
        self.search_college()
        self.save_list()

    def import_file(self, file_addr):
        try:
            with open(file_addr, "r") as file:
                self.urls = [line.strip() for line in file]
        except FileNotFoundError:
            print("Text file" + file_addr + "not found")
            sys.exit()

    def search_college(self):
        if self.urls == []:
            return
        current_url = self.urls.pop()
        print("Searching: " + current_url)
        try:
            response = requests.get(current_url)
            if response.status_code != 200:
                raise SearchExceptions.URLNotFound(current_url)
        except requests.exceptions.ConnectionError:
            raise SearchExceptions.URLNotFound(current_url)

        self.content = BeautifulSoup(response.text, "html.parser")

        college_url = self.content.find_all(
            "a", href=self.COLLEGE_URL_PATTERN, class_=None
        )
        if college_url == []:
            warnings.warn("No college found in " + current_url)
        [
            self.results.add(college.text)
            if college.text.replace("\n", "").strip()
            else None
            for college in college_url
        ]
        self.construct_url(current_url)
        if self.has_next():
            self.urls.append(self.next_page_url)
        self.search_college()

    def has_next(self):
        return self.content.find("a", href=self.next_page_pattern)

    def construct_url(self, url):
        base_url, page = url.split(self.PAGE) if self.PAGE in url else (url, "1")
        self.next_page_url = base_url + self.PAGE + str(int(page) + 1)
        self.next_page_pattern = "/" + "/".join(self.next_page_url.split("/")[-2:])

    def save_list(self):
        with open("colleges.txt", "w", encoding="UTF-8") as file:
            for result in self.results:
                print(result)
                file.write(result + "\n")


if __name__ == "__main__":
    addr = input("Enter file name (default is url.text): ")
    if addr == "":
        addr = "url.txt"
    if not addr.endswith(".txt"):
        addr += ".txt"
    try:
        print("Searching...(press ctrl+c to stop)")
        Search(addr)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
    except SearchExceptions.URLNotFound as e:
        print(e.message)
        sys.exit(1)
    except SearchExceptions.URLNotCollegeList as e:
        print(e.message)
        sys.exit(1)

    except Exception as e:
        print("Unkown Error: \n" + e)
        sys.exit(1)

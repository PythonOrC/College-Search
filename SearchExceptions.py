class URLNotFound(Exception):
    def __init__(self, url):
        self.url = url
        self.message = "URL not found: " + url
        super().__init__(self.message)

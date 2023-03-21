class UrlManager:
    """
        url管理器
    """
    def __init__(self): 
        self.new_urls = set()
        self.old_urls = set()

    # 添加单个url
    def add_new_url(self, url):
        if url is None or len(url) == 0:
            return
        if url  in self.new_urls or url  in self.old_urls:
            return
        self.new_urls.add(url)

    # 批量添加url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 获取一个url
    def get_url(self):
        if self.has_new_url():
            new_url = self.new_urls.pop()
            self.old_urls.add(new_url)
            return new_url
        else:
            return None

    # 判断是否有新的url
    def has_new_url(self):
        return len(self.new_urls) != 0


if __name__ == "__main__":
    url_manager = UrlManager()
    url_manager.add_new_url("url1")
    url_manager.add_new_urls(["url1", "url2"])
    print(url_manager.new_urls,url_manager.old_urls)
    print("#"*50)

    print(url_manager.get_url())
    print(url_manager.get_url())
    print(url_manager.new_urls,url_manager.old_urls)

    print("#"*50)
    print(url_manager.has_new_url())

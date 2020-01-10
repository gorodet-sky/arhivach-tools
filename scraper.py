import csv
import threading
from queue import Queue

import requests
from requests.exceptions import HTTPError

from parsers import parse_posts_list


class ArhivachPostsScraper(object):
    def __init__(self, urls, out_file, thread_count):
        self.queue = Queue()
        self.thread_count = thread_count
        self.urls = urls
        self.out_file = out_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        for url in urls:
            result = URLTarget(url, self.headers, None)
            self.queue.put(result)

    def run(self):
        for i in range(self.thread_count):
            thread = Downloader(self.queue, self.out_file)
            thread.start()

        if self.queue.qsize() > 0:
            self.queue.join()


class Downloader(threading.Thread):
    def __init__(self, queue, out_file):
        super().__init__()
        self.queue = queue
        self.out_file = out_file
        self.fields = ["post_id", "post_datetime", "post_tags", "poster_name", "reply_to", "post_text"]

    def run(self):
        while self.queue.empty() == False:
            url = self.queue.get()
            response = url.download()
            if (response):
                posts = parse_posts_list(response)
                if (len(posts) > 0):
                    self.write(posts)
                print('Success: ' + str(url))

            self.queue.task_done()

    def write(self, datas):
        with open(self.out_file, 'a+', encoding='utf-8') as file:
            w = csv.DictWriter(file, self.fields, delimiter=';')
            for data in datas:
                w.writerow(data)


class URLTarget(object):
    def __init__(self, url, headers, proxy):
        self.url = url
        self.headers = headers
        self.proxy = proxy

    def download(self):
        try:
            posts_page = requests.get(self.url, proxies=self.proxy, headers=self.headers)
            posts_page.raise_for_status()
            posts_page.encoding = 'utf-8'
        except Exception as err:
            print('Failure: ' + str(self.url) + ' ' + str(err))
        else:
            return posts_page.text

    def __str__(self):
        return self.url

import argparse
import os
import sys

from scraper import ArhivachPostsScraper

ARHIVACH_BASE_URL = 'http://arhivach.ng'
DEFAULT_FOLDER = "./data"
DEFAULT_FILENAME = 'posts'
DEFAULT_SUFFIX = 'csv'


def build_posts_page_url(post_id, base_url):
    result_url = base_url + '/thread/' + str(post_id)

    return result_url


def get_args_parser():
    parser = argparse.ArgumentParser()

    # optional
    parser.add_argument("-U", "--url", type=str,
                        help="arhivach base url", default=ARHIVACH_BASE_URL)
    parser.add_argument("-E", "--end", type=int,
                        help="end thread id", default=513282)
    parser.add_argument("-S", "--start", type=int,
                        help="start thread id", default=47)
    parser.add_argument("-D", "--step", type=int,
                        help="thread id iteration step", default=1)
    parser.add_argument("-T", "--thread_count", type=int,
                        help="count of worker threads", default=5)
    parser.add_argument("-O", "--out", type=str,
                        help="output file")

    return parser


if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()

    start_id = args.start
    end_id = args.end
    step = args.step
    base_url = args.url
    thread_count = args.thread_count
    out_file = args.out

    if not out_file:
        if (not os.path.exists(DEFAULT_FOLDER)):
            os.makedirs(DEFAULT_FOLDER)
        out_file = os.path.join(DEFAULT_FOLDER, DEFAULT_FILENAME + '.' + DEFAULT_SUFFIX)
    else:
        out_file = out_file.strip()

    if (start_id > end_id):
        temp = start_id
        start_id = end_id
        end_id = temp

    posts_range = range(start_id, end_id, step)
    urls = list(reversed([build_posts_page_url(post_id, base_url) for post_id in posts_range]))

    downloader = ArhivachPostsScraper(urls, out_file, thread_count)
    downloader.run()

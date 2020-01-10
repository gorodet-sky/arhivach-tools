from lxml import html
import re


def get_post_num(text):
    '''
    Get post number from text.
    '''
    result = re.search(r'[#>]+(?P<num>\d+)', text)

    if (result):
        return result.group('num')


def parse_posts_list(html_page):
    '''
    Parse a posts list.
    '''
    results = []

    tree = html.fromstring(html_page)
    posts_list = tree.xpath('//div[@class = "thread_inner"]')

    if (len(posts_list) > 0):
        posts = posts_list[0].xpath('.//div[@class = "post"]')
        tags = parse_thread_tags(tree)

        for post_tree in posts:
            post = parse_post(post_tree)
            if (post):
                post["post_tags"] = tags
                results.append(post)

    return results


def parse_post(tree):
    try:
        post_comment_body = tree.xpath('.//div[@class = "post_comment_body"]')[0]
        post_head = tree.xpath('.//div[@class = "post_head"]')[0]

        # get post text
        post_text = " ".join(post_comment_body.itertext()).strip()

        # get post id
        post_id_link = post_head.xpath('.//span[@class = "post_id"]/a/@href')

        if (len(post_text) < 1 or not post_id_link):
            return

        post_id_link = post_id_link[0]
        post_id = get_post_num(post_id_link)

        # get reply to ids
        reply_link = post_comment_body.xpath('.//a/@href')
        reply_to = []

        for i in reply_link:
            reply_to_id = get_post_num(i)
            if (reply_to_id):
                reply_to.append(reply_to_id)

        # get poster name
        poster_name = post_head.xpath('.//span[@class = "poster_name"]/text()')
        if (poster_name):
            poster_name = poster_name[0]

        # get post date time
        post_datetime = post_head.xpath('.//span[@class = "post_time"]/text()')
        if (post_datetime):
            post_datetime = post_datetime[0]

        return {
            "post_id": post_id,
            "post_datetime": post_datetime,
            "poster_name": poster_name,
            "reply_to": reply_to,
            "post_text": post_text
        }
    except:
        return


def parse_thread_tags(tree):
    '''
    Parse thread tags.
    '''
    results = []

    thread_head = tree.xpath('//div[@class = "row-fluid thread_header"]')

    if (len(thread_head) > 0):
        thread_tags = thread_head[0].xpath('.//div[@class = "span3 thread_tags"]/span/a')
        for tag in thread_tags:
            # get tag title
            title = tag.xpath('.//@title')[0]
            if (title):
                results.append(title)

    return results

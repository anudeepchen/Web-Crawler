from HTMLParser import HTMLParser
from urllib2 import urlopen
from urlparse import urljoin
from Text_Parser import get_words
from database_handler import create_table
from database_handler import add_item
from database_handler import get_top_urls_for_word
from chart_handler import draw_chart
from sys import stdin


# Concept from: http://www.netinstructions.com/how-to-make-a-web-crawler-in-under-50-lines-of-python-code/
class WebCrawler(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = urljoin(self.baseUrl, value)
                    self.links = self.links + [new_url]

    def get_links(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        html_bytes = response.read()
        html_string = html_bytes.decode("utf-8")
        self.feed(html_string)
        return html_string, self.links


def bfs_spider(url, word, maxPages):
    pages_to_visit = [url]
    pages_visited = {url}
    number_of_pages_visited = 0

    # pages_visited.add(url)
    found_word = False

    table_name = 'PageDetails'
    create_table(table_name)
    while number_of_pages_visited < maxPages and pages_to_visit != []:
        number_of_pages_visited += 1
        url = pages_to_visit.pop(0)

        try:
            print("---------------------------")
            print(number_of_pages_visited, "Visiting:", url)
            # print(number_of_pages_visited, "Visiting:", url)
            crawler = WebCrawler()
            data, links = crawler.get_links(url)
            if data.find(word) > -1:
                num_of_occurrences = len(list(find_all_occurrences(data, word)))
                found_word = True
                words = get_words(url)
                page_details = get_page_details(url, word, num_of_occurrences, links)
                add_item(page_details, table_name)
                print("Found the keyword!")
                print(" ")
                print("The most relevant keywords in the page are: ")
                print(words[:5])
                print(" ")

            for link in links:
                if link not in pages_visited:
                    pages_visited.add(link)
                    pages_to_visit.append(link)
        except Exception as e:
            print(str(e))

    print("---------------------------")
    print(" ")
    if not found_word:
        print("Keyword not found...")


def dfs_spider(url, word, max_pages):
    pages_to_visit = [url]
    pages_visited = {url}
    number_of_pages_visited = 0

    # pages_visited.add(url)
    found_word = False

    table_name = 'PageDetails'
    create_table(table_name)
    while number_of_pages_visited < max_pages and pages_to_visit != []:
        number_of_pages_visited += 1
        url = pages_to_visit.pop(0)

        try:
            print("---------------------------")
            print(" ")
            print(number_of_pages_visited, "Visiting:", url)
            # print(number_of_pages_visited, "Visiting:", url)
            crawler = WebCrawler()
            data, links = crawler.get_links(url)
            if data.find(word) > -1:
                num_of_occurrences = len(list(find_all_occurrences(data, word)))
                found_word = True
                words = get_words(url)
                page_details = get_page_details(url, word, num_of_occurrences, links)
                add_item(page_details, table_name)
                print(" ")
                print("Found the keyword!")
                print(" ")
                print("The most relevant keywords in the page are: ")
                print(words[:5])

            for link in links:
                if link not in pages_visited:
                    pages_visited.add(link)
                    pages_to_visit.insert(0, link)
        except Exception as e:
            print(str(e))

    print("---------------------------")
    print(" ")
    if not found_word:
        print("Keyword not found...")


def find_all_occurrences(data, word):
    start_index = 0
    while True:
        start_index = data.find(word, start_index)
        if start_index == -1:
            return
        yield start_index
        start_index += len(word)


def get_page_details(url, word, word_count, links):
    page_details = {'url': url, 'word': word, 'word_count': word_count, 'hyperlinks': links}
    return page_details

if __name__ == "__main__":
    print("Enter the keyword you wish to find: ")
    keyword = stdin.readline().rstrip('\n')
    print("Would you like to crawl the web for the keyword or search the database? (web / db): ")
    search_location = stdin.readline().rstrip('\n')
    if search_location == 'web':
        print("Enter the initial URL (starting from http://www.): ")
        url = stdin.readline().rstrip('\n')
        print("Choose (bfs / dfs): ")
        search_type = stdin.readline().rstrip('\n')
        print("Enter the maximum number of web-pages to crawl (around 200 gives good coverage): ")
        max_pages = int(stdin.readline().rstrip('\n'))
        # url = "http://www.cmu.edu"
        if search_type == 'bfs':
            bfs_spider(url, keyword, max_pages)
        else:
            dfs_spider(url, keyword, max_pages)
        print(' ')
        print("In the generated star graph, the closer a URL is to the the word in the center, the more is its relevance.")
        print("Relevance is decided by the number of times a word occurs in a URL.")
        draw_chart(keyword, 15)
    else:
        top_urls = get_top_urls_for_word(keyword, 10, 'PageDetails')
        if top_urls['Count'] == 0:
            print('This keyword is not present in the database.')
        else:
            print(' ')
            print('The top 10 pages with this keyword are: ')
            for item in top_urls['Items']:
                print(item['url'])
            print(' ')
            print("In the generated star graph, the closer a URL is to the the word in the center, the more is its relevance.")
            print("Relevance is decided by the number of times a word occurs in a URL.")
            draw_chart(keyword, 10)

    # for item in top_urls['Items']:
    #     print(item['word_count'])


import requests
from bs4 import BeautifulSoup
import re
import string
from nltk.corpus import stopwords
import collections
import sys

# To Remove Stopwords
cachedStopWords = stopwords.words("english")

# url = "http://www.walmart.com/ip/Canon-PIXMA-MG2520-Inkjet-All-in-One-Printer/28773460"

# Method verifies if the input URL is valid or not : Source : Stackoverflow
def url_validation(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    m = regex.match(url) 
    if m:
        return True
    else:
        return False

# to raise exception when an input is invalid url
class UrlException(Exception):
    pass

# Method fetches all the words in Title, Paragraph, Header tag of a HTML page
def get_words(urls):
    if(url_validation(urls)):
        resp = requests.get(urls)
        soup = BeautifulSoup(resp.text, "html.parser")

    # Get data from 'Title','Paragraph','header'
        title = soup.find_all('title')
        ptag = soup.find_all('p')
        htag = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Regular expression to remove unnecessary punctuation
        regex = re.compile('[%s]' % re.escape(string.punctuation))

    # Text of Title tag
        title_text = title[0].text
        title_words = regex.sub('', title_text).lower().split()

    # Text of Paragraph tag
        ptags = [regex.sub('', tag.text).lower().split() for tag in ptag]
        ptags_words  = [val for sublist in ptags for val in sublist]

    # Text of Header tag
        htags = [regex.sub('', tag.text).lower().split() for tag in htag]
        htags_words  = [val for sublist in htags for val in sublist]

    # List of words from above tags
        final_list = title_words+ptags_words+htags_words
    
    # List of all the words after removing the stopwords
        filtered_words = [word for word in final_list if word not in stopwords.words('english')]
        return filtered_words
    else:
        raise UrlException("Input URL is not valid")
        sys.exit(0)

# filtered_words = get_words(url)


# Method gives the number of times each word has appeared on the webpage
def word_frequency(words, n):
    output_words = {}
    for i in range(len(words)-n+1):
        g = ' '.join(words[i:i+n])
        output_words.setdefault(g, 0)
        output_words[g] += 1
    return output_words

# words = word_frequency(filtered_words, 1)

# sorted_x = sorted(words.items(), key=operator.itemgetter(1), reverse=True)

# print(sorted_x[:5])


# Method defined to generate ngrams based on input
def ngrams(words, n):
    output_words = {}
    for i in range(len(words)-n+1):
        g = ' '.join(words[i:i+n])
        output_words.setdefault(g, 0)
        output_words[g] += 1
    return output_words

# Calculating 2grams to identify the relevant topics of a page
number_of_ngrams = 2
# output_words = ngrams(filtered_words, number_of_ngrams)

keywords = {}

# Method calculates the keyword density
# Keyword density is derived as given below where v = number of occurrences of particular phrase
# len(output_words) = total number of words
def density_calc(output_words,ngrams):
    for k, v in output_words.items():
        keyword_density = v/(len(output_words)-((ngrams-1) * v))
        keywords.setdefault(k, 0)
        keywords[k] = keyword_density
    return keywords

# keywords = density_calc(output_words, number_of_ngrams)
# Fetch the phrases with highest value
output = collections.Counter(keywords).most_common(10)

# print("Input : ",url)
# print("List of common topics that best describe the contents of that page:")
for item in output:
    print(item[0])
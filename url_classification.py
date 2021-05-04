from urllib.parse import urlparse
import ipaddress
import numpy as np
import matplotlib.pyplot as plt
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
##import nltk

#nltk.download('stopwords')
#from nltk.corpus import stopwords
import pandas as pd
import re

'''from tld import get_tld, get_fld'''
import string
import ast

class main_class():
    def Enter_url(url):
        if url.startswith("file") or "localhost" in url  or url.startswith("http"):
            res = "localfile"
        if url.startswith("https"):
            res = main_class.search_using_naive_bayes(url)
        elif url.startswith("file") or ipaddress.ip_address(url) or ipaddress.ip_network(url):
            res = "localfile"
        else:
             res = "localfile"
        return res
    def search_using_naive_bayes(url):
        def preprocess(sentence):
            import nltk
            from nltk.tokenize import RegexpTokenizer
            from nltk.stem import WordNetLemmatizer, PorterStemmer
            from nltk.stem.lancaster import LancasterStemmer
            from nltk.stem import SnowballStemmer
            from nltk.corpus import stopwords
            import re
            lemmatizer = WordNetLemmatizer()
            stemmer = PorterStemmer()
            # stemmer= LancasterStemmer()
            # stemmer = SnowballStemmer(language='spanish')
            sentence = str(sentence)
            sentence = sentence.lower()
            sentence = sentence.replace('{html}', "")
            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '', sentence)
            rem_url = re.sub(r'http\S+', '', cleantext)
            rem_num = re.sub('[0-9]+', '', rem_url)
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(rem_num)
            filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english')]
            # stem_words=[stemmer.stem(w) for w in filtered_words]
            # appending_or = [x for x in stem_words]
            appending_or = [x for x in filtered_words]
            return " ".join(appending_or)

        def extract_url_details(url, count=0):
            from bs4 import BeautifulSoup
            import requests
            content = []
            title2 = []
            header = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Safari/537.36'}
            res = requests.get(url, headers=header, timeout=30)
            if (res.status_code == 200):
                try:
                    #soup = BeautifulSoup(res.text,"lxml")
                    soup = BeautifulSoup(res.content, "html")
                    title = soup.title.string
                    title2.append(title)
                    meta = soup.find_all('meta')
                    for tag in meta:
                        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description',
                                                                                                'keywords']:
                            content.append(tag.attrs['content'])
                except:
                    content.append("no_details")
                    title2.append("no_details")

                content = ' '.join(content)
                search_content = preprocess(content)
                search_title = preprocess(title2)
                url_content = []
                if (sum([i.strip(string.punctuation).isalpha() for i in search_content.split()]) < 8) and (
                        sum([i.strip(string.punctuation).isalpha() for i in search_title.split()]) < 8):
                    if search_content == "no_details" or search_title == "no_details":
                        url_content = 'no_details'
                    elif (len(search_content) > len(search_title)):
                        url_content = search_content
                    elif (search_title != 'no_details'):
                        url_content = search_title
                    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
                    if (count == 0):
                        return extract_url_details(base_url, count=1)
                elif (len(search_content) > len(search_title)):
                    url_content = search_content
                elif (search_title != 'no_details'):
                    url_content = search_title
                elif search_content == "no_details" or search_title == "no_details":
                    url_content = 'no_details'

                return str(url_content)
            else:
                return 'error'
       # import ast
        import pickle
        with open('short_dataset.pkl', 'rb') as fout:
            mini_dataset = pickle.load(fout)
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
        if base_url in mini_dataset:
            res = mini_dataset[base_url]
            return res


        url_content = extract_url_details(url)
        print("URL content is :",url_content)
        res = ''
        if (url_content == 'no_details'):
            res = "others"
            return res
        elif (url_content == 'error'):
            res = "You cannot access this page"
            return res
        else:
            import pickle
             #with open('pickeled_csv.pkl', 'wb') as fout:
                # print(" ")
                #pickle.dump((count_vect, clf_pavan), fout)
            with open('pickeled_csv.pkl', 'rb') as fin:
                vectorizer, clf = pickle.load(fin)
            res = clf.predict(vectorizer.transform([url_content]))[0]
            return res
    def main():
        res = input("enter url")
        result = main_class.Enter_url(res.strip())
        print(result)

main_class.main()
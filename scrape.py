import sys
import os
import re
from googlesearch import search
from html.parser import HTMLParser
import datetime
import requests
import urllib3

def main():
    start_line = 1
    filepath = "default.txt"
    string_to_append = ' email'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
  
    with open(filepath) as fp:
        print(str(datetime.datetime.now()))
        cnt = 0
        for line in fp:
            print('prcessing line ' + str(cnt + start_line) + '...')
            save_result(str(cnt + start_line), process_line(line.strip() + string_to_append))
            cnt += 1
        print(str(datetime.datetime.now()))

def save_result(line, list_of_emails):
    with open("result.txt", "a") as f:
        f.write(line + ', ' + ', '.join(list_of_emails) + '\r')
    print(line + ', ' + ', '.join(list_of_emails))

def process_line(query):
    max_tries = 3
    counter = 0
    while counter < max_tries:
        try:
            print("searching google for " + query + ", tentative #" + str(counter + 1))
            extracted = []
            for j in search(query, tld='com', num=10, stop=10, pause=2): 
                for email_address in process_url(j):
                    if email_address not in extracted:
                        extracted.append(email_address)
            counter = max_tries
        except:
            print("error encountred, retrying... ")
            counter += 1
    return extracted

def process_url(url):
    max_tries = 3
    res = ''
    regex_email = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    counter = 0
    while counter < max_tries:
        try:
            print("tentative #" + str(counter + 1) + " -> " + url)
            response = requests.get(url, verify=False)
            counter = max_tries
            print("done, no errors")
        except requests.exceptions.RequestException as e:
            print("retrying..." + e)
            counter += 1
    matches = re.findall(regex_email, response.text)
    result = list(dict.fromkeys(matches))
    result = [x for x in result if x]
    return result

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == '__main__':
    main()

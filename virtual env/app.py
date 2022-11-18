import validators
from validators import ValidationFailure
import argparse
import requests
import json
import time
import concurrent.futures
import threading

class URLManager:

    def __init__(self):
        self.thread_local = threading.local()
        self.url_dict = {}

    def isline_url(self, line):
        result = validators.url(line)

        if isinstance(result, ValidationFailure):
            return False
        return True

    def check_text_sample(self, path):
        self.valid_urls, self.invalid_urls = set(), {}
        count = 1
        
        with open (path, 'r',) as f:
            data = f.readlines()
        
        for line in data:
            line = line.strip()
            if self.isline_url(line):
                self.valid_urls.add(line)
            else:
                self.invalid_urls[count] = line
            count += 1

    def print_invalid_lines(self):
        for number, line in self.invalid_urls.items():
            print(f"Line {number} is not a URL")

    def get_session(self):
        if not hasattr(self.thread_local, "session"):
            self.thread_local.session = requests.Session()
        return self.thread_local.session
    
    def check_site_http(self, url):
        self.url_dict[url] = {}
        session = self.get_session()
        methods = [session.get, session.post, session.put, session.head, session.delete, session.options, session.patch]
        for method in methods:
            req = method(url)
            status = req.status_code
            if status < 400:
                method = method.__name__.upper()
                self.url_dict[url][method] = req.status_code


    def check_http_methods(self):
        '''Methods, which need to check (get, post, put, head, delete, options, patch'''
        
        #implement threading
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.check_site_http, self.valid_urls)

        json_data = self.url_dict
        json_formatted_str =json.dumps(json_data, indent=2)
        print(json_formatted_str)





class CLIManager:

    def __init__(self,  argv=None):
        self.parser = argparse.ArgumentParser(description="The program check each line of text as URL address")
        self.manager = URLManager()

        self.parser.add_argument('-t', '--text', help='After this key, you must insert sample text')
        self.parser.add_argument('-f', '--file', help='After this key, you must insert path to .txt file with sample code')

        self.args = self.parser.parse_args(argv)

    def run(self):
        text = self.args.text
        file_name = self.args.file

        if text != None:
            if self.manager.isline_url(text):
                print(f'The URL {text} is valid')
            else:
                print(f'The line {text} is invalid URL')
        elif file_name != None:
            try:
                self.manager.check_text_sample(file_name)
                self.manager.print_invalid_lines()
                self.manager.check_http_methods()
            except FileNotFoundError:
                print('No such file or directory')

if __name__ == "__main__":
    start_time = time.time()
    app = CLIManager()
    app.run()
   

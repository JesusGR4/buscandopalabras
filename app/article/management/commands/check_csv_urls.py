from django.core.management.base import BaseCommand
import pandas as pd
import numpy
from urllib import request, parse
from bs4 import BeautifulSoup
import re


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Nombre del archivo que quieres usar")
        parser.add_argument('href_regex', type=str, help="Expresión regular que se quiere buscar por href de a")

    def handle(self, **options):

        csv_file = options['csv_file']
        href_regex = options['href_regex']
        df = pd.read_csv(csv_file, dtype='str')
        url_errors = []
        for i, k in df.iterrows():
            url = k.get('urls')
            try:
                req = request.Request(url=url, headers={
                    'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
                handler = request.urlopen(req)
                http_code = handler.code
                if http_code == 200:
                    content = handler.read()
                    soup = BeautifulSoup(content, 'lxml')
                    hrefs = soup.find_all('a', {'href': re.compile(href_regex)})
                    if not hrefs:
                        url_errors.append(url)
            except Exception as e:
                url_errors.append(url)
                continue

        # Save errors in csv
        numpy.savetxt("urls_not_found.csv", url_errors, delimiter=",", fmt="%s")

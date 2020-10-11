from django.core.management.base import BaseCommand
from article.models import *
import pandas as pd


class Command(BaseCommand):
    def handle(self, **options):
        df = pd.read_csv('keywords.csv', dtype='str')
        for keyword in df['Keyword']:
            self.init_process(keyword)

    def init_process(self, keyword):

        keyword_splitted_by_o = keyword.split(" o ")
        if len(keyword_splitted_by_o) > 1:
            title = "Buscando la palabra correcta: ¿%s?" % keyword
            print(title)
            exit
            for splitted_keyword in keyword_splitted_by_o:
                self.create_article(splitted_keyword)
        else:
            keyword_splitted_by_y = keyword.split(" y ")
            for splitted_keyword in keyword_splitted_by_y:
                self.create_article(splitted_keyword)

    def create_article(self, keyword):
        pass

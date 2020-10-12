from django.core.management.base import BaseCommand
from article.models import *
import pandas as pd
from article.models import Article
import time
from random import randrange
import traceback

class Command(BaseCommand):

    def handle(self, **options):

        df = pd.read_csv('keywords.csv', dtype='str')
        for keywords in df['Keyword']:
            print("Ejecutando las keywords -> %s " % keywords)
            try:
                self.init_process(keywords)
            except Exception as e:
                print('La key %s ha petao' % keywords)
                traceback.print_exc()
                continue
            time_to_sleep = randrange(1, 5)
            time.sleep(time_to_sleep)
            print("He dormido %d segundos" % time_to_sleep)

    def init_process(self, keywords):
        if not Article.keywords_exists(keywords):
            article = Article()
            article.keywords = keywords
            article.save()
        else:
            print("Esta keyword ya existe")

import os, numpy
from django.core.management.base import BaseCommand
from article.models import *
import pandas as pd
from article.models import Article
import time
from random import randrange
import traceback
class Command(BaseCommand):
    def handle(self, **options):
        df = pd.read_csv('kw.csv', dtype='str')
        kw_errors = []
        for i, k in df.iterrows():
            keywords = k.get('Keyword')
            order = k.get('Order')
            print("INFO: Ejecutando las keywords *%s*" % keywords)
            try:
                self.init_process(keywords, order)
            except Exception as e:
                print(f'ERROR: La key *{keywords}* ha petao')
                # traceback.print_exc()
                kw_errors.append([keywords])
            time_to_sleep = randrange(1, 5)
            time.sleep(time_to_sleep)
            print("INFO: He dormido %d segundos." % time_to_sleep)

        # Save errors in csv
        numpy.savetxt("kw_errors.csv", kw_errors, delimiter=",", fmt="%s")

    def init_process(self, keywords, order):
        if not Article.keywords_exists(keywords):
            article = Article()
            article.keywords = keywords
            article.order = order
            article.save()
        else:
            print(f"WARNING: *{keywords}* ya existe!")

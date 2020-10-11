from urllib import request
from bs4 import BeautifulSoup
import re
class WordReference(object):
    synonymous_url = "https://www.wordreference.com/sinonimos/"

    def get_synonymous(self, word):
        url = self.synonymous_url + "%s" % word


class Rae(object):
    rae_url = "https://dle.rae.es/"

    def get_word_definition(self, word):
        url = self.rae_url + "%s" % word
        req = request.Request(url=url   , headers={
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        handler = request.urlopen(req)
        http_code = handler.code
        if not http_code == 200:
            result = ''
        else:
            content = handler.read()
            soup = BeautifulSoup(content, 'lxml')
            p_set = soup.find("div", {"id": "resultados"}).findAll('p', {"id": True})
            if not p_set:
                # Significa que no tiene resultados, por lo que no devolvemos nada
                result = ''
            else:
                cleanr = re.compile('<.*?>')
                definitions = []
                for p in p_set:
                    prettify = p.prettify()
                    cleantext = re.sub(cleanr, '', prettify)
                    cleantext = cleantext.replace('\n', '')
                    cleantext = cleantext.strip()
                    definitions.append(" ".join(cleantext.split()))
                result = '\n'.join(definitions)

        return result
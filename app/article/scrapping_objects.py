from urllib import request, parse
from bs4 import BeautifulSoup
import re
from googletrans import Translator


class WordReference(object):
    synonymous_url = "https://www.wordreference.com/sinonimos/"

    def get_synonymous(self, word):
        word_encoded = parse.quote(word)
        synonymous = ""
        url = self.synonymous_url + "%s" % word_encoded
        req = request.Request(url=url, headers={
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        handler = request.urlopen(req)
        content = handler.read()
        soup = BeautifulSoup(content, 'lxml')
        article = soup.find("div", {"id": "article"}).find("div", {"class": "trans clickable"})
        if article:
            text_synonymous = article.find("ul").find("li").get_text()
            synonymous = " ".join(text_synonymous.split())

        return synonymous


class Translation(object):
    languages = {
        'fr': 'Francés',
        'it': 'Italiano',
        'en': 'Inglés',
        'pt': 'Portugués'
    }

    def get_translations_from_word(self, word):
        translator = Translator(service_urls=[
            'translate.google.es'])
        translation_array = []

        for language_code in self.languages:
            language_value = self.languages.get(language_code)
            translation = translator.translate(word, src='es', dest=language_code)
            translate_text = translation.text
            translation_array.append("La palabra %s se escribe en %s -> %s" % (word, language_value, translate_text))

        return '\n'.join(translation_array)


class Rae(object):
    rae_url = "https://dle.rae.es/"

    def get_word_definition(self, word):
        word_encoded = parse.quote(word)
        url = self.rae_url + "%s" % word_encoded
        req = request.Request(url=url, headers={
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

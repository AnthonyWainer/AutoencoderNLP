import json
import re
from typing import AnyStr, Dict, List

import requests
import nltk

from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def get_words(text_content: AnyStr) -> List:
    """ Function to get words from text content

        @param text_content    The text content
    """
    text_in_lower = str(text_content).replace('\n', ' ').replace("\t", " ").lower()

    emoji_text = emoji.replace_emoji(text_in_lower)

    only_text = re.sub(r'(#\w+)|(.#\w+)|(@\w+)|(.@\w+)|(http\S+)|([^a-záéíóúñ ]+)', ' ', emoji_text)
    dropped_words = set(only_text.split())
    return list(dropped_words)


def processing_words(text_content: AnyStr, own_words: List = None, lang="spanish") -> AnyStr:
    """ Function to processing words from text content

        :param lang: language
        :param text_content    The text content
        :param own_words       Words customized
    """

    if own_words is None:
        own_words = []
    words = get_words(text_content)

    spanish_stops = set(stopwords.words(lang) + own_words)

    return " ".join([word for word in words if word not in spanish_stops and len(word) > 3])


class EmojiDecode:

    def __init__(self, emoji_path: AnyStr) -> None:
        emoji_file = requests.get(emoji_path)
        self.emojis = json.loads(emoji_file.text)

    @staticmethod
    def multiple_replace(emojis, text: AnyStr) -> AnyStr:
        regex = re.compile("(%s)" % "|".join(map(re.escape, emojis.keys())))

        return regex.sub(lambda em: emojis[em.string[em.start():em.end()]], text)

    def filter_emojis(self, by_replace: List) -> Dict:
        return {i: self.emojis[i] for i in by_replace if i in self.emojis.keys()}

    def replace_emoji(self, text: AnyStr) -> AnyStr:
        by_replace = list(set(re.findall(r'[^\w\s,]', text)))
        if not by_replace:
            return text

        emojis = self.filter_emojis(by_replace)
        if not emojis:
            return text

        return self.multiple_replace(emojis, text)


__URL_GIT__ = 'https://github.com/anthonywainer/embeddings_analysis_spanish/blob/master/data/emoticones.json?raw=true'
emoji = EmojiDecode(__URL_GIT__)

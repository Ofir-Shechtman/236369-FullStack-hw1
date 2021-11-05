from hw1_utils import generate_wordcloud_to_file
from pdfminer import high_level
import re

STOPWORDS = 'stopwords.txt'
with open(STOPWORDS) as f:
    stopwords = f.read().splitlines()


class WordCloudGenerator:

    @staticmethod
    def extract_words(pdf_name) -> str:
        text = high_level.extract_text(pdf_name)
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        words_list = [word for word in text.split() if word not in stopwords]
        return ' '.join(words_list)

    @classmethod
    def generate_wordcloud_to_file(cls, pdf_name, picture_name) -> None:
        generate_wordcloud_to_file(cls.extract_words(pdf_name), picture_name)


if __name__ == '__main__':
    WordCloudGenerator.generate_wordcloud_to_file('HW1_236369.pdf', 'HW1_236369.png')

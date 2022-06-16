from src.crawler import Crawler
from src.language_classifier import LanguageClassifier
from src.vad_service import VAD


class CSSPipeline:
    def run(self):
        crawler = Crawler()
        vad = VAD()
        language_classifier = LanguageClassifier()

        crawler.crawl()
        vad.detect()
        language_classifier.classify()

import logging

from css_pipeline import CSSPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

if __name__ == '__main__':
    css_pipeline = CSSPipeline()
    css_pipeline.run()

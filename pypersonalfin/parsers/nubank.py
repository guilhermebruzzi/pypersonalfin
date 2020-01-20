from .base import BaseParser


class NubankParser(BaseParser):
    def __init__(self):
        super().__init__('nubank')


nubank = NubankParser()

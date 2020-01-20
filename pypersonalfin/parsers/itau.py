from .base import BaseParser


class ItauParser(BaseParser):
    def __init__(self):
        super().__init__('itau')


itau = ItauParser()

from .base import BaseParser


class ItauParser(BaseParser):
    def __init__(self, locale):
        super().__init__('itau', locale, ';')

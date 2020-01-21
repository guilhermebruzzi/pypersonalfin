from .base import BaseParser


class NubankParser(BaseParser):
    def __init__(self, locale):
        super().__init__('nubank', locale)

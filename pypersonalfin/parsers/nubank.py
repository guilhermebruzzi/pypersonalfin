from .base import BaseParser


class NubankParser(BaseParser):
    def __init__(self, locale):
        super().__init__('nubank', locale)

    # On Nubank exits of cash are positive numbers, so we fix it here
    def get_amount(self, amount):
        amount = super().get_amount(amount)

        if not isinstance(amount, int):
            return amount

        return -1 * amount

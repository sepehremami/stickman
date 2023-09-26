class Player:
    def __init__(self) -> None:
        self.money = 1000

    def get_money(self):
        return self.money

    def spend_money(self, money):
        self.money -= money

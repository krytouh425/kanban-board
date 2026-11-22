# Модуль уведомлений — оповещаем о важных событиях на доске
# Показывает предупреждения при запуске приложения

from datetime import datetime


class UvedomleniyaDoski:
    def __init__(self, board):
        self.board = board
        self.vremya = datetime.now()

    def _vozrast_kartochki(self, card):
        try:
            data = datetime.strptime(card.created_at, "%Y-%m-%d %H:%M")
            return (self.vremya - data).days
        except ValueError:
            return 0

    def srochnye(self):
        # карточки с высоким приоритетом
        return [
            card for card in self.board.cards.values()
            if card.priority == "high"
        ]

    def zavisshie(self, dney=5):
        # карточки которые долго не двигаются
        return [
            (card, self._vozrast_kartochki(card))
            for card in self.board.cards.values()
            if self._vozrast_kartochki(card) >= dney
        ]

    def pokazat(self):
        srochnye = self.srochnye()
        zavisshie = self.zavisshie()

        est_uvedomleniya = False

        if srochnye:
            est_uvedomleniya = True
            print(f"\nСРОЧНЫЕ КАРТОЧКИ ({len(srochnye)}):")
            print("-" * 40)
            for card in srochnye:
                col = self.board.get_column(card.column_id)
                col_name = col.title if col else "неизвестно"
                print(f"  {card.title} [{col_name}]")

        if zavisshie:
            est_uvedomleniya = True
            print(f"\nДАВНО НЕ ЗАКРЫТЫЕ ({len(zavisshie)}):")
            print("-" * 40)
            for card, dney in sorted(zavisshie, key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {card.title} — {dney} дней")

        if not est_uvedomleniya:
            print("\n✓ Срочных уведомлений нет\n")
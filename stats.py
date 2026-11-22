# Модуль статистики — анализируем активность на доске
# Используется для отчётов о продуктивности команды

from datetime import datetime
from collections import Counter


class StatistikaDoski:
    def __init__(self, board):
        self.board = board
        self.vremya = datetime.now()

    def po_prioritetam(self):
        return Counter(card.priority for card in self.board.cards.values())

    def po_kolonkam(self):
        return {
            col.title: len(col.card_ids)
            for col in self.board.columns
        }

    def starye_kartochki(self, dney=7):
        # карточки которые висят дольше N дней
        starye = []
        for card in self.board.cards.values():
            try:
                data = datetime.strptime(card.created_at, "%Y-%m-%d %H:%M")
                vozrast = (self.vremya - data).days
                if vozrast >= dney:
                    starye.append((card, vozrast))
            except ValueError:
                continue
        return sorted(starye, key=lambda x: x[1], reverse=True)

    def vyvesti(self):
        po_prior = self.po_prioritetam()
        po_kol = self.po_kolonkam()
        starye = self.starye_kartochki()

        print(f"\n{'=' * 45}")
        print(f"  СТАТИСТИКА ДОСКИ")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 45}")
        print(f"  Всего карточек: {len(self.board.cards)}")

        print(f"\n  По колонкам:")
        for kolonka, count in po_kol.items():
            print(f"    {kolonka}: {count}")

        print(f"\n  По приоритетам:")
        print(f"    Высокий: {po_prior.get('high', 0)}")
        print(f"    Обычный: {po_prior.get('normal', 0)}")
        print(f"    Низкий:  {po_prior.get('low', 0)}")

        if starye:
            print(f"\n  Давно не закрытые (топ 3):")
            for card, dney in starye[:3]:
                print(f"    {card.title} — {dney} дней")

        print(f"{'=' * 45}\n")
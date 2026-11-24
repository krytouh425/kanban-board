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
        vsego = len(self.board.cards)

        # считаем процент выполненных
        vypolneno = po_kol.get(
            self.board.columns[-1].title, 0
        ) if self.board.columns else 0
        protsent = round(vypolneno / vsego * 100) if vsego > 0 else 0
        progress = "█" * (protsent // 10) + "░" * (10 - protsent // 10)

        print(f"\n{'=' * 45}")
        print(f"  СТАТИСТИКА ДОСКИ")
        print(f"  Дата: {self.vremya.strftime('%d.%m.%Y')}")
        print(f"{'=' * 45}")
        print(f"  Всего карточек: {vsego}")
        print(f"  Прогресс: {progress} {protsent}%")

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
# Модуль поиска — ищем карточки по разным критериям
# Используется для быстрого нахождения нужных задач

from datetime import datetime


class PoiskKartochek:
    def __init__(self, board):
        self.board = board

    def po_nazvaniyu(self, zapros):
        # поиск по частичному совпадению в названии
        zapros = zapros.lower().strip()
        return [
            card for card in self.board.cards.values()
            if zapros in card.title.lower()
        ]

    def po_opisaniyu(self, zapros):
        # поиск по описанию карточки
        zapros = zapros.lower().strip()
        return [
            card for card in self.board.cards.values()
            if zapros in card.description.lower()
        ]

    def po_tegu(self, teg):
        # поиск по тегу
        return [
            card for card in self.board.cards.values()
            if teg in card.tags
        ]

    def polnyy_poisk(self, zapros):
        # ищем по названию и описанию одновременно
        zapros = zapros.lower().strip()
        rezultat = []
        for card in self.board.cards.values():
            if (zapros in card.title.lower() or
                    zapros in card.description.lower()):
                rezultat.append(card)
        return rezultat

    def vyvesti(self, kartochki, zapros=""):
        if not kartochki:
            print(f"По запросу '{zapros}' ничего не найдено")
            return

        print(f"\n{'=' * 45}")
        print(f"  РЕЗУЛЬТАТЫ ПОИСКА ({len(kartochki)})")
        print(f"{'=' * 45}")
        for card in kartochki:
            col = self.board.get_column(card.column_id)
            col_name = col.title if col else "неизвестно"
            print(f"  [{card.priority}] {card.title}")
            print(f"    Колонка: {col_name}")
            if card.description:
                print(f"    {card.description[:50]}...")
        print(f"{'=' * 45}\n")
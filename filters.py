# Модуль фильтрации — фильтруем карточки по разным критериям
# Используется для поиска нужных задач на доске

from datetime import datetime


class FiltrKarotchek:
    def __init__(self, board):
        self.board = board

    def po_prioritetu(self, prioritet):
        # возвращаем карточки с нужным приоритетом
        return [
            card for card in self.board.cards.values()
            if card.priority == prioritet
        ]

    def po_kolonke(self, column_id):
        # все карточки в конкретной колонке
        col = self.board.get_column(column_id)
        if not col:
            return []
        return [
            self.board.cards[card_id]
            for card_id in col.card_ids
            if card_id in self.board.cards
        ]

    def po_tegu(self, teg):
        # карточки с конкретным тегом
        return [
            card for card in self.board.cards.values()
            if teg in card.tags
        ]

    def po_klyuchevomu_slovu(self, slovo):
        # поиск по названию и описанию
        slovo = slovo.lower()
        return [
            card for card in self.board.cards.values()
            if slovo in card.title.lower()
            or slovo in card.description.lower()
        ]

    def statistika(self):
        # общая статистика по доске
        vsego = len(self.board.cards)
        po_prioritetam = {"high": 0, "normal": 0, "low": 0}
        po_kolonkam = {}

        for card in self.board.cards.values():
            po_prioritetam[card.priority] = po_prioritetam.get(card.priority, 0) + 1

        for col in self.board.columns:
            po_kolonkam[col.title] = len(col.card_ids)

        return {
            "vsego": vsego,
            "po_prioritetam": po_prioritetam,
            "po_kolonkam": po_kolonkam
        }
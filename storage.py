# Модуль хранения — сохраняем доску в JSON файл
# Все данные хранятся локально рядом с приложением

import json
import os
from models import Board, Column, Card

BOARD_FILE = "board.json"


class BoardStorage:
    def __init__(self, filepath=BOARD_FILE):
        self.filepath = filepath

    def save(self, board):
        # сериализуем всю доску в JSON
        danye = {
            "title": board.title,
            "columns": [c.to_dict() for c in board.columns],
            "cards": {id: card.to_dict() for id, card in board.cards.items()}
        }
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)

    def load(self):
        # загружаем доску из JSON
        if not os.path.exists(self.filepath):
            return self._sozdat_novuyu()

        with open(self.filepath, encoding="utf-8") as f:
            danye = json.load(f)

        board = Board(danye["title"])
        board.columns = [Column.from_dict(c) for c in danye["columns"]]
        board.cards = {
            id: Card.from_dict(card)
            for id, card in danye["cards"].items()
        }
        return board

    def _sozdat_novuyu(self):
        # создаём новую доску с дефолтными колонками
        board = Board()
        board.add_column("Нужно сделать")
        board.add_column("В процессе")
        board.add_column("Готово")
        self.save(board)
        return board
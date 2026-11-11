# Модели данных — основные сущности Kanban доски
# Card — карточка задачи, Column — колонка, Board — вся доска

from datetime import datetime
import uuid


class Card:
    def __init__(self, title, description="", priority="normal", column_id=None):
        self.id = str(uuid.uuid4())[:8]  # короткий уникальный id
        self.title = title
        self.description = description
        self.priority = priority          # low / normal / high
        self.column_id = column_id
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tags = []                    # список тегов

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "column_id": self.column_id,
            "created_at": self.created_at,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        card = cls(data["title"], data["description"], data["priority"])
        card.id = data["id"]
        card.column_id = data["column_id"]
        card.created_at = data["created_at"]
        card.tags = data.get("tags", [])
        return card

    def __repr__(self):
        return f"Card({self.id}: {self.title} [{self.priority}])"


class Column:
    def __init__(self, title, position=0):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.position = position  # порядок колонки на доске
        self.card_ids = []        # список id карточек в колонке

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "position": self.position,
            "card_ids": self.card_ids
        }

    @classmethod
    def from_dict(cls, data):
        col = cls(data["title"], data["position"])
        col.id = data["id"]
        col.card_ids = data.get("card_ids", [])
        return col


class Board:
    def __init__(self, title="My Kanban Board"):
        self.title = title
        self.columns = []  # список Column
        self.cards = {}    # словарь id -> Card

    def add_column(self, title):
        col = Column(title, position=len(self.columns))
        self.columns.append(col)
        return col

    def add_card(self, title, column_id, description="", priority="normal"):
        card = Card(title, description, priority, column_id)
        self.cards[card.id] = card
        col = self.get_column(column_id)
        if col:
            col.card_ids.append(card.id)
        return card

    def get_column(self, column_id):
        return next((c for c in self.columns if c.id == column_id), None)

    def get_card(self, card_id):
        return self.cards.get(card_id)

    def move_card(self, card_id, new_column_id):
        # перемещаем карточку из одной колонки в другую
        card = self.get_card(card_id)
        if not card:
            return False

        old_col = self.get_column(card.column_id)
        if old_col and card_id in old_col.card_ids:
            old_col.card_ids.remove(card_id)

        new_col = self.get_column(new_column_id)
        if new_col:
            new_col.card_ids.append(card_id)
            card.column_id = new_column_id
            return True
        return False
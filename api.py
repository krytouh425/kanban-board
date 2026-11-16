# Дополнительные API роуты — управление колонками и поиск
# Вынесено из app.py для чистоты кода

from flask import Blueprint, request, jsonify
from storage import BoardStorage

api = Blueprint("api", __name__)
storage = BoardStorage()


@api.route("/api/column", methods=["POST"])
def add_column():
    # добавляем новую колонку на доску
    board = storage.load()
    danye = request.json

    if not danye.get("title"):
        return jsonify({"error": "Название обязательно"}), 400

    col = board.add_column(danye["title"])
    storage.save(board)
    return jsonify(col.to_dict()), 201


@api.route("/api/card/<card_id>", methods=["PUT"])
def update_card(card_id):
    # обновляем данные карточки
    board = storage.load()
    card = board.get_card(card_id)

    if not card:
        return jsonify({"error": "Карточка не найдена"}), 404

    danye = request.json
    if "title" in danye:
        card.title = danye["title"]
    if "description" in danye:
        card.description = danye["description"]
    if "priority" in danye:
        card.priority = danye["priority"]

    storage.save(board)
    return jsonify(card.to_dict())


@api.route("/api/search")
def search():
    # поиск карточек по названию
    zapros = request.args.get("q", "").lower().strip()
    if not zapros:
        return jsonify([])

    board = storage.load()
    rezultat = [
        card.to_dict()
        for card in board.cards.values()
        if zapros in card.title.lower() or zapros in card.description.lower()
    ]
    return jsonify(rezultat)
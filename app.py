# Основной Flask сервер — обрабатывает запросы и отдаёт страницы
# Запуск: python app.py

from flask import Flask, render_template, request, jsonify
from storage import BoardStorage

app = Flask(__name__)
storage = BoardStorage()


@app.route("/")
def index():
    # главная страница — отдаём доску
    board = storage.load()
    return render_template("index.html", board=board)


@app.route("/api/card", methods=["POST"])
def add_card():
    # создаём новую карточку
    board = storage.load()
    danye = request.json

    if not danye.get("title"):
        return jsonify({"error": "Название обязательно"}), 400

    card = board.add_card(
        title=danye["title"],
        column_id=danye["column_id"],
        description=danye.get("description", ""),
        priority=danye.get("priority", "normal")
    )
    storage.save(board)
    return jsonify(card.to_dict()), 201


@app.route("/api/card/<card_id>/move", methods=["POST"])
def move_card(card_id):
    # перемещаем карточку в другую колонку
    board = storage.load()
    danye = request.json

    uspeshno = board.move_card(card_id, danye["column_id"])
    if not uspeshno:
        return jsonify({"error": "Карточка не найдена"}), 404

    storage.save(board)
    return jsonify({"ok": True})


@app.route("/api/card/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    # удаляем карточку
    board = storage.load()
    card = board.get_card(card_id)

    if not card:
        return jsonify({"error": "Карточка не найдена"}), 404

    col = board.get_column(card.column_id)
    if col and card_id in col.card_ids:
        col.card_ids.remove(card_id)
    del board.cards[card_id]

    storage.save(board)
    return jsonify({"ok": True})


@app.route("/api/board")
def get_board():
    # отдаём данные доски в JSON для фронтенда
    board = storage.load()
    return jsonify({
        "title": board.title,
        "columns": [c.to_dict() for c in board.columns],
        "cards": {id: card.to_dict() for id, card in board.cards.items()}
    })


if __name__ == "__main__":
    app.run(debug=True)
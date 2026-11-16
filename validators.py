# Валидация входных данных — проверяем данные перед сохранением
# Защищаем API от некорректных запросов

VALID_PRIORITIES = ("low", "normal", "high")
MAX_TITLE_LENGTH = 100
MAX_DESC_LENGTH = 500


def validate_card(data):
    oshibki = []

    # проверяем название
    title = data.get("title", "").strip()
    if not title:
        oshibki.append("Название карточки обязательно")
    elif len(title) > MAX_TITLE_LENGTH:
        oshibki.append(f"Название слишком длинное (максимум {MAX_TITLE_LENGTH} символов)")

    # проверяем описание
    desc = data.get("description", "")
    if len(desc) > MAX_DESC_LENGTH:
        oshibki.append(f"Описание слишком длинное (максимум {MAX_DESC_LENGTH} символов)")

    # проверяем приоритет
    priority = data.get("priority", "normal")
    if priority not in VALID_PRIORITIES:
        oshibki.append(f"Неверный приоритет '{priority}', доступны: {', '.join(VALID_PRIORITIES)}")

    # проверяем column_id
    if not data.get("column_id"):
        oshibki.append("Колонка обязательна")

    return oshibki


def validate_column(data):
    oshibki = []

    title = data.get("title", "").strip()
    if not title:
        oshibki.append("Название колонки обязательно")
    elif len(title) > 50:
        oshibki.append("Название колонки слишком длинное (максимум 50 символов)")

    return oshibki


def validate_move(data):
    oshibki = []

    if not data.get("column_id"):
        oshibki.append("ID колонки обязателен")

    return oshibki
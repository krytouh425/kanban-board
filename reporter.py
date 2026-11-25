# Модуль отчётов — формируем отчёт по доске для руководства
# Используется для еженедельных статус-апдейтов команды

import os
from datetime import datetime


class ReporterDoski:
    def __init__(self, board):
        self.board = board
        self.vremya = datetime.now()

    def _statistika(self):
        vsego = len(self.board.cards)
        po_kolonkam = {}
        po_prioritetam = {"high": 0, "normal": 0, "low": 0}

        for col in self.board.columns:
            po_kolonkam[col.title] = len(col.card_ids)

        for card in self.board.cards.values():
            po_prioritetam[card.priority] += 1

        # последняя колонка — выполненные
        vypolneno = len(self.board.columns[-1].card_ids) if self.board.columns else 0
        protsent = round(vypolneno / vsego * 100) if vsego > 0 else 0

        return {
            "vsego": vsego,
            "vypolneno": vypolneno,
            "protsent": protsent,
            "po_kolonkam": po_kolonkam,
            "po_prioritetam": po_prioritetam
        }

    def v_txt(self, filepath=None):
        if not filepath:
            vremya_str = self.vremya.strftime("%Y%m%d_%H%M")
            filepath = f"report_{vremya_str}.txt"

        stat = self._statistika()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"ОТЧЁТ ПО ДОСКЕ — {self.board.title}\n")
            f.write(f"Дата: {self.vremya.strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Всего карточек: {stat['vsego']}\n")
            f.write(f"Выполнено: {stat['vypolneno']} ({stat['protsent']}%)\n\n")

            f.write("По колонкам:\n")
            for kolonka, count in stat["po_kolonkam"].items():
                f.write(f"  {kolonka}: {count}\n")

            f.write("\nПо приоритетам:\n")
            f.write(f"  Высокий: {stat['po_prioritetam']['high']}\n")
            f.write(f"  Обычный: {stat['po_prioritetam']['normal']}\n")
            f.write(f"  Низкий:  {stat['po_prioritetam']['low']}\n")

            f.write("\nКарточки по колонкам:\n")
            for col in self.board.columns:
                f.write(f"\n[ {col.title} ]\n")
                for card_id in col.card_ids:
                    card = self.board.cards.get(card_id)
                    if card:
                        f.write(f"  [{card.priority}] {card.title}\n")

        print(f"✓ Отчёт сохранён: {filepath}")
        return filepath
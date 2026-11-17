# Модуль экспорта — выгружаем доску в разные форматы
# Используется для резервных копий и отчётов

import json
import csv
import os
from datetime import datetime

EXPORT_DIR = "exports"


class ExporterDoski:
    def __init__(self, board, export_dir=EXPORT_DIR):
        self.board = board
        self.export_dir = export_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def _imya_fayla(self, format):
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.export_dir, f"board_{vremya}.{format}")

    def v_json(self):
        # полный экспорт доски в JSON
        fayl = self._imya_fayla("json")
        danye = {
            "title": self.board.title,
            "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "columns": [c.to_dict() for c in self.board.columns],
            "cards": {id: card.to_dict() for id, card in self.board.cards.items()}
        }
        with open(fayl, "w", encoding="utf-8") as f:
            json.dump(danye, f, ensure_ascii=False, indent=2)
        print(f"✓ Доска экспортирована в JSON: {fayl}")
        return fayl

    def v_csv(self):
        # экспортируем все карточки в CSV
        fayl = self._imya_fayla("csv")
        kolonki_map = {col.id: col.title for col in self.board.columns}

        with open(fayl, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Название", "Описание", "Приоритет", "Колонка", "Создано"])
            for card in self.board.cards.values():
                writer.writerow([
                    card.id,
                    card.title,
                    card.description,
                    card.priority,
                    kolonki_map.get(card.column_id, ""),
                    card.created_at
                ])
        print(f"✓ Карточки экспортированы в CSV: {fayl}")
        return fayl

    def v_txt(self):
        # читаемый текстовый отчёт
        fayl = self._imya_fayla("txt")
        with open(fayl, "w", encoding="utf-8") as f:
            f.write(f"{self.board.title}\n")
            f.write(f"Экспорт: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("=" * 50 + "\n\n")

            for col in self.board.columns:
                f.write(f"[ {col.title} ] ({len(col.card_ids)} карточек)\n")
                f.write("-" * 40 + "\n")
                for card_id in col.card_ids:
                    card = self.board.cards.get(card_id)
                    if card:
                        f.write(f"  [{card.priority}] {card.title}\n")
                        if card.description:
                            f.write(f"  {card.description}\n")
                f.write("\n")

        print(f"✓ Отчёт сохранён: {fayl}")
        return fayl
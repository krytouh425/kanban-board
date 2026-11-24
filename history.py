# Модуль истории — отслеживаем все изменения на доске
# Позволяет увидеть кто и когда менял карточки

import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"


class HistoryDoski:
    def __init__(self, filepath=HISTORY_FILE):
        self.filepath = filepath

    def _zagruzit(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, encoding="utf-8") as f:
            return json.load(f)

    def _sohranit(self, istoriya):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(istoriya, f, ensure_ascii=False, indent=2)

    def zapisat(self, deystvie, card_id, detali=""):
        istoriya = self._zagruzit()
        istoriya.append({
            "vremya": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deystvie": deystvie,
            "card_id": card_id,
            "detali": detali
        })
        self._sohranit(istoriya)

    def poslednie(self, kolichestvo=20):
        istoriya = self._zagruzit()
        return istoriya[-kolichestvo:]

    def po_kartochke(self, card_id):
        istoriya = self._zagruzit()
        return [z for z in istoriya if z["card_id"] == card_id]

    def vyvesti(self, kolichestvo=10):
        zapisi = self.poslednie(kolichestvo)
        if not zapisi:
            print("История пуста")
            return

        print(f"\n{'=' * 50}")
        print(f"  ИСТОРИЯ ИЗМЕНЕНИЙ")
        print(f"{'=' * 50}")
        for z in reversed(zapisi):
            print(f"  [{z['vremya']}] {z['deystvie']}")
            if z['detali']:
                print(f"    {z['detali']}")
        print(f"{'=' * 50}\n")

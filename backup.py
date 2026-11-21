# Модуль резервного копирования — автоматически сохраняем доску
# Запускается перед каждым изменением данных

import os
import json
import shutil
from datetime import datetime

BACKUP_DIR = "backups"
MAX_BACKUPS = 10


class BackupDoski:
    def __init__(self, source_file="board.json", backup_dir=BACKUP_DIR):
        self.source_file = source_file
        self.backup_dir = backup_dir
        self._sozdat_papku()

    def _sozdat_papku(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _imya_fayla(self):
        vremya = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.backup_dir, f"board_backup_{vremya}.json")

    def sozdat(self):
        # создаём резервную копию перед изменением
        if not os.path.exists(self.source_file):
            return None

        backup = self._imya_fayla()
        shutil.copy2(self.source_file, backup)
        self._udalit_starye()
        print(f"✓ Резервная копия создана: {backup}")
        return backup

    def _udalit_starye(self):
        fayly = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith("board_backup_")
        ])
        while len(fayly) > MAX_BACKUPS:
            os.remove(os.path.join(self.backup_dir, fayly.pop(0)))

    def vosstanovit(self, backup_fayl):
        if not os.path.exists(backup_fayl):
            raise FileNotFoundError(f"Резервная копия не найдена: {backup_fayl}")
        shutil.copy2(backup_fayl, self.source_file)
        print(f"✓ Доска восстановлена из: {backup_fayl}")

    def spisok(self):
        fayly = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith("board_backup_")
        ], reverse=True)

        if not fayly:
            print("Резервных копий нет")
            return []

        print(f"\nРезервные копии ({len(fayly)}):")
        for f in fayly:
            razmer = os.path.getsize(os.path.join(self.backup_dir, f)) / 1024
            print(f"  {f} ({razmer:.1f} КБ)")
        return fayly
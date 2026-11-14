// Логика фронтенда — drag & drop и работа с API
// Используем нативный HTML5 Drag and Drop API

let draggedCard = null;

// ===== DRAG & DROP =====

document.addEventListener('DOMContentLoaded', () => {
    initDragAndDrop();
});

function initDragAndDrop() {
    // вешаем события на все карточки
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('dragstart', onDragStart);
        card.addEventListener('dragend', onDragEnd);
    });

    // вешаем события на все колонки
    document.querySelectorAll('.column').forEach(col => {
        col.addEventListener('dragover', onDragOver);
        col.addEventListener('drop', onDrop);
        col.addEventListener('dragleave', onDragLeave);
    });
}

function onDragStart(e) {
    draggedCard = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this.dataset.cardId);
}

function onDragEnd() {
    this.classList.remove('dragging');
    document.querySelectorAll('.column').forEach(col => {
        col.classList.remove('drag-over');
    });
    draggedCard = null;
}

function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    this.classList.add('drag-over');
}

function onDragLeave() {
    this.classList.remove('drag-over');
}

async function onDrop(e) {
    e.preventDefault();
    this.classList.remove('drag-over');

    const cardId = e.dataTransfer.getData('text/plain');
    const columnId = this.dataset.columnId;

    if (!cardId || !columnId) return;

    // перемещаем карточку через API
    const ok = await moveCard(cardId, columnId);
    if (ok) {
        // перезагружаем страницу чтобы обновить счётчики
        location.reload();
    }
}

// ===== API =====

async function moveCard(cardId, columnId) {
    try {
        const res = await fetch(`/api/card/${cardId}/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ column_id: columnId })
        });
        return res.ok;
    } catch (err) {
        console.error('Ошибка перемещения:', err);
        return false;
    }
}

async function deleteCard(cardId) {
    if (!confirm('Удалить карточку?')) return;

    try {
        const res = await fetch(`/api/card/${cardId}`, {
            method: 'DELETE'
        });
        if (res.ok) location.reload();
    } catch (err) {
        console.error('Ошибка удаления:', err);
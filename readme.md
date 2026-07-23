# MAX rent bot v1

Современный бот для MAX, который показывает свободные помещения АО «ТомскАгроИнвест», открывает карточки объектов и подводит пользователя к заявке.

## Возможности

- приветствие и главное меню;
- меню команд MAX: `/start`, `/menu`, `/clear`, `/help`;
- список свободных помещений из `data/premises.csv`;
- карточка помещения с площадью, ценой, типом, зданием, этажом и описанием;
- быстрый возврат к списку;
- команда `/clear` для удаления доступной боту истории сообщений в чате;
- заглушки для заявки, документов и контактов, чтобы меню v1 было цельным.

## Запуск

1. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

2. Создайте `.env` и укажите токен:

   ```env
   BOT_TOKEN=your_max_bot_token
   ```

3. Запустите бота:

   ```bash
   python app.py
   ```

## Данные

CSV-файл помещений находится в `data/premises.csv`. Для публикации помещения в боте установите `status` в `free`.

## Упрощение структуры

Удалены лишние файлы, которые были пустыми, дублировали будущую функциональность или не использовались в v1:

- `Bot.zip` — архив исходников больше не нужен после распаковки проекта в репозиторий;
- `data/applications.csv` — заявки в v1 не сохраняются в CSV;
- `handlers/application.py`, `handlers/contacts.py`, `handlers/documents.py` — пустые обработчики заменены callback-логикой в `handlers/callbacks.py`;
- `keyboards/keyboards.py` — пустой файл, общий builder находится в `keyboards/main_menu.py`;
- `models/application.py` — модель заявки не используется до полноценного сценария заявок;
- `repository/repository.py` — абстракция не используется текущим CSV-репозиторием;
- `services/application_service.py`, `services/document_service.py`, `services/menu_service.py`, `services/pagination.py` — пустые/неиспользуемые сервисы;
- `storage/session.py` — in-memory session не используется текущими сценариями;
- `utils/csv_utils.py`, `utils/validators.py` — пустые утилиты.

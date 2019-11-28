# AsyncTelegramStarter


### Как протестировать

0. Нужен `python3.7.5`

1. Установить зависимости
    ```bash
    pip3 install -r requirements.txt
    ```

2. Добавить файл `config.json` на верхний уровень рядом с файлом `coniig_example.json`.
  Структура должна быть как в файле примере конфига.
    ```json
    {
        "token": "TOKEN_FROM_BOTFATHER",
        "proxy": null
    }
    ```

3. Запустить файл `bot.py` и всё будет работать.

4. Можно менять состояния, их порядок и т.д. в папке `states` когда бот выключен, главное чтобы всегда было какое-то одно задекорированное декоратором `dispatcher.Dispatcher.primary_state`, с него будет начинаться вся работа.

# AsyncTelegramStarter


### Как протестировать

0. Нужно иметь `python3.7.5`.

1. Установить зависимости.
    ```bash
    pip3 install -r requirements.txt
    ```

2. Добавить файл `config.json` на верхний уровень рядом с файлом `config_example.json`.
  Структура должна быть как в файле примере конфига.
    ```json
    {
        "token": "TOKEN_FROM_BOTFATHER",
        "proxy": null
    }
    ```

3. Запустить файл `bot.py` и всё будет работать.

4. Можно менять состояния, их порядок и т.д. в папке `states` когда бот выключен, главное чтобы всегда было какое-то одно c аргументов `primary_state=True` в `state_handler` (`@dp.state_handler(primary_state=True)`), его значение равно `None` с него будет начинаться вся работа.

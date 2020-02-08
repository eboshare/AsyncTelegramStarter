# AsyncTelegramStarter


### How to test

- python3.7 is needed

- Install requirements.
    ```bash
    pip3 install -r requirements.txt
    ```

- Add the file `config.py` on the top level next to `config_example.json`
    The structure must be the same as in the example file.

- You can change states, their order etc. in the `states` folder. But you need to always have the one state with the argument `primary_state=True` (example: `@dp.state_handler(primary_state=True)`). This configures the primary state which value is `None` and the whole process begins with it.

- Run `bot.py` file.

- - -

- By the way in the `preparation.py` file `utils.storage.MotorStorage` is used.
    ```python
    mongo_client = AsyncIOMotorClient(config.mongo.uri)
    storage = MotorStorage(
        mongo_client=mongo_client,
        mongo_database=mongo_client[config.mongo.database]
    )

    dispatcher = AiogramBasedDispatcher(bot=bot, storage=storage)
    ```
    If you don't want to use it you can use `aiogram.contrib.fsm_storage.memory.MemoryStorage` as a test storage.

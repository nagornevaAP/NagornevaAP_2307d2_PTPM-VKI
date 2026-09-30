import logging

from logger_config import setup_logging
from validator import register_user


def main():
    setup_logging()
    logging.info("Приложение запущено")

    while True:
        login = input("Логин (или q для выхода): ")
        if login.strip().lower() == "q":
            break
        password = input("Пароль: ")
        confirm = input("Подтверждение пароля: ")

        success, message = register_user(login, password, confirm)
        print(f"Результат: {success}")
        print(f"Сообщение: '{message}'")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()
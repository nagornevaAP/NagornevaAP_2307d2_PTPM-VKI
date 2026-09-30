import hashlib
import logging
import re
import string

# Чёрный список логинов
BLACKLIST = {"admin", "administrator", "root", "user", "test", "guest", "qwerty", "12345"}

# маски
PHONE_RE = re.compile(r"^\+\d-\d{3}-\d{3}-\d{4}$") # +x-xxx-xxx-xxxx
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
LOGIN_RE = re.compile(r"^[A-Za-z0-9_]+ n$") # латиница, цифры, _

SPECIALS = re.escape(string.punctuation) # !"#$%&... и т.д.
PASSWORD_ALLOWED_RE = re.compile(r"^[А-Яа-яЁё0-9" + SPECIALS + r"]+$")
UPPER_RE = re.compile(r"[А-ЯЁ]")
LOWER_RE = re.compile(r"[а-яё]")
DIGIT_RE = re.compile(r"[0-9]")
SPECIAL_RE = re.compile(r"[" + SPECIALS + r"]")

MIN_LOGIN_LEN = 5
MIN_PASSWORD_LEN = 7


def mask_password(password):
    if not isinstance(password, str):
        return "<не строка>"
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return "***" + digest[:10]


def check_login(login):
    if login == "":
        return "Логин не может быть пустым"

    if login.lower() in BLACKLIST:
        return "Этот логин запрещён (находится в чёрном списке)"

    if "@" in login:
        if not EMAIL_RE.match(login):
            return "Неверный формат email"
    elif login.startswith("+"):
        if not PHONE_RE.match(login):
            return "Неверный формат телефона (нужен вид +x-xxx-xxx-xxxx)"
    else:
        if len(login) < MIN_LOGIN_LEN:
            return f"Логин слишком короткий (минимум {MIN_LOGIN_LEN} символов)"
        if not LOGIN_RE.match(login):
            return "Логин может содержать только латиницу, цифры и знак _"
    return ""


def check_password(password, confirm):
    if password == "":
        return "Пароль не может быть пустым"
    if len(password) < MIN_PASSWORD_LEN:
        return f"Пароль слишком короткий (минимум {MIN_PASSWORD_LEN} символов)"
    if not PASSWORD_ALLOWED_RE.match(password):
        return "Пароль может содержать только кириллицу, цифры и спецсимволы"
    if not UPPER_RE.search(password):
        return "В пароле нет заглавной буквы"
    if not LOWER_RE.search(password):
        return "В пароле нет строчной буквы"
    if not DIGIT_RE.search(password):
        return "В пароле нет цифры"
    if not SPECIAL_RE.search(password):
        return "В пароле нет спецсимвола"
    if password != confirm:
        return "Пароль и подтверждение не совпадают"
    return ""


def register_user(login, password, confirm):
    params = (f"login={login!r}, password={mask_password(password)}, "
    f"confirm={mask_password(confirm)}")
    logging.debug(f"Получен запрос: {params}")

    try:
        error = check_login(login)
        if not error:
            error = check_password(password, confirm)
    except Exception:
        logging.exception(f"Неуспешный запрос: {params} - непредвиденная ошибка")
        return False, "Внутренняя ошибка при проверке данных"

    if error:
        logging.error(f"Неуспешный запрос: {params} - {error}")
        return False, error

    logging.info(f"Успешный запрос: {params} - регистрация прошла успешно")
    return True, ""
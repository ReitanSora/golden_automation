from datetime import datetime


def compare_date(saved_date: str, new_date: str) -> bool:
    date_24_format = '%Y-%m-%d %H:%M:%S'

    saved_date_formated = datetime.strptime(saved_date, date_24_format)
    new_date_formated = datetime.strptime(new_date, date_24_format)

    return new_date_formated > saved_date_formated

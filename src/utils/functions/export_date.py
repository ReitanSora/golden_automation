from datetime import datetime


def export_date():
    archivo = open('src/storage/date.txt', "w")

    archivo.write(str(datetime.now())[:-7])

    archivo.close()

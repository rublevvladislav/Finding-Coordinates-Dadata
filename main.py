import dadata_requests
import database


def set_settings():
    db = database.DataBase('sqlite.db')
    db.get_connection()
    while True:
        print(f'Текущие настройки: \nAPI ключ: {db.get_api_key()}')
        print(f'Базовый URL: {db.get_url()}')
        print(f'Язык: {db.get_language()}\n')
        print('Для изменения API ключа введите 1')
        print('Для изменения URL введите 2')
        print('Для смены языка (en/ru) введите 3')
        print('Для выхода из меню настроек введите 0')
        cmd = input()
        if cmd == '1':
            cmd = input('Оставте поле пустым для отмены\nВведите новый API ключ:')
            if cmd != '':
                db.set_api_key(cmd)
        elif cmd == '2':
            cmd = input('Оставте поле пустым для отмены\nВведите новый url:')
            if cmd != '':
                db.set_url(cmd)
        elif cmd == '3':
            if db.get_language() == 'ru':
                db.set_language('en')
                print('Язык изменен на английский')
            else:
                db.set_language('ru')
                print('Язык изменен на русский')
        elif cmd == '0':
            db.close_connection()
            return True
        elif cmd == 'exit':
            db.close_connection()
            return False


def search_address(query, api_key, language):
    api = dadata_requests.DadataRequests(api_key, language)
    if api.get_address(query):
        idx = input('Выберите номер адреса, координаты которого хотите узнать: ')
        if idx == '':
            return
        while not api.get_coordinates(idx):
            idx = input('Введите один из доступных номеров или оставьте поле пустым для отмены: ')
            if idx == '':
                return
    else:
        print('Не удалось найти адреса, попробуйте изменить запрос.')


def main():
    language = 'ru'
    quit_list = ['q', 'quit', 'exit']
    settings_list = ['set', 'settings', 'config']
    print('Эта программа предназначена для определения географических координат интересующих Вас объектов.')
    db = database.DataBase('sqlite.db')
    db.get_connection()
    if db.is_empty():
        api_key = input('Для начала работы, пожалуйста, введите API-ключ от сервиса Dadata: ')
        db.insert_data(api_key, language)
    else:
        api_key = db.get_api_key()
        language = db.get_language()
    db.close_connection()
    settings_changed = False
    while True:
        print('*** Для выхода из приложения введите q, quit или exit')
        print('*** Для изменения настроек введите set, settings или config')
        query = input('Для поиска координат введите адрес объекта: ')
        if query.lower() in quit_list:
            exit()
        elif query.lower() in settings_list:
            settings_changed = set_settings()
            if not settings_changed:
                exit()
        else:
            if settings_changed:
                db.get_connection()
                api_key = db.get_api_key()
                language = db.get_language()
                db.close_connection()
                settings_changed = False
            search_address(query, api_key, language)


if __name__ == '__main__':
    main()

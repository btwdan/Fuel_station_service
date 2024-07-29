# Требуется: Написать функцию, которая получает из Сети код страниц из списка и сохраняет его (код) на диск.

import requests
import os

def save_webpages(url_list: list[str], save_directory: str) -> None:
    # Создаем папку для сохранения, если она не существует
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Проходим по каждому URL в списке
    for i, url in enumerate(url_list):
        try:
            # Получаем HTML-код страницы
            response = requests.get(url)
            response.raise_for_status()  # Проверка на успешность запроса

            # Определяем имя файла
            filename = f"page_{i + 1}.html"
            filepath = os.path.join(save_directory, filename)

            # Сохраняем HTML-код на диск
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(response.text)

            print(f"Сохранено: {url} в {filepath}")

        except requests.RequestException as e:
            print(f"Не удалось получить доступ к {url}: {e}")
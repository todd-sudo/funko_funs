import json
import time

from logger import logger
from parser import get_figure
from utils import get_urls, check_folder


def service():
    check_folder()

    ru: bool = False
    exclusive_category: bool = False
    start = input(
        "Выберите действие:\n\n1) Собираем ссылки\n2) Парсим товары по ссылкам\n\n funko --> "
    )

    if start == "1":
        filename_urls = input("Введите название выходного файла --> ")
        category = input("\nВыберите категорию:\n1) Обычный каталог\n2) Эксклюзивы\n\n funko --> ")

        if category == "2":
            exclusive_category = True

        start_time_get_urls = time.monotonic()
        data = get_urls(exclusive=exclusive_category)
        path = f"results/urls/{filename_urls}.json"

        if exclusive_category:
            with open(
                f"results/urls/exclusive/{filename_urls}.json", 
                "a", encoding="utf-8"
            ) as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                logger.success(
                    f"Все ссылки спаршены!"
                    f"\nВремени потрачено: "
                    f"{(time.monotonic() - start_time_get_urls) / 60}"
                )
        else:
            with open(path, "a", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                logger.success(
                    f"Все ссылки спаршены!"
                    f"\nВремени потрачено: "
                    f"{(time.monotonic() - start_time_get_urls) / 60}"
                )


    elif start == "2":
        _lang = False
        _exlusive = False
        lang = input("Переключить на русский? (y/n) --> ")
        if lang in ["y", "Y"]:
            _lang = True
        input_filename = input("Введите название файла с ссылками --> ")
        out_filename = input("Введите название выходного файла --> ")
        category = input("\nВыберите категорию:\n1) Обычный каталог\n2) Эксклюзивы\n\n funko --> ")
        if category == "2":
            _exlusive = True
        start_time = time.monotonic()
        data_object = get_figure(input_filename, _lang, _exlusive)

        if category == "1":
            with open(f"results/detail/{out_filename}.json", "a", encoding="utf-8") as file:
                json.dump(data_object, file, indent=4, ensure_ascii=False)
                logger.success(
                    f"Парсинг завершен!\n"
                    f"Объектов спаршено: {len(data_object)}"
                    f"\nПотрачено времени: {(time.monotonic() - start_time) / 60} минут"
                )
        else:
            with open(f"results/detail/exclusive/{out_filename}.json", "a", encoding="utf-8") as file:
                json.dump(data_object, file, indent=4, ensure_ascii=False)
                logger.success(
                    f"Парсинг завершен!\n"
                    f"Объектов спаршено: {len(data_object)}"
                    f"\nПотрачено времени: {(time.monotonic() - start_time) / 60} минут"
                )


@logger.catch
def main():
    service()


if __name__ == "__main__":
    main()

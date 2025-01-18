# main.py
import os
import shutil
from markdown import generate_pages_recursive

def copy_directory(src, dst):
    """
    Рекурсивно копирует содержимое каталога src в каталог dst.
    Если каталог dst существует, его содержимое удаляется.
    """
    # Удаляем целевой каталог, если он существует
    if os.path.exists(dst):
        print(f"Удаление содержимого каталога: {dst}")
        shutil.rmtree(dst)

    # Создаем целевой каталог
    print(f"Создание каталога: {dst}")
    os.makedirs(dst)

    # Рекурсивно копируем содержимое
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            # Если это каталог, рекурсивно копируем его
            print(f"Копирование каталога: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)
        else:
            # Если это файл, копируем его
            print(f"Копирование файла: {src_path} -> {dst_path}")
            shutil.copy2(src_path, dst_path)


def main():
    # Удаляем все файлы из каталога public
    if os.path.exists("public"):
        shutil.rmtree("public")

    # Копируем статические файлы из static в public
    copy_directory("static", "public")

    # Генерируем страницу из content/index.md
    generate_pages_recursive("content", "template.html", "public")

    

if __name__ == "__main__":
    main()
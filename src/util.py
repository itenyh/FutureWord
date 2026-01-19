import os
import flet as ft

async def _savefiles_as_filters(filepathes: list[str], encoding='utf-8'):

    storage_path = await ft.StoragePaths().get_application_support_directory()
    destination_dir = storage_path + "/filters"
    #如果目录不存在，则创建
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    print(f"文件存储至: {destination_dir}")

    for filepath in filepathes:
        source_file = filepath.path
        filename = os.path.basename(source_file)
        destination_file = os.path.join(destination_dir, filename)
        # 复制文件内容
        with open(source_file, 'r', encoding=encoding) as src, open(destination_file, 'w', encoding=encoding) as dst:
            dst.write(src.read())

def _readfile_as_text(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        return f.read()

def _readfile_as_list(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        return [line.strip() for line in f]

async def _readfiles_in_filters_dir_as_list(encoding='utf-8'):
    storage_path = await ft.StoragePaths().get_application_support_directory()
    directory = storage_path + "/filters"
    filepaths = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    result = []
    for filepath in filepaths:
        filter_words = _readfile_as_list(filepath)
        result.extend(filter_words)
    return result

async def _savelist_to_file(word_list: list[str], encoding='utf-8'):
    path = await ft.FilePicker().save_file(file_name="selection.txt", initial_directory="./")
    if path:
        with open(path, 'w', encoding=encoding) as f:
            f.write('\n'.join(str(item) for item in word_list) + '\n')
    return True

def _exclude(new_list, filter_list):
    return [item for item in new_list if item not in filter_list]


if __name__ == "__main__":
    _savefiles_as_filters(["data/filter.txt"])
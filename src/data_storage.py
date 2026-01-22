from click import pass_obj
from tinydb import TinyDB, Query
import os
import asyncio
import flet as ft
import time

data_dir = None

async def _init_path():

    global data_dir
    storage_path = await ft.StoragePaths().get_application_support_directory()
    data_dir = os.path.join(storage_path, "data")
    os.makedirs(data_dir, exist_ok=True)
    print(f"数据目录: {data_dir}")

class WordsSession:
    def __init__(self, name, wordlist):
        self.name = name
        self.wordlist = [self._word_to_dict(word) for word in wordlist]
        self.create_time = int(time.time())
        self.has_finish = False
        self.finish_time = 0
        self.cur_page = 0

    def word_text_list(self):
        return [word["w"] for word in self.wordlist]

    def to_dict(self):
        return {
            "name": self.name, # 会话名称
            "word_list": self.wordlist, # 单词列表
            "create_time": self.create_time, # 创建时间
            "has_finish": self.has_finish, # 是否完成
            "finish_time": self.finish_time, # 完成时间
            "cur_page": self.cur_page, # 当前页码
        }

    def _word_to_dict(self, word):
        return {
            "w": word, # 单词
            "s": 0 # 选中状态
        }

class WordSessionDao:

    def create_session(self, name, wordlist):
        session = WordsSession(name, wordlist)
        self.db_save(session)
        return session

    def save_session(session: WordsSession, wordlist):
        session.wordlist = wordlist
        self.db_save(session)

    def db_save(self, session: WordsSession):
        if not data_dir:
            print("数据目录未初始化，请先调用 _init_path()")
            return
        print(f"保存会话: {data_dir}")
        filepath = f"{data_dir}/{session.name}.fuw"
        db = TinyDB(filepath)
        db.insert(session.to_dict())


if __name__ == "__main__":

    async def main(page: ft.Page):
        # 最简单一行搞定
        # support_dir = await page.storage_paths.get_application_support_directory()
        # data_dir = os.path.join(support_dir, "data")  # 推荐用 os.path.join
        # os.makedirs(data_dir, exist_ok=True)
        dao = WordSessionDao()
        # print(f"应用支持目录: {support_dir}")
        # print(f"你的数据目录: {data_dir}")
        # dao.create_session("test", ["a", "b", "c"])
        await _init_path()
        page.update()
        dao.create_session("test", ["a", "b", "c"])

    ft.app(target=main)

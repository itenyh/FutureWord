import re

def _exclude(new_list, filter_list):
    return [item for item in new_list if item not in filter_list]
class WordViewItem():
    def __init__(self, word: str):
        self.word = word
        self.selected = False

class WordViewModel():
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.page_column = 3
        self.page_size = self.page_column * self.page_column
        self.word_list = []
        self.worditem_list = []
        self._setup_list()

    def _setup_list(self):
        # input_list = _readfile_as_list('data/product/input.txt')
        # filter_list = _readfile_as_list('data/product/filter.txt')

        # input_list = []
        # filter_list = []
        # self.word_list = _exclude(input_list, filter_list)
        self.worditem_list = [WordViewItem(word) for word in self.word_list]
        self.total_page = (len(self.worditem_list) + self.page_size - 1) // self.page_size

    def update_wordlist(self, words: list[str]):
        self.word_list = words
        self._setup_list()

    def filter_word_list(self, words: list[str]):
        self.word_list = _exclude(self.word_list, words)
        self._setup_list()

    def get_current_word_list(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        if start < 0:
            start = 0
        if end > len(self.worditem_list):
            end = len(self.worditem_list)
        # print("start - end", start, '-' ,end)
        return self.worditem_list[start:end]

    def on_word_clicked(self, index: int, selected: bool):
        real_index = self.current_page * self.page_size + index
        # print(index, real_index, selected, self.worditem_list[real_index].word)
        self.worditem_list[real_index].selected = selected

    def page_change(self, is_next: bool):
        if is_next:
            self.current_page += 1
        else:
            self.current_page -= 1
        if self.current_page < 0:
            self.current_page = 0
        if self.current_page * self.page_size >= len(self.worditem_list):
            self.current_page -= 1

    def selected_words(self):
        selected_words = [item.word for item in self.worditem_list if item.selected]
        return selected_words

    def selected_words_str(self):
        words = self.selected_words()
        return '\n'.join(words)

    def update_wordlist_with_text(self, text: str):
        words = self._createlist_with_text(text)
        self.update_wordlist(words)

    def _createlist_with_text(self, text: str):

        # 允许英文字母、数字、-
        pattern = r"[a-zA-Z][a-zA-Z0-9]*(?:['-][a-zA-Z0-9]+)*"
        words = re.findall(pattern, text)
        
        # 排除重复word
        words = list(set(words))

        return words


if __name__ == '__main__':

    vm = WordViewModel()
    words = vm._createlist_with_text("ab cd 11 abv")
    print(words)
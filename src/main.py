import flet as ft
from word_viewmodel import WordViewModel, WordViewItem

def _readfile_as_text(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        return f.read()

def _readfile_as_list(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        return [line.strip() for line in f]

async def _savelist_to_file(word_list: list[str], encoding='utf-8'):
    path = await ft.FilePicker().save_file(file_name="selection.txt", initial_directory="./")
    if path:
        with open(path, 'w', encoding=encoding) as f:
            f.write('\n'.join(str(item) for item in word_list) + '\n')
    return True

class WordCollectionView(ft.Container):
    def __init__(self, columns: int = 3):
        super().__init__()
        self.columns = columns
        self.button_width = 180

    def refresh(self, word_view_list: list[WordViewItem]):
        button_list = []
        total = self.columns * self.columns
        for i in range(total):
            if i < len(word_view_list):
                item = word_view_list[i]
                button = ft.Button(
                    content=ft.Text(
                        item.word,
                        text_align=ft.TextAlign.CENTER,  # 设置居中
                        size=20,
                        style=ft.TextStyle(
                            height=1.0,  # 关键：行高倍数
                        ),
                    ),
                    key=i,
                    bgcolor=ft.Colors.WHITE,
                    color=ft.Colors.BLACK,
                    width=self.button_width,
                    height=45,
                    on_click=self._button_clicked,
                )
                self._decorate_button(button, item.selected)
            else:
                button = ft.Button(
                    content=ft.Text(
                        text_align=ft.TextAlign.CENTER,  # 设置居中
                        size=20,
                        style=ft.TextStyle(
                            height=1.0,  # 关键：行高倍数
                        ),
                    ),
                    bgcolor=ft.Colors.GREY_300,
                    width=self.button_width,
                    height=45,
                    disabled=True
                )
            button_list.append(button)

        row_buttons = [button_list[i:i+self.columns] for i in range(0, len(button_list), self.columns)]
        rows = [ft.Row(controls=row_button, alignment=ft.MainAxisAlignment.END) for row_button in row_buttons]
        self.content = ft.Column(controls=rows)

        self.update()

    def _decorate_button(self, button: ft.Button, selected: bool):
        if selected:
            button.bgcolor = ft.Colors.RED
        else:
            button.bgcolor = ft.Colors.WHITE
    
    def _button_clicked(self, e):

        selected = e.control.bgcolor == ft.Colors.RED
        self._decorate_button(e.control, not selected)
        e.control.update()

        if self.on_word_clicked:
            self.on_word_clicked(e.control.key, not selected)

@ft.control
class FutureWordApp(ft.Container):
    def init(self):
        self.bgcolor = ft.Colors.PINK_300
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.info_label = ft.Text(value="请添加单词列表", color=ft.Colors.WHITE, size=20)
        self.word_viewmodel = WordViewModel()
        self.collection_view = WordCollectionView(columns=self.word_viewmodel.page_column)
        self.collection_view.on_word_clicked = self.word_viewmodel.on_word_clicked
        
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.info_label]),
                ft.Row(
                    controls=[
                        self.collection_view
                    ]
                ),
                ft.Row(
            controls=[
                ft.Button("上一页", on_click=self._page_clicked, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
                ft.Button("下一页", on_click=self._page_clicked, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
                ft.Button("导出", on_click=self._export_clicked, bgcolor=ft.Colors.BLUE_ACCENT, color=ft.Colors.WHITE),
                ft.Button("打开", on_click=self._handle_pick_files, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK),
                ft.Button("过滤", on_click=self._handle_filter_files, bgcolor=ft.Colors.WHITE, color=ft.Colors.BLACK)
            ]
            )
            ]
        )
    
    async def _handle_pick_files(self, e):
        picker = ft.FilePicker()
        files = await picker.pick_files(allow_multiple=False)
        if files:
            text = _readfile_as_text(files[0].path)
            self.word_viewmodel.update_wordlist_with_text(text)
            self._reload_view()

    async def _handle_filter_files(self, e):
        picker = ft.FilePicker()
        files = await picker.pick_files(allow_multiple=False)
        if files:
            filter_words = _readfile_as_list(files[0].path)
            self.word_viewmodel.filter_word_list(filter_words)
            self._reload_view()

    async def _export_clicked(self, e):
        words = self.word_viewmodel.selected_words()
        await _savelist_to_file(words)
    
    def _page_clicked(self, e):
        self.word_viewmodel.page_change(e.control.content == "下一页")
        self._reload_view()
        
    def _reload_view(self):
        current_word_list = self.word_viewmodel.get_current_word_list()
        self.collection_view.refresh(current_word_list)
        self.info_label.value = f"第 {self.word_viewmodel.current_page + 1} / {self.word_viewmodel.total_page} 页"
        self.info_label.update()

    def load_test_data(self):
        input_text = _readfile_as_text("data/3. The Menstrual Cycle.txt")
        self.word_viewmodel.update_wordlist_with_text(input_text)
        filter_list = _readfile_as_list("data/filter.txt")
        self.word_viewmodel.filter_word_list(filter_list)
        self._reload_view()

def main(page: ft.Page):

    page.title = "FutureWord"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    app = FutureWordApp()
    page.add(ft.Row(controls=[app], alignment=ft.MainAxisAlignment.CENTER))
    app.load_test_data()
    # app._reload_view()

ft.run(main)

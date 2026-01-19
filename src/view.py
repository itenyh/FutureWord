import flet as ft
from word_viewmodel import WordViewItem

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
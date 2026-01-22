import flet as ft
import util as ut
from word_viewmodel import WordViewModel, WordViewItem
from view import WordCollectionView
from data_storage import _init_path, WordSessionDao

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
            text = ut._readfile_as_text(files[0].path)
            self.word_viewmodel.update_wordlist_with_text(text)
            self._reload_view()

    async def _handle_filter_files(self, e):
        picker = ft.FilePicker()
        files = await picker.pick_files(allow_multiple=True)
        if files:
            await ut._savefiles_as_filters(files)

    async def _export_clicked(self, e):
        words = self.word_viewmodel.selected_words()
        await ut._savelist_to_file(words)
    
    def _page_clicked(self, e):
        self.word_viewmodel.page_change(e.control.content == "下一页")
        self._reload_view()
        
    def _reload_view(self):
        current_word_list = self.word_viewmodel.get_current_word_list()
        self.collection_view.refresh(current_word_list)
        self.info_label.value = f"第 {self.word_viewmodel.current_page + 1} / {self.word_viewmodel.total_page} 页"
        self.info_label.update()

    def load_test_data(self):
        input_text = ut._readfile_as_text("data/3. The Menstrual Cycle.txt")
        self.word_viewmodel.update_wordlist_with_text(input_text)
        filter_list = ut._readfile_as_list("data/filter.txt")
        self.word_viewmodel.filter_word_list(filter_list)
        self._reload_view()

async def main(page: ft.Page):

    page.title = "FutureWord"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    app = FutureWordApp()
    page.add(ft.Row(controls=[app], alignment=ft.MainAxisAlignment.CENTER))

    await _init_path()

    # app.load_test_data()
    # app._reload_view()

ft.run(main)

from PyQt5.QtWidgets import QAction, QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, textEditor):
        super().__init__()

        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(textEditor.openFileDialog)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(textEditor.saveFile)

        file_menu = self.addMenu('File')
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)

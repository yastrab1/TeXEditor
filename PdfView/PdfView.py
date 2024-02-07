from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout


class PdfView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.engine = QWebEngineView()

        self.layout.addWidget(self.engine)
        self.setLayout(self.layout)
    def openFile(self,url):
        self.engine.load(url)

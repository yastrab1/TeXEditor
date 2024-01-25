from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class PdfViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.engine = QWebEngineView(self)
        settings = self.engine.settings()
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)
        htmlContent = f'No pdf currently showing'
        self.engine.setHtml(htmlContent)

        self.layout.addWidget(self.engine)
        self.setLayout(self.layout)

    def openPdf(self, url):
        url = QUrl.fromLocalFile(url)
        self.engine.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.engine.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.engine.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.engine.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.engine.settings().SpatialNavigationEnabled
        self.engine.load(url)

from PyQt5.QtGui import QFont

family = "Roboto"

titleFont = QFont(family)
titleFont.setPointSize(25)
titleFont.setBold(True)
titleFont.setCapitalization(QFont.Capitalization.AllUppercase)

classicFont = QFont(family)
classicFont.setPointSize(8)

importantFont = QFont(family)
importantFont.setPointSize(8)
importantFont.setBold(True)

lessImportantFont = QFont(family)
lessImportantFont.setPixelSize(12)
lessImportantFont.setItalic(True)

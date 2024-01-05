from PyQt5.QtGui import QFont

family = "Roboto"

titleFont = QFont(family)
titleFont.setPixelSize(30)
titleFont.setBold(True)
titleFont.setCapitalization(QFont.AllUppercase)

classicFont = QFont(family)
classicFont.setPixelSize(12)

importantFont = QFont(family)
importantFont.setPixelSize(12)
importantFont.setBold(True)

import json

from PyQt5.QtGui import QTextCharFormat, QFont, QColor

from Config.Config import Config
from Defaults import FontDefaults


class ColorMapInterpreter:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(ColorMapInterpreter, cls).__new__(cls)
            cls.instance.colorMap = {}
            cls.instance.load()
        return cls.instance

    def load(self):
        path = Config().get("ColorMapPath")
        with open(path, "r", encoding="utf-8") as f:
            self.colorMap = json.loads(f.read())

    def interpret(self, colorKey):
        format = QTextCharFormat()
        font = QFont(self.getFontAttributeOrDefault("family", self.colorMap[colorKey]))
        weight = self.getFontAttributeOrDefault("weight", self.colorMap[colorKey])
        font.setWeight(self.cssWFontWeightToQt(weight))
        font.setPixelSize(self.getFontAttributeOrDefault("pixelSize", self.colorMap[colorKey]))
        format.setFont(font)
        fg = self.getFromDict(self.colorMap[colorKey], "foreground")
        if fg:
            format.setForeground(QColor(fg))
        bg = self.getFromDict(self.colorMap[colorKey], "background")
        if bg:
            format.setBackground(QColor(bg))
        return format

    def getFontAttributeOrDefault(self, attribute, properties):
        if attribute in properties:
            return properties[attribute]
        default = getattr(FontDefaults.classicFont, attribute)()
        if not default:
            raise Exception("Invalid font attribute")
        return default

    def getFromDict(self, dict, value):
        return dict[value] if value in dict else None

    def cssWFontWeightToQt(self, weight):
        css_weight_to_qfont = {
            100: QFont.Thin,
            200: QFont.ExtraLight,
            300: QFont.Light,
            400: QFont.Normal,
            500: QFont.Medium,
            600: QFont.DemiBold,
            700: QFont.Bold,
            800: QFont.ExtraBold,
            900: QFont.Black,
        }
        return css_weight_to_qfont[weight]

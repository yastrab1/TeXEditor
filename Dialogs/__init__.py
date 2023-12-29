from Config.Config import Config
from Dialogs.TemplatePropertyDialog import TemplatePropertyDialog

for prop in Config().get("FileTemplateProperties"):
    Config().registerDialog(TemplatePropertyDialog,[prop],[prop])
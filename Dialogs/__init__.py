from Config.Config import Config
from Dialogs.TemplatePropertyDialog import TemplatePropertyDialog
from Dialogs.UsernamePasswordAskDialog import UsernamePasswordDialog

for prop in Config().get("FileTemplateProperties"):
    Config().registerDialog(TemplatePropertyDialog,[prop],[prop])
for domain in Config().get("SupportedDomains"):
    Config().registerDialog(UsernamePasswordDialog, [f"{domain}Username", f"{domain}Password"], [domain])

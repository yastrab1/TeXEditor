from Config.Config import Config
from Dialogs.SeminarAskingDialogs import SelectSeminarExcercises, SelectSeminars
from Dialogs.TemplatePropertyDialog import TemplatePropertyDialog
from Dialogs.UsernamePasswordAskDialog import UsernamePasswordDialog

for prop in Config().get("FileTemplateProperties"):
    Config().registerDialog(TemplatePropertyDialog,[prop],[prop])
for domain in Config().get("SupportedDomains"):
    Config().registerDialog(UsernamePasswordDialog, [f"{domain}Username", f"{domain}Password"], [domain])
for seminarName in Config().get("SupportedSeminars"):
    Config().registerDialog(SelectSeminarExcercises, [f"Current{seminarName}Exercises"], [seminarName])
Config().registerDialog(SelectSeminars, ["CurrentSeminars"])

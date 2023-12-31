from PyQt5.QtWidgets import QLineEdit, QLabel, QHBoxLayout

from Config.Config import Config
from Dialogs.ConfigAskDialog import ConfigAskDialog


class UsernamePasswordDialog(ConfigAskDialog):
    def __init__(self, domainName):
        self.domainName = domainName
        ConfigAskDialog.__init__(self)

        self.setWindowTitle("Please enter Username and Passwords for domain " + domainName)

        self.intro = QLabel("We do not know your username and password for " + domainName)
        self.layout.addWidget(self.intro)

        self.usernameLayout = QHBoxLayout()
        self.usernameLabel = QLabel("Username:")
        self.usernameInput = QLineEdit(self)
        self.usernameLayout.addWidget(self.usernameLabel)
        self.usernameLayout.addWidget(self.usernameInput)

        self.passwordLayout = QHBoxLayout()
        self.passwordLabel = QLabel("Password:")
        self.passwordInput = QLineEdit(self)
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.passwordInput)

        self.layout.addLayout(self.usernameLayout)
        self.layout.addLayout(self.passwordLayout)

        self.chillOut = QLabel(
            "We will never use your password in other places than where it should. This editor is open-source, you can check")
        self.layout.addWidget(self.chillOut)
        self.layout.addWidget(self.okButton)

    def collectData(self) -> {}:
        result = {}
        result[f"{self.domainName}Username"] = self.usernameInput.text()
        result[f"{self.domainName}Password"] = self.passwordInput.text()
        return result


Config().registerDialog(UsernamePasswordDialog, [])

from PyQt5.QtWidgets import QMessageBox

class MessageBox:
    def __init__(self, title="AutoRaman", text="", icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(buttons)
        msg_box.exec_()

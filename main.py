import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Editor v0.0")
        self.resize(850, 700)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QtGui.QIcon("ediv1.png"))

        # StyleSheet
        self.setStyleSheet("background-color: 'cyan';")

        # Create a 'GridLayout'
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)  # Set the layout

        # The menu bar
        menubar = QtWidgets.QMenuBar()
        menubar.setNativeMenuBar(False)
        self.layout.addWidget(menubar, 0, 0)
        menubar.setStyleSheet(
            "background-color: rgb(170, 170, 170);font-size: 14px; margin: 0px; padding: 0px;"
        )

        # Add a menu 'File' into the menubar
        menufile = menubar.addMenu("File")
        action_new_file = QtWidgets.QAction("New file", self)  # New action menu
        action_new_file.setToolTip("Create new file")
        action_new_file.setShortcut("Ctrl+N")  # Shortcut to New file
        menufile.addAction(action_new_file)  # Add the action to menu 'File'
        menufile.addSeparator()  # Separator line

        action_open_file = QtWidgets.QAction("Open file", self)
        action_open_file.setToolTip("Open a file")
        action_open_file.setShortcut("Ctrl+O")
        menufile.addAction(action_open_file)
        menufile.addSeparator()

        action_save_file = QtWidgets.QAction("Save as", self)
        action_save_file.setToolTip("Save the file")
        action_save_file.setShortcut("Ctrl+S")
        menufile.addAction(action_save_file)
        menufile.addSeparator()

        action_exit = QtWidgets.QAction("Exit", self)
        action_exit.setToolTip("Exit the app")
        menufile.addAction(action_exit)
        menufile.addSeparator()

        # Add a menu 'Edit' into the menubar
        menuedit = menubar.addMenu("Edit")
        action_copy = QtWidgets.QAction("Copy", self)
        action_copy.setShortcut("Ctrl+C")
        menuedit.addAction(action_copy)
        menuedit.addSeparator()

        action_paste = QtWidgets.QAction("Paste", self)
        action_paste.setShortcut("Ctrl+V")
        menuedit.addAction(action_paste)
        menuedit.addSeparator()

        action_cut = QtWidgets.QAction("Cut", self)
        action_cut.setShortcut("Ctrl+X")
        menuedit.addAction(action_cut)
        menuedit.addSeparator()

        action_zoomout = QtWidgets.QAction("Zoom-", self)
        action_zoomout.setShortcut("Ctrl+-")
        menuedit.addAction(action_zoomout)
        menuedit.addSeparator()

        action_zoomin = QtWidgets.QAction("Zoom+", self)
        action_zoomin.setShortcut("Ctrl++")
        menuedit.addAction(action_zoomin)

        # Add a menu 'Help' into menubar
        menuhelp = menubar.addMenu("Help")
        action_about = QtWidgets.QAction("About us", self)
        menuhelp.addAction(action_about)
        menuhelp.addSeparator()
        action_readme = QtWidgets.QAction("Read me", self)
        menuhelp.addAction(action_readme)

        # Create plain text edit
        self.plaintext = QtWidgets.QPlainTextEdit()

        # self.layout.addWidget(self.plaintext, 1, 0)   Add the plaintext widget into the 'GridLayout'
        self.plaintext.setCursorWidth(2)  # Set the cursor width

        # Style the plaintext widget
        self.plaintext.setStyleSheet(
            f"background-color: rgb(78, 78, 78); color: 'white'; margin: 0px; padding: 0px;"
            "font-family: 'Cascadia Mono';"
        )

        # TabWidget configuration
        self.tabwidget = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabwidget, 1, 0)
        self.tabwidget.addTab(self.plaintext, "Document")
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.setMovable(True)

        # Create a 'FileDialog'
        self.filedialog = QtWidgets.QFileDialog()

        # Create a status bar
        self.status = QtWidgets.QStatusBar()
        self.layout.addWidget(self.status, 2, 0)
        self.checkedbox = QtWidgets.QCheckBox("Read-only")
        self.checkedbox.setChecked(False)
        self.status.addPermanentWidget(self.checkedbox, 1)
        self.checkedbox.toggled.connect(self.checkedbox_method)

        # Label to display the file lenght into the status bar
        self.text_lab = '0'
        self.lenght = QtWidgets.QLabel()
        self.lenght.setAlignment(QtCore.Qt.AlignRight)

        # Create a timer to call the method counter file lenght each 100 ms times
        self.timeur = QtCore.QTimer()
        self.timeur.timeout.connect(self.timeit)  # Connect the timer to the method
        self.timeur.start(100)  # Start the timer by give it the interval of time

        self.status.insertPermanentWidget(2, self.lenght, 0)

        # Connexion between methods and widgets
        action_new_file.triggered.connect(self.new_file_method)
        action_open_file.triggered.connect(self.open_file_method)
        action_save_file.triggered.connect(self.save_file_method)
        action_exit.triggered.connect(self.exit_method)
        action_copy.triggered.connect(self.copy_method)
        action_paste.triggered.connect(self.paste_method)
        action_zoomin.triggered.connect(self.zoomin_method)
        action_zoomout.triggered.connect(self.zoomout_method)
        action_about.triggered.connect(self.about_method)
        action_cut.triggered.connect(self.cut_method)
        action_readme.triggered.connect(self.readme_method)
        self.tabwidget.tabCloseRequested.connect(self.closetab)

    # Methods defined
    def closetab(self):
        self.tabwidget.removeTab(self.tabwidget.currentIndex())

    def new_file_method(self):
        self.plaintext.clear()
        if self.tabwidget.isTabEnabled(0):
            pass
        else:
            self.tabwidget.insertTab(0, self.plaintext, "New document")

    def open_file_method(self):
        self.filedialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

        try:
            # In open() i remove encoding specification to fix reding other king of file than '.txt'
            with open(str(self.filedialog.getOpenFileName(self, 'Open file')[0]), mode='r', encoding='utf-8')\
                    as the_file:
                self.plaintext.clear()
                self.plaintext.insertPlainText(f"{str(the_file.read())}")
        except FileNotFoundError:
            pass

    def save_file_method(self):
        self.filedialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        # self.filedialog.open()
        # print(QtWidgets.QFileDialog.getSaveFileName())
        try:
            with open(str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')[0]), mode='w', encoding='utf-8')\
                    as file:
                file.write(str(self.plaintext.toPlainText()))
                self.status.showMessage("File saved", 4000)
        except FileNotFoundError:
            pass

        """self.filedialog.saveFileContent(bytes(self.plaintext.toPlainText(), encoding='utf-8'))
        print(QtWidgets.QFileDialog)"""

    @staticmethod
    def exit_method():
        QtWidgets.qApp.exit()

    def copy_method(self):
        self.plaintext.copy()

    def paste_method(self):
        self.plaintext.paste()

    def cut_method(self):
        self.plaintext.cut()

    def zoomin_method(self):
        self.plaintext.zoomIn(4)

    def zoomout_method(self):
        self.plaintext.zoomOut(4)

    @staticmethod
    def about_method():
        popup = QtWidgets.QMessageBox()
        popup.setInformativeText(
            f"Simple Editor App\n\nAuthor: Cherif Abdourahmane Ba\nEmail: baabdourahmane210@gmail.com\t\n\n"
        )
        popup.setWindowTitle("About us")
        popup.setIcon(QtWidgets.QMessageBox.NoIcon)
        popup.setStandardButtons(QtWidgets.QMessageBox.Close)
        popup.exec_()

    def timeit(self):
        self.text_lab = str(len(self.plaintext.toPlainText()))
        self.lenght.setText(str('Size: ') + str(self.text_lab) + str(' B'))
        # print(len(self.plaintext.toPlainText()))
        # print("Ok it works")

    def readme_method(self):
        try:
            with open("README.md", mode='r', encoding="utf-8") as file:
                content = file.read()
            self.plaintext.clear()
            self.plaintext.insertPlainText(format(content))
            self.plaintext.setReadOnly(True)
        except FileNotFoundError:
            pass

    def checkedbox_method(self):
        if self.checkedbox.isChecked():
            self.plaintext.setReadOnly(True)
        if self.checkedbox.isChecked() is False:
            self.plaintext.setReadOnly(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys
import validators
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtPrintSupport
import json


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setStyleSheet(
            "background-color:#0088ff;color : #ffffff;")
        layout = QVBoxLayout()

        title = QLabel("WEB Plus Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)
        self.setStyleSheet("background-color:#000000;color : #ffffff;")

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('images', 'ma-icon-128.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Mark 4"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        self.setWindowTitle("Web Plus")
        self.setLayout(layout)


class Help(QDialog):
    def __init__(self, *args, **kwargs):
        super(Help, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        title = QLabel("KeyBoard Shortcuts")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        layout.addWidget(QLabel(" Open New Tab--Ctrl+Alt+t \n Open a HTML file--Ctrl+o \n Print the web page--Ctrl+p \n Get information about the version of web plus you are using--Ctrl+Alt+a \n Visit Web Plus's official website--Ctrl+Alt+h \n View Page Source Code--Ctrl+Alt+v \n Back to previous page--Ctrl+b \n Forward to next page--Ctrl+f \n Reload page--Ctrl+Alt+r \n Open the home page--Ctrl+h"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        self.setWindowTitle("Keyboard Shortcuts")
        self.setLayout(layout)



class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        self.featurePermissionRequested.connect(
            self.handleFeaturePermissionRequested)

    @QtCore.pyqtSlot(QtCore.QUrl, QtWebEngineWidgets.QWebEnginePage.Feature)
    def handleFeaturePermissionRequested(self, securityOrigin, feature):
        title = "Permission Request"
        questionForFeature = {
            QtWebEngineWidgets.QWebEnginePage.Geolocation: "Allow {feature} to access your location information?",
            QtWebEngineWidgets.QWebEnginePage.MediaAudioCapture: "Allow {feature} to access your microphone?",
            QtWebEngineWidgets.QWebEnginePage.MediaVideoCapture: "Allow {feature} to access your webcam?",
            QtWebEngineWidgets.QWebEnginePage.MediaAudioVideoCapture: "Allow {feature} to lock your mouse cursor?",
            QtWebEngineWidgets.QWebEnginePage.DesktopVideoCapture: "Allow {feature} to capture video of your desktop?",
            QtWebEngineWidgets.QWebEnginePage.DesktopAudioVideoCapture: "Allow {feature} to capture audio and video of your desktop?"
        }
        question = questionForFeature.get(feature)
        if question:
            question = question.format(feature=securityOrigin.host())
            if QtWidgets.QMessageBox.question(self.view().window(), title, question) == QtWidgets.QMessageBox.Yes:
                self.setFeaturePermission(
                    securityOrigin, feature, QtWebEngineWidgets.QWebEnginePage.PermissionGrantedByUser)
            else:
                self.setFeaturePermission(
                    securityOrigin, feature, QtWebEngineWidgets.QWebEnginePage.PermissionDeniedByUser)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        # defining shotcuts

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+t'), self)
        self.shortcut_open.activated.connect(self.add_new_tab)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+p'), self)
        self.shortcut_open.activated.connect(self.printRequested)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+o'), self)
        self.shortcut_open.activated.connect(self.open_file)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+a'), self)
        self.shortcut_open.activated.connect(self.about)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+h'), self)
        self.shortcut_open.activated.connect(self.navigate_mozarella)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+v'), self)
        self.shortcut_open.activated.connect(self.view)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+b'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().back())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+f'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().forward())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+r'), self)
        self.shortcut_open.activated.connect(
            lambda: self.tabs.currentWidget().reload())

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+h'), self)
        self.shortcut_open.activated.connect(self.navigate_home)

        
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)


        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.nav = QToolBar("Navigation")
        self.nav.setOrientation(QtCore.Qt.Vertical)
        self.nav.setIconSize(QSize(26, 26))
        self.nav.setMovable(False)
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.nav)

        add = QAction(
            QIcon(os.path.join('images', 'plus.png')), "Add new tab", self)
        add.setStatusTip("Add new tab")
        add.triggered.connect(lambda _: self.add_new_tab())
        self.nav.addAction(add)

        self.navtb = QToolBar("Navigation")
        self.navtb.setIconSize(QSize(25, 25))
        self.navtb.setMovable(False)
        self.addToolBar(self.navtb)

        back_btn = QAction(
            QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navtb.addAction(back_btn)

        next_btn = QAction(
            QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navtb.addAction(next_btn)
        
        '''
        home_btn = QAction(
            QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Open the home page")
        home_btn.triggered.connect(self.navigate_home)
        self.navtb.addAction(home_btn)
        '''

        reload_btn = QAction(
            QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())
        self.navtb.addAction(reload_btn)


        self.connect_btn = QAction(QIcon(os.path.join('images', 'lock-nossl.png')), "Connection Status", self)
        self.navtb.addAction(self.connect_btn)

        self.urlbar = QLineEdit()
        # self.urlbar.setStyleSheet("background-color : none; border-radius : None")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        #self.urlbar.setFixedWidth(1640)
        self.urlbar.setFixedHeight(28)
        self.navtb.addWidget(self.urlbar)

        stop_btn = QAction(
            QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(stop_btn)
        '''
        connect_btn = QAction(
            QIcon(os.path.join('images', 'lock-ssl.png')), "Connection Status", self)
        # connect_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(connect_btn)

        extension_btn = QAction(
            QIcon(os.path.join('images', 'extension.png')), "Extension", self)
        # extension_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(extension_btn)
        
        option_btn = QAction(
            QIcon(os.path.join('images', 'options.png')), "Option", self)
        # option_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.navtb.addAction(option_btn)'''

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        self.file_menu = self.menuBar().addMenu("&File")
        new_tab_action = QAction(
            QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        self.file_menu.addAction(new_tab_action)

        print_action = QAction(
            QIcon(os.path.join('images', 'printer.png')), "Print", self)
        print_action.setStatusTip("Print the webpage")
        print_action.triggered.connect(self.printRequested)
        self.file_menu.addAction(print_action)

        open_file_action = QAction(
            QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_file_action)

        self.help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(os.path.join('images', 'question.png')), "About Web Plus", self)
        about_action.setStatusTip("Find out more about Web Plus")
        about_action.triggered.connect(self.about)
        self.help_menu.addAction(about_action)

        keyboard = QAction(
            QIcon(os.path.join('images', 'keyboard.png')), "Keyboard Shotcut", self)
        keyboard.setStatusTip(
            "Find out more about Web Plus's Keyboard Shotcuts")
        keyboard.triggered.connect(self.keyboardshotcut)
        self.help_menu.addAction(keyboard)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Web Plus Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to Web Plus Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        self.help_menu.addAction(navigate_mozarella_action)

        self.tool_menu = self.menuBar().addMenu("&Tools")
        view = QAction(QIcon(os.path.join('images', 'view.png')),
                       "View page source code", self)
        view.setStatusTip("View page source code")
        view.triggered.connect(self.view)
        self.tool_menu.addAction(view)

        self.settings_menu = self.menuBar().addMenu("&Settings")
        dark_theme_action = QAction(QIcon(os.path.join('images', 'icon.png')),
                       "Dark theme", self)
        dark_theme_action.setStatusTip("Enable/Disable dark mode")
        dark_theme_action.triggered.connect(self.darkTheme)
        self.settings_menu.addAction(dark_theme_action)

        

        self.add_new_tab(QUrl('file:///html/home.html'), 'UNTITLED')

        self.show()


        self.setWindowTitle("Web Plus")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        self.switch()
        self.darkTheme()
    
    

    def switch(self):
        with open("config.json", 'r') as f:
            data = json.load(f)
        self.res=data["theme"]

        if self.res == 'light': 
            with open('config.json', 'r+') as f:
                data = json.load(f)
                data['theme'] = "dark" 
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            with open('config.json', 'r+') as f:
                data = json.load(f)
                data['theme'] = "light" 
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()

    def add_new_tab(self, qurl=None, label="UNTITLED"):

        if qurl is None:
            qurl = QUrl('file:///html/home.html')

        browser = QWebEngineView()
        page = WebEnginePage(browser)
        browser.setPage(page)
        browser.setUrl(qurl)
        page.printRequested.connect(self.printRequested)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile(
        ).downloadRequested.connect(self.on_downloadRequested)

        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        self.tabs.setTabIcon(i, browser.page().icon())

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

        browser.iconChanged.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabIcon(i, browser.icon()))



    def printRequested(self):
        # if you are viewing this part of my code can you please improve this as I don't think this is the best way to print a page and I can't understand how to fix this
        url = self.urlbar.text()
        if url == "":
            url = 'file:///html/home.html'
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.page = QtWebEngineWidgets.QWebEnginePage(self)
        self.view.setPage(self.page)
        self.view.load(QtCore.QUrl(url))
        defaultPrinter = QtPrintSupport.QPrinter(
            QtPrintSupport.QPrinterInfo.defaultPrinter())
        dialog = QtPrintSupport.QPrintDialog(defaultPrinter, self)
        if dialog.exec():
            # printer object has to be persistent
            self._printer = dialog.printer()
            self.page.print(self._printer, self.printResult)

    def printResult(self, success):
        if success:
            pass
        else:
            QtWidgets.QMessageBox.information(self, 'Print failed',
                                              'Printing has failed!', QtWidgets.QMessageBox.Ok)
        del self._printer

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():

            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Web Plus" % title)

    def navigate_mozarella(self):
        self.tabs.currentWidget().setUrl(
            QUrl("https://saptakbhoumik.github.io/web.github.io/"))

    def view(self):
        url = self.urlbar.text()
        if url == "":
            url = "file:///html/home.html"
        url = f"view-source:{url}"
        self.add_new_tab(QUrl(url), 'UNTITLED')

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def keyboardshotcut(self):
        dlg = Help()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "HTML(*.htm *.html);;")
        if filename == "":
            pass
        else:
            self.tabs.currentWidget().setUrl(QUrl(f"file:///{filename}"))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("file:///html/home.html"))

    def navigate_to_url(self):
        inputtext = self.urlbar.text()
        if validators.url(inputtext):
            q = QUrl(inputtext)
        elif validators.url(f"https://{inputtext}"):
            q = QUrl(f"http://{inputtext}")
        elif inputtext.find("file:///") == 0 or inputtext.find("view-source:") == 0 :
            q = QUrl(inputtext)

        else:
            url = f'https://www.ecosia.org/search?q={inputtext.replace("+","%2B").replace(" ","+")}'
            q = QUrl(url)

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)
        

    def update_urlbar(self, q, browser=None):
        url = q.toString()
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'ssl.png')))
            self.connect_btn.setStatusTip("Your connection is secure")

        elif q.scheme() == 'http':
            # Insecure padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'lock-nossl.png')))
            self.connect_btn.setStatusTip("Your connection is not secure")

        elif q.scheme() == 'file':
            if url == "file:///html/home.html":
                # search padlock icon
                self.connect_btn.setIcon(QIcon(os.path.join('images', 'search.png')))
                self.connect_btn.setStatusTip("Search or type a url")
            else:
                # file padlock icon
                self.connect_btn.setIcon(QIcon(os.path.join('images', 'document.png')))
                self.connect_btn.setStatusTip(
                    "You are viewing a local or shared file")

        elif q.scheme() == 'view-source':
            # source code padlock icon
            self.connect_btn.setIcon(QIcon(os.path.join('images', 'code.png')))
            self.connect_btn.setStatusTip(
                f"You are viewing the source of a website")

        if url == "file:///html/home.html":
            self.urlbar.setText("")
        else:
            self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        

    def darkTheme(self):
        with open("config.json", 'r') as f:
	        data = json.load(f)
        self.res=data["theme"]

        if self.res == 'dark':
            self.status = 'dark'
        else:
            self.status = 'light'

        if self.status == 'light':

            self.tabs.setStyleSheet("""
                                    QTabWidget {
                                        background: #ffffff; 
                                    }
                                    QTabBar {
                                        background: #e7eaed; 
                                    }
                                    QTabBar::tab {
                                        background: #e7eaed; 
                                        padding: 10px;
                                        color: #000000;
                                        margin-top: -1px;
                                        margin-bottom: -1px; 
                                        margin-left: 1pt solid black;
                                        margin-right: 1pt solid black;
                                        border: 1px solid #000000;
                                        border-radius: 4px;
                                    } 
                                    QTabBar::tab:hover { 
                                        background: #f0f0f0;  
                                    } 
                                    QTabBar::tab:selected { 
                                        background: #ffffff;  
                                        color: #000000;
                                    }
                                    """)
            self.navtb.setStyleSheet("""
                                QToolBar {
                                    background-color: #ffffff; 
                                    color:#000000;
                                }
                                QToolBar QToolButton {
                                    background-color: #ffffff;
                                    border-radius: 2px;
                                }
                                QToolBar QToolButton:pressed {
                                    background-color: #ffffff;
                                    border-radius: 2px;
                                }
                                
                                """)


            self.nav.setStyleSheet("""
                                QToolBar {
                                    background-color : #ffffff; 
                                    margin-bottom: -1px;
                                    color:#000000;
                                }
                                QToolBar QToolButton {
                                    background-color: #ffffff;
                                    border-radius: 2px;
                                }
                                QToolBar QToolButton:pressed {
                                    background-color: #ffffff;
                                    border-radius: 2px;
                                }
                                
                                """)


            self.statusBar().setStyleSheet("background-color : #ffffff ; color : #000000")


            self.urlbar.setStyleSheet(
               "font-size: 11pt;border: 1px solid #0088ff;border-radius: 10px;background-color:#ffffff;color:#000000")
            self.file_menu.setStyleSheet(
                "color:#000000;background-color:#ffffff;")
            self.help_menu.setStyleSheet(
                "color:#000000;background-color:#ffffff;")
            self.tool_menu.setStyleSheet(
                "color:#000000;background-color:#ffffff;")

            self.menuBar().setStyleSheet(
                'color:#000000;background-color:#ffffff;border: 1px solid white')


            with open('config.json', 'r+') as f:
                data = json.load(f)
                data['theme'] = "dark" 
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

        else:
            self.tabs.setStyleSheet("""
                                    QTabWidget {
                                        background: #000000; 
                                    }
                                    QTabBar {
                                        background: #000000; 
                                    }
                                    QTabBar::tab {
                                        background: #000000; 
                                        padding: 10px;
                                        color: #ffffff;
                                        margin-top: -1px;
                                        margin-bottom: -1px;
                                        margin-left: 1pt solid black;
                                        margin-right: 1pt solid black;
                                        border: 1px solid #ffffff;
                                        border-radius: 4px;
                                    } 
                                    QTabBar::tab:hover { 
                                        background: #414141;  
                                    }
                                    
                                    QTabBar::tab:selected { 
                                        background: #979797;  
                                    }
                                    """)
            self.navtb.setStyleSheet("""
                                QToolBar {
                                    background-color: #000000; 
                                    color:#ffffff;
                                }
                                QToolBar QToolButton {
                                    background-color: #000000;
                                    border-radius: 2px;
                                }
                                QToolBar QToolButton:pressed {
                                    background-color: #000000;
                                    border-radius: 2px;
                                }
                                
                                """)
            
            self.nav.setStyleSheet("""
                                    QToolBar {
                                        background-color : #ffffff; 
                                        margin-bottom: -1px;
                                        color:#000000;
                                    }
                                    QToolBar QToolButton {
                                        background-color: #ffffff;
                                        border-radius: 2px;
                                    }
                                    QToolBar QToolButton:pressed {
                                        background-color: #ffffff;
                                        border-radius: 2px;
                                    }
                                    
                                    """)

            self.statusBar().setStyleSheet("background-color : #000000 ; color : #ffffff")

            self.urlbar.setStyleSheet(
                 "font-size: 11pt;border: 1px solid #ffffff;border-radius: 10px;background-color:#333435;color:#ffffff")
            self.file_menu.setStyleSheet(
                "color:#ffffff;background-color:#000000; ")
            self.help_menu.setStyleSheet(
                "color:#ffffff;background-color:#000000;")
            self.tool_menu.setStyleSheet(
                "color:#ffffff;background-color:#000000;")
            self.menuBar().setStyleSheet(
                'color:#ffffff;background-color:#000000;border: 1px solid black')
            
            with open('config.json', 'r+') as f:
                data = json.load(f)
                data['theme'] = "light" 
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Web Plus")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

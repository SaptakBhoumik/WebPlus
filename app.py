from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import os
import sys
import validators
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok 
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setStyleSheet("background-color:#0088ff;color : #ffffff;")
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

        layout.addWidget(QLabel("Mark 2"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        self.setWindowTitle("Web Plus")
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #defining shotcuts

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+t'), self)
        self.shortcut_open.activated.connect(self.add_new_tab)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+o'), self)
        self.shortcut_open.activated.connect(self.open_file)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+a'), self)
        self.shortcut_open.activated.connect(self.about)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+h'), self)
        self.shortcut_open.activated.connect(self.navigate_mozarella)

        self.shortcut_open = QShortcut(QKeySequence('Ctrl+Alt+v'), self)
        self.shortcut_open.activated.connect(self.view)


        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setStyleSheet("color:#000000;background-color : #ffffff;") 
        
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        navtb.setStyleSheet("background-color:#ffffff;") 
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel() 
        self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.urlbar.setStyleSheet("font-size: 11pt;border: 1px solid #0088ff;")
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.setStyleSheet("color:#000000;background-color : #ffffff;")
        new_tab_action = QAction(QIcon(os.path.join('images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('images', 'disk--arrow.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.setStyleSheet("color:#000000;background-color : #ffffff;")
        about_action = QAction(QIcon(os.path.join('images', 'question.png')), "About Web Plus", self)
        about_action.setStatusTip("Find out more about Web Plus")  
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(QIcon(os.path.join('images', 'lifebuoy.png')),
                                            "Web Plus Homepage", self)
        navigate_mozarella_action.setStatusTip("Go to Web Plus Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)


        tool_menu = self.menuBar().addMenu("&Tool")
        tool_menu.setStyleSheet("color:#000000;background-color : #ffffff;")
        view = QAction(QIcon(os.path.join('images', 'view.png')), "View page source code", self)
        view.setStatusTip("View page source code")
        view.triggered.connect(self.view)
        tool_menu.addAction(view)


        self.add_new_tab(QUrl('http://www.ecosia.org'), 'Homepage')
        
        self.show()

        self.setWindowTitle("Web Plus")
        self.setWindowIcon(QIcon(os.path.join('images', 'ma-icon-64.png')))
        
    
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
    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl('http://www.ecosia.org')
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(
            self.on_downloadRequested
        )
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
    
    

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
        self.tabs.currentWidget().setUrl(QUrl("https://saptakbhoumik.github.io/web.github.io/"))

    def view(self):
        url =self.urlbar.text()
        url=f"view-source:{url}"
        self.tabs.currentWidget().setUrl(QUrl(url))
        

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "","HTML(*.htm *.html);;")
        if filename=="":
            pass
        else:
            self.tabs.currentWidget().setUrl(QUrl(f"file:///{filename}"))
       

   


    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.ecosia.org"))

    def navigate_to_url(self):
        inputtext=self.urlbar.text()
        if validators.url(inputtext):
            q = QUrl(self.urlbar.text())
        elif inputtext.find("file:///")==0:
            q = QUrl(inputtext)  

        else:
            url=f'https://www.ecosia.org/search?q={inputtext.replace("+","%2B").replace(" ","+")}'
            q = QUrl(url)
        
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Web Plus")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
    

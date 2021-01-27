# -*- coding: utf-8 -*-
"""
frontend of pybox
---------
@author: maikherbig
"""
#Continue starting the app
from PyQt5 import QtCore, QtGui, QtWidgets
import traceback,io,os,psutil,time,sys
import all_imports
import backend #Optionally: outsource some of the functions to backend to keep frontend clean
dir_root = os.path.dirname(all_imports.__file__)#ask the module for its origin

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class WorkerSignals(QtCore.QObject):
    '''
    Code inspired from here: https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
    
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `int` indicating % progress
    history
        `dict` containing keras model history.history resulting from .fit
    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)
    history = QtCore.pyqtSignal(dict)

class Worker(QtCore.QRunnable):
    '''
    Code inspired/copied from: https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['history_callback'] = self.signals.history

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 650)
        
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_python_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_python_1.setObjectName("verticalLayout_python_1")
        self.groupBox_pythonMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_pythonMenu.setMaximumSize(QtCore.QSize(16777215, 71))
        self.groupBox_pythonMenu.setObjectName("groupBox_pythonMenu")
        self.gridLayout_40 = QtWidgets.QGridLayout(self.groupBox_pythonMenu)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.horizontalLayout_pythonMenu = QtWidgets.QHBoxLayout()
        self.horizontalLayout_pythonMenu.setObjectName("horizontalLayout_pythonMenu")
        self.label_pythonCurrentFile = QtWidgets.QLabel(self.groupBox_pythonMenu)
        self.label_pythonCurrentFile.setObjectName("label_pythonCurrentFile")
        self.horizontalLayout_pythonMenu.addWidget(self.label_pythonCurrentFile)
        self.lineEdit_pythonCurrentFile = QtWidgets.QLineEdit(self.groupBox_pythonMenu)
        self.lineEdit_pythonCurrentFile.setEnabled(False)
        self.lineEdit_pythonCurrentFile.setObjectName("lineEdit_pythonCurrentFile")
        self.horizontalLayout_pythonMenu.addWidget(self.lineEdit_pythonCurrentFile)
        self.gridLayout_40.addLayout(self.horizontalLayout_pythonMenu, 0, 0, 1, 1)
        self.verticalLayout_python_1.addWidget(self.groupBox_pythonMenu)
        self.splitter_python_1 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_python_1.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_python_1.setObjectName("splitter_python_1")
        self.groupBox_pythonEditor = QtWidgets.QGroupBox(self.splitter_python_1)
        self.groupBox_pythonEditor.setObjectName("groupBox_pythonEditor")
        self.gridLayout_38 = QtWidgets.QGridLayout(self.groupBox_pythonEditor)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.verticalLayout_editor_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_editor_1.setObjectName("verticalLayout_editor_1")
        self.horizontalLayout_editor_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_editor_1.setObjectName("horizontalLayout_editor_1")
        self.pushButton_pythonInOpen = QtWidgets.QPushButton(self.groupBox_pythonEditor)
        self.pushButton_pythonInOpen.setObjectName("pushButton_pythonInOpen")
        self.horizontalLayout_editor_1.addWidget(self.pushButton_pythonInOpen)
        self.pushButton_pythonSaveAs = QtWidgets.QPushButton(self.groupBox_pythonEditor)
        self.pushButton_pythonSaveAs.setObjectName("pushButton_pythonSaveAs")
        self.horizontalLayout_editor_1.addWidget(self.pushButton_pythonSaveAs)
        self.pushButton_pythonInClear = QtWidgets.QPushButton(self.groupBox_pythonEditor)
        self.pushButton_pythonInClear.setObjectName("pushButton_pythonInClear")
        self.horizontalLayout_editor_1.addWidget(self.pushButton_pythonInClear)
        self.pushButton_pythonInRun = QtWidgets.QPushButton(self.groupBox_pythonEditor)
        self.pushButton_pythonInRun.setObjectName("pushButton_pythonInRun")
        self.horizontalLayout_editor_1.addWidget(self.pushButton_pythonInRun)
        self.verticalLayout_editor_1.addLayout(self.horizontalLayout_editor_1)
        self.plainTextEdit_pythonIn = QtWidgets.QPlainTextEdit(self.groupBox_pythonEditor)
        self.plainTextEdit_pythonIn.setObjectName("plainTextEdit_pythonIn")
        self.verticalLayout_editor_1.addWidget(self.plainTextEdit_pythonIn)
        self.gridLayout_38.addLayout(self.verticalLayout_editor_1, 0, 0, 1, 1)
        self.groupBox_pythonConsole = QtWidgets.QGroupBox(self.splitter_python_1)
        self.groupBox_pythonConsole.setObjectName("groupBox_pythonConsole")
        self.gridLayout_39 = QtWidgets.QGridLayout(self.groupBox_pythonConsole)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.verticalLayout_console_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_console_1.setObjectName("verticalLayout_console_1")
        self.horizontalLayout_console_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_console_1.setObjectName("horizontalLayout_console_1")
        self.pushButton_pythonOutClear = QtWidgets.QPushButton(self.groupBox_pythonConsole)
        self.pushButton_pythonOutClear.setObjectName("pushButton_pythonOutClear")
        self.horizontalLayout_console_1.addWidget(self.pushButton_pythonOutClear)
        self.pushButton_pythonOutRun = QtWidgets.QPushButton(self.groupBox_pythonConsole)
        self.pushButton_pythonOutRun.setObjectName("pushButton_pythonOutRun")
        self.horizontalLayout_console_1.addWidget(self.pushButton_pythonOutRun)
        self.verticalLayout_console_1.addLayout(self.horizontalLayout_console_1)
        self.textBrowser_pythonOut = QtWidgets.QTextBrowser(self.groupBox_pythonConsole)
        self.textBrowser_pythonOut.setEnabled(True)
        self.textBrowser_pythonOut.setObjectName("textBrowser_pythonOut")
        self.verticalLayout_console_1.addWidget(self.textBrowser_pythonOut)
        self.gridLayout_39.addLayout(self.verticalLayout_console_1, 0, 0, 1, 1)
        self.verticalLayout_python_1.addWidget(self.splitter_python_1)
        self.gridLayout.addLayout(self.verticalLayout_python_1, 0, 0, 1, 1)
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar_cpuRam = QtWidgets.QLabel("CPU: xx%  RAM: xx%   ")
        self.statusbar.addPermanentWidget(self.statusbar_cpuRam)        

        


        ############################Variables##################################
        #######################################################################
        #Initilaize some variables which are lateron filled in the program
        self.threadpool = QtCore.QThreadPool()
        self.threadpool_single_queue = 0 #count nr. of threads in queue; 

        #Start running show_cpu_ram function and run it all the time
        worker_cpu_ram = Worker(self.cpu_ram_worker)
        self.threadpool.start(worker_cpu_ram)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




        ######################Connections######################################
        self.pushButton_pythonInRun.clicked.connect(self.pythonInRun)
        self.pushButton_pythonInClear.clicked.connect(self.pythonInClear)
        self.pushButton_pythonSaveAs.clicked.connect(self.pythonInSaveAs)
        self.pushButton_pythonInOpen.clicked.connect(self.pythonInOpen)
        self.pushButton_pythonOutClear.clicked.connect(self.pythonOutClear)
        self.pushButton_pythonOutRun.clicked.connect(self.pythonInRun)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyBox"))
        self.groupBox_pythonEditor.setTitle(_translate("MainWindow", "Editor"))
        self.label_pythonCurrentFile.setText(_translate("MainWindow", "Current file:"))

        self.pushButton_pythonInOpen.setText(_translate("MainWindow", "Open file.."))
        self.pushButton_pythonSaveAs.setText(_translate("MainWindow", "Save as..."))
        self.pushButton_pythonInClear.setText(_translate("MainWindow", "Clear"))
        self.pushButton_pythonInRun.setText(_translate("MainWindow", "Run"))
        self.groupBox_pythonConsole.setTitle(_translate("MainWindow", "Console"))
        self.pushButton_pythonOutClear.setText(_translate("MainWindow", "Clear"))
        self.pushButton_pythonOutRun.setText(_translate("MainWindow", "Run"))

    #####################Python Editor/Console#################################
    def pythonInRun(self):
        self.threadpool_single_queue += 1
        if self.threadpool_single_queue == 1:
            worker = Worker(self.pythonInRun_Worker)                          
            self.threadpool.start(worker)
    
    def pythonInRun_Worker(self,progress_callback,history_callback):
        code = self.plainTextEdit_pythonIn.toPlainText()
        out,error = backend.run_python(code)
        text_out = "Out:\n"+out
        text_error = "Error:\n"+error
   
        #Print both to textBrowser_pythonOut
        self.textBrowser_pythonOut.append(text_out)
        if len(error)>0: 
            self.textBrowser_pythonOut.append(text_error)
    
        self.threadpool_single_queue = 0 #reset thread counter
        
    def pythonInClear(self):
        self.plainTextEdit_pythonIn.clear()
        self.lineEdit_pythonCurrentFile.clear()
    
    def pythonInSaveAs(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save code', dir_root,"Python file (*.py)")
        filename = filename[0]
        if len(filename)==0:
            return
        #add the suffix .csv
        if not filename.endswith(".py"):
            filename = filename +".py"               
    
        code = self.plainTextEdit_pythonIn.toPlainText()
    
        myfile = open(filename,'w')#Open the file with writing permission
        myfile.write(code)        
        myfile.close()
        self.lineEdit_pythonCurrentFile.setText(filename)
    
    def pythonInOpen(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Python file', dir_root,"Python file (*.py)")
        filename = filename[0]
        if not filename.endswith(".py"):
            return
        if not os.path.isfile(filename):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)       
            msg.setText("File not found")
            msg.setWindowTitle("File not found")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return
        with open(filename, 'r') as myfile:
            data = myfile.read()
        
        self.plainTextEdit_pythonIn.clear()
        self.plainTextEdit_pythonIn.insertPlainText(data)
        self.lineEdit_pythonCurrentFile.setText(filename)
    
    def pythonOutClear(self):
        self.textBrowser_pythonOut.clear()
    
    #Show cpu and ram usage on the status bar
    def cpu_ram_worker(self,progress_callback,history_callback):
        while True:
            cpu,ram = psutil.cpu_percent(),psutil.virtual_memory().percent
            self.statusbar_cpuRam.setText("CPU: "+str(cpu)+"%  RAM: "+str(ram)+"%")            
            time.sleep(2)
    



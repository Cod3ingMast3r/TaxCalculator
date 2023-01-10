from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QApplication, QDateEdit, QMainWindow;
import sys;
import numpy as np;
import datetime as dt;
global hoursPerWeek;
global todaysDate;
global currentYear, currentMonth, currentDay;
global incomeAfterTaxOutput;
global incomeInput;

todaysDate = dt.date.today()
currentYear = todaysDate.year;
currentMonth = todaysDate.month;
currentDay = todaysDate.day;

def yearOrHour(income, yearOrHour, startDate, endDate, daysWorkedPerWeek = 5, hoursPerWeek = 40, daysWorked = 'Mon Tue Wed Thu Fri'):
    income = float(income);
    ###################### Income Input Start ###########################################################################################
    if yearOrHour == 0:
        ###This tells it to not worry about the dates and just assume the imcome is total###
        return income;
        exit;
    ####################################################################################
    ###This tells it to worry about the business dates###
    elif yearOrHour == 1:
    ###################### Counts buisnessdays worked Start ###########################################################################################
        startToEndBusinessDays = np.busday_count(startDate, endDate, weekmask = daysWorked)
        print("Days that will be worked:" + str(startToEndBusinessDays));
        income *= (hoursPerWeek/daysWorkedPerWeek)*startToEndBusinessDays;
        print(income);
        return income;
    ###################### Counts buisnessdays worked End ###########################################################################################

    else: print("Error in YearOrHour");

    ###################### Income Input End ###########################################################################################

def incomeTax(income):
    income = float(income)
    if income < 0:
            print("Error, input positive income.");
            return;
    ######################FED TAX START###########################################################################################
    global taxPerBracket;
    global taxBracketPercents;
    global taxBracketAmounts;
    global totalFedTax;
    global afterFedTax;
    global incomeLeftOverAfterTaxs;
    standardDeduction = 12400.00; ###SUBJECT TO CHANGE EACH YEAR###
    leftOver = income - standardDeduction;
    
    ###BRACKETS ARE SUBJECT TO CHANGE EACH YEAR###
    totalFedBrakets = 7;
    taxBracketAmounts = [9875.00,40125.00,85525.00,163300.00,207350.00,518401.00,float(leftOver),0]; #ALLWAYS HAVE A 0 AT TH END   last 0 is for -1 in first if
    taxBracketPercents = [10/100,12/100,22/100,24/100,32/100,35/100,37/100]; ###SUBJECT TO CHANGE EACH YEAR###
    ###BRACKETS ARE SUBJECT TO CHANGE EACH YEAR###

    taxPerBracket = [0]*totalFedBrakets
    for i in range (0,totalFedBrakets):
        if leftOver >= taxBracketAmounts[i]:
            taxPerBracket[i] = (taxBracketAmounts[i]-taxBracketAmounts[i-1])*taxBracketPercents[i];
            leftOver -= (taxBracketAmounts[i]-taxBracketAmounts[i-1]);
        elif leftOver < taxBracketAmounts[i] and leftOver >= 0:
            taxPerBracket[i] = leftOver*taxBracketPercents[i];
            leftOver -= taxBracketPercents[i]*leftOver;
            break;
        else:
            break
    totalFedTax = sum(taxPerBracket)
    ###################### FED TAX END ###########################################################################################
    ###################### STATE TAX START #######################################################################################
    MI_TaxRate = 4.25/100
    stateTaxRate = MI_TaxRate
    totalStateTax = income*stateTaxRate;
    ###################### STATE TAX END #########################################################################################
    ###################### SOCIAL SECURITY TAX START #############################################################################
    taxableToSocialCapIncome = 142800.00; ###SUBJECT TO CHANGE EACH YEAR###
    socialSecurityFlatRate = 6.20/100; ###SUBJECT TO CHANGE EACH YEAR###
    maxSocialSeurityTax = taxableToSocialCapIncome*socialSecurityFlatRate
    if income >= taxableToSocialCapIncome:
        totalSocialTax = maxSocialSeurityTax;
    else:
        totalSocialTax = income*socialSecurityFlatRate
    maxSocialSeurityTax = taxableToSocialCapIncome*socialSecurityFlatRate;
    ###################### SOCIAL SECURITY TAX END ###############################################################################
    ###################### MEDICARE TAX START ####################################################################################
    medicareFlatTaxRate = 1.45/100; ###SUBJECT TO CHANGE EACH YEAR###
    additionalMedicareAfter = 200000.00; ###SUBJECT TO CHANGE EACH YEAR###
    additionalMedicareRate = 0.9/100; ###SUBJECT TO CHANGE EACH YEAR###
    if income > additionalMedicareAfter:
        totalMedicareTax = (additionalMedicareAfter*medicareFlatTaxRate)+((income-additionalMedicareAfter)*(medicareFlatTaxRate+additionalMedicareRate));
    else:  
        totalMedicareTax = income*medicareFlatTaxRate;
    ###################### MEDICARE TAX END ######################################################################################
    ###################### FINAL CALCULATIONS START ##############################################################################
    incomeLeftOverAfterTaxs = income-totalFedTax-totalStateTax-totalSocialTax-totalMedicareTax
    return incomeLeftOverAfterTaxs;
    ###################### FINAL CALCULATIONS END ################################################################################


def validating():
    QDoubleValidator()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1129, 861)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMouseTracking(False)
        MainWindow.setTabletTracking(False)
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 555, 154))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.startDateInput = QtWidgets.QDateEdit(self.gridLayoutWidget)
        self.startDateInput.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(1752, 9, 14), QtCore.QTime(0, 0, 0)))
        self.startDateInput.setCalendarPopup(True)
        self.startDateInput.setDate(QtCore.QDate(currentYear, 1, 1))
        self.startDateInput.setObjectName("startDateInput")
        self.horizontalLayout.addWidget(self.startDateInput)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.endDateInput = QtWidgets.QDateEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endDateInput.sizePolicy().hasHeightForWidth())
        self.endDateInput.setSizePolicy(sizePolicy)
        self.endDateInput.setBaseSize(QtCore.QSize(0, 0))
        self.endDateInput.setMaximumTime(QtCore.QTime(1, 59, 59))
        self.endDateInput.setCalendarPopup(True)
        self.endDateInput.setDate(QtCore.QDate(currentYear, 12, 31))
        self.endDateInput.setObjectName("endDateInput")
        self.horizontalLayout.addWidget(self.endDateInput)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        self.incomeCalculateButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.incomeCalculateButton.setObjectName("incomeCalculateButton")
        self.gridLayout.addWidget(self.incomeCalculateButton, 4, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.incomeAfterTaxLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka Heading")
        font.setPointSize(16)
        self.incomeAfterTaxLabel.setFont(font)
        self.incomeAfterTaxLabel.setObjectName("incomeAfterTaxLabel")
        self.horizontalLayout_2.addWidget(self.incomeAfterTaxLabel)
        self.incomeAfterTaxOutput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.incomeAfterTaxOutput.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incomeAfterTaxOutput.sizePolicy().hasHeightForWidth())
        self.incomeAfterTaxOutput.setSizePolicy(sizePolicy)
        self.incomeAfterTaxOutput.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.incomeAfterTaxOutput.setFont(font)
        self.incomeAfterTaxOutput.setText("")
        self.incomeAfterTaxOutput.setFrame(True)
        self.incomeAfterTaxOutput.setDragEnabled(True)
        self.incomeAfterTaxOutput.setClearButtonEnabled(False)
        self.incomeAfterTaxOutput.setObjectName("incomeAfterTaxOutput")
        self.horizontalLayout_2.addWidget(self.incomeAfterTaxOutput)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.incomeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Sitka Heading")
        font.setPointSize(16)
        self.incomeLabel.setFont(font)
        self.incomeLabel.setObjectName("incomeLabel")
        self.horizontalLayout_3.addWidget(self.incomeLabel)
        self.incomeInput = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.incomeInput.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incomeInput.sizePolicy().hasHeightForWidth())
        self.incomeInput.setSizePolicy(sizePolicy)
        self.incomeInput.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.incomeInput.setFont(font)
        self.incomeInput.setText("")
        self.incomeInput.setFrame(True)
        self.incomeInput.setDragEnabled(True)
        self.incomeInput.setClearButtonEnabled(False)
        self.incomeInput.setObjectName("incomeInput")
        self.horizontalLayout_3.addWidget(self.incomeInput)
        self.yearOrHourInput = QtWidgets.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.yearOrHourInput.setFont(font)
        self.yearOrHourInput.setEditable(False)
        self.yearOrHourInput.setObjectName("yearOrHourInput")
        self.yearOrHourInput.addItem("")
        self.yearOrHourInput.addItem("")
        self.horizontalLayout_3.addWidget(self.yearOrHourInput)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1129, 26))
        self.menubar.setObjectName("menubar")
        self.menuInome = QtWidgets.QMenu(self.menubar)
        self.menuInome.setObjectName("menuInome")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuInome.menuAction())

        self.retranslateUi(MainWindow)
        self.yearOrHourInput.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        self.incomeCalculateButton.clicked.connect(self.incomeCalculate);
    def incomeCalculate(self):
            startDate = dt.date(self.startDateInput.date().year(), self.startDateInput.date().month(), self.startDateInput.date().day());
            endDate = dt.date(self.endDateInput.date().year(), self.endDateInput.date().month(), self.endDateInput.date().day());
            startToEndBusinessDays = np.busday_count(startDate, endDate)
            global income;
            income = self.incomeInput.text();
            income = yearOrHour(income, self.yearOrHourInput.currentIndex(), startDate, endDate, daysWorkedPerWeek = 5, hoursPerWeek = 40, daysWorked = 'Mon Tue Wed Thu Fri')
            self.incomeAfterTaxOutput.setText(str(incomeTax(income)));




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "From:"))
        self.label_3.setText(_translate("MainWindow", "To:"))
        self.incomeCalculateButton.setText(_translate("MainWindow", "Calculate"))
        self.incomeAfterTaxLabel.setText(_translate("MainWindow", "Income After Tax:"))
        self.incomeAfterTaxOutput.setPlaceholderText(_translate("MainWindow", "$0.00"))
        self.incomeLabel.setText(_translate("MainWindow", "Income:"))
        self.incomeInput.setPlaceholderText(_translate("MainWindow", "$100,000.00"))
        self.yearOrHourInput.setItemText(0, _translate("MainWindow", "/Yr"))
        self.yearOrHourInput.setItemText(1, _translate("MainWindow", "/Hr"))
        self.menuInome.setTitle(_translate("MainWindow", "Inome"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


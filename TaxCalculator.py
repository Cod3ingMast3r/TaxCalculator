import PyQt5
import PyQt5.QtWidgets as qtw;
import PyQt5.QtGui as qtg;
import numpy as np;
import datetime as dt;
global income;
global todaysDate;
global currentYear;
global currentMonth;
global currentDay;
global incomeTax;
#currently assumed not head of househod and filing single and NOT self employed
#Planning to add the following
    #assuming not head of houshold, later add option for asking if they are head of household
    #add ability to update standard deduction maybe using API or webscrapper on google


def incomeTax(income):
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
    ###################### FINAL CALCULATIONS END ################################################################################
    
class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__();
        self.setWindowTitle("Tax Calculator")

        ###################### Layout Start ###########################################################################################
        
        self.setLayout(qtw.QVBoxLayout());
        
        my_label = qtw.QLabel("Input Income Here");
        my_label.setFont(qtg.QFont('Helvetica', 18));
        self.layout().addWidget(my_label);

        #entry Box
        my_income = qtw.QLineEdit();
        my_income.setObjectName("Income");
        my_income.setPlaceholderText("100,000.00");
        my_income.setFont(qtg.QFont('Helvetica', 18));
        self.layout().addWidget(my_income);

        #create a button
        my_button = qtw.QPushButton("Enter" , 
        clicked = lambda: calculate())
        self.layout().addWidget(my_button);

        my_afterTax = qtw.QLabel("Money Left After Tax:");
        my_afterTax.setFont(qtg.QFont('Helvetica', 12));
        self.layout().addWidget(my_afterTax);

        def calculate():
            incomeTax(float(my_income.text()));
            my_afterTax.setText("Money Left After Tax: " +str(incomeLeftOverAfterTaxs))







        ###################### Layout End ###########################################################################################


        self.show();



app = qtw.QApplication([]);

mw = MainWindow();

app.exec_();

todaysDate = dt.date.today()
print(todaysDate);
currentYear = todaysDate.year;
print(currentYear);
currentMonth = todaysDate.month;
print(currentMonth);
currentDay = todaysDate.day;
print(currentDay);

###################### Income Input Start ###########################################################################################
yearOrHour = input("Income By year or Hour: ");
print( yearOrHour.capitalize());

if yearOrHour.capitalize() == "Year":
    income = float(input("Put yearly total income here: "));
elif yearOrHour.capitalize() == "Hour":
    income = float(input("Put hourly total income here: "));
    hoursPerWeek = float(input("Put hours per week here: "));
###################### Counts buisnessdays worked Start ###########################################################################################
    setTime = input("Will there be a fixed start and end date? (yes or no): ");
    if setTime.capitalize() == "Yes":
        startYear = int(input("Input start year here (ie: 2021): "));
        startMonth = int(input("Input start month here (ie: Jan so, 1): "));
        startDay = int(input("Input start day here (ie: 1): "));
        endYear = int(input("Input end date year (ie: 2021): "));
        endMonth = int(input("Input end month here (ie: Jan so, 1): "));
        endDay = int(input("Input end day here (ie: 1): "));
        startDate = dt.date(startYear, startMonth, startDay);
        endDate = dt.date(endYear, endMonth, endDay);
        startToEndBusinessDays = np.busday_count(startDate, endDate)
        print("Days that will be worked:" + str(startToEndBusinessDays));
        income *= (hoursPerWeek/5)*startToEndBusinessDays;
    elif setTime.capitalize() == "No":
        print("Since not set time, the hourly income is multiplied by every workday in current year")
        startDate = dt.date(currentYear, 1, 1);
        endDate = dt.date(currentYear, 12, 31);
        startToEndBusinessDays = np.busday_count(startDate, endDate)
        print("Days that will be worked in current Year without sick or vacation or PTO:" + str(startToEndBusinessDays));
        income *= (hoursPerWeek/5)*startToEndBusinessDays;
        exit;
    else: 
        print("error, yes or no value may have been enetered incorrectly");
###################### Counts buisnessdays worked End ###########################################################################################

else: print("Error, enter hour or year only")
###################### Income Input End ###########################################################################################


def incomeTax(income):
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
    ###################### FINAL CALCULATIONS END ################################################################################
incomeTax(income);
print(incomeLeftOverAfterTaxs);



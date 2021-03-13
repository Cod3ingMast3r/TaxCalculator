global income;
#currently assumed not head of househod and filing single and NOT self employed
#Planning to add the following
    #write if statements for week vs month vs quarter vs hour vs year incomes
    #assuming not head of houshold, later add option for asking if they are head of household
    #add ability to update standard deduction maybe using API or webscrapper on google
income = float(input("Put yearly total income here: "));

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
incomeTax(income)
print(incomeLeftOverAfterTaxs)
from datetime import datetime
import datetime
from math import floor
from tkinter import messagebox
import customtkinter as ctk
import os
import sys
from PIL import Image
from dateutil.relativedelta import relativedelta

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    
        # create tabs
        self.add("CHASE")
        self.add("CITIBANK-OTHERS")
        self.add("CITIBANK-MACYS")
        self.add("TARGET-TD")
        self.add("BQ")
        self.add("CAVALRY")
        
        #-----CHASE TAB-----
        self.chaseFrame = ctk.CTkFrame(self.tab('CHASE'))
        self.chaseFrame.pack(fill="both", expand=True)
        
        #payment entry label and variable
        self.chasePaymentAmount = ctk.CTkLabel(self.chaseFrame, text='*ACCOUNT BALANCE:')
        self.chasePaymentAmount.grid(row=1, column=0, pady=5, padx=5)
        self.chasePaymentVar = ctk.StringVar()
        #Payment Entry box
        self.chasePaymentAmountEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chasePaymentVar)
        self.chasePaymentAmountEntry.grid(row=1, column=1, pady=5, padx=5)
        
        #NRC PAYMENT LABEL AND ENTRY
        self.chasePaymentNRC = ctk.CTkLabel(self.chaseFrame, text='Enter NRC USD:')
        self.chasePaymentNRC.grid(row=2, column=0, pady=5, padx=5)
        self.chaseNRCVar = ctk.StringVar()
        
        self.chasePaymentNRCEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseNRCVar)
        self.chasePaymentNRCEntry.grid(row=2, column=1, pady=5, padx=5)
        
         #calculate button
        self.buttonPayment = ctk.CTkButton(self.chaseFrame, text='Calculate', width=20, height=10, command=self.chasePrincipal)
        self.buttonPayment.grid(row=3, column=1, pady=5, padx=5)
        
        #*ORIGINAL SETTLEMENT AMOUNT
        self.chaseSettlementLabel = ctk.CTkLabel(self.chaseFrame, text='*SETTLEMENT AMOUNT:')
        self.chaseSettlementLabel.grid(row=4, column=0, pady=5, padx=5)
        self.chaseSettlementVar = ctk.StringVar()
        
        self.chaseSettlementEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseSettlementVar)
        self.chaseSettlementEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #DOWN PAYMENT
        self.chaseDownPaymentLabel = ctk.CTkLabel(self.chaseFrame, text='INITIAL PAYMENT:\n(DOWN PAYMENT)')
        self.chaseDownPaymentLabel.grid(row=5, column=0, pady=5, padx=5)
        self.chaseDownPaymentVar = ctk.StringVar()
        
        self.chaseDownPaymentEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseDownPaymentVar)
        self.chaseDownPaymentEntry.grid(row=5, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.chaseNumberOfPaymentsLabel = ctk.CTkLabel(self.chaseFrame, text='*NUMBER OF PAYMENTS:')
        self.chaseNumberOfPaymentsLabel.grid(row=6, column=0, pady=5, padx=5)
        self.chaseNumberOfPaymentsVar = ctk.StringVar()
        
        self.chaseNumberOfPaymentsEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseNumberOfPaymentsVar)
        self.chaseNumberOfPaymentsEntry.grid(row=6, column=1, pady=5, padx=5)
        
        #FIRST PAYMENT DATE
        self.chaseFirstPaymentLabel = ctk.CTkLabel(self.chaseFrame, text='*FIRST PAYMENT DATE:')
        self.chaseFirstPaymentLabel.grid(row=7, column=0, pady=5, padx=5)
        self.chaseFirstPaymentVar = ctk.StringVar()
        
        self.chaseFirstPaymentEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseFirstPaymentVar)
        self.chaseFirstPaymentEntry.grid(row=7, column=1, pady=5, padx=5)
        
        #clear date on left-click
        chaseDateClickedBox = self.chaseFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.chaseFirstPaymentEntry, chaseDateClickedBox))

        #blankspace
        calculations = ctk.CTkLabel(self.chaseFrame, text='                                   ')
        calculations.grid(row=4, column=3)
        topline = ctk.CTkLabel(self.chaseFrame, text='  ')
        topline.grid(row=0, column=1)
        
        #LUMP SUM 90%
        self.chaseLumpSum90Label = ctk.CTkLabel(self.chaseFrame, text='LUMP SUM 90%:')
        self.chaseLumpSum90Label.grid(row=0, column=4, pady=5, padx=5)
        
        self.chaseLumpSum90Textbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseLumpSum90Textbox.grid(row=1, column=4, padx=5,pady=5,)
        self.chaseLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.chaseLumpSum85Label = ctk.CTkLabel(self.chaseFrame, text='LUMP SUM 85%:')
        self.chaseLumpSum85Label.grid(row=2, column=4, pady=5, padx=5)
        
        self.chaseLumpSum85Textbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseLumpSum85Textbox.grid(row=3, column=4, padx=5,pady=5,)
        self.chaseLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.chaseLumpSum80Label = ctk.CTkLabel(self.chaseFrame, text='LUMP SUM 80%:')
        self.chaseLumpSum80Label.grid(row=4, column=4, pady=5, padx=5)
        
        self.chaseLumpSum80Textbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseLumpSum80Textbox.grid(row=5, column=4, padx=5,pady=5,)
        self.chaseLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.chaseLumpSum75Label = ctk.CTkLabel(self.chaseFrame, text='LUMP SUM 75%:')
        self.chaseLumpSum75Label.grid(row=6, column=4, pady=5, padx=5)
        
        self.chaseLumpSum75Textbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseLumpSum75Textbox.grid(row=7, column=4, padx=5,pady=5,)
        self.chaseLumpSum75Textbox.configure(state="disabled")
        
        #FINAL PAYMENT
        self.chaseFinalPaymentLabel = ctk.CTkLabel(self.chaseFrame, text='FINAL PAYMENT:')
        self.chaseFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.chaseFinalPaymentTextbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5,)
        self.chaseFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.chaseLastPaymentDateLabel = ctk.CTkLabel(self.chaseFrame, text='FINAL PAYMENT DATE:')
        self.chaseLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.chaseLastPaymentDateTextbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5,)
        self.chaseLastPaymentDateTextbox.configure(state="disabled")
        
        #SIF EXPIRATION DATE
        self.chaseSifExpirationDateLabel = ctk.CTkLabel(self.chaseFrame, text='SIF EXPIRATION DATE:')
        self.chaseSifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.chaseSifExpirationDateTextbox = ctk.CTkTextbox(self.chaseFrame, width=100, height=5)
        self.chaseSifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5,)
        self.chaseSifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.chaseMonthlyPaymentLabel = ctk.CTkLabel(self.chaseFrame, text='Custom Monthly Payment')
        self.chaseMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.chaseMonthlyPaymentVar = ctk.StringVar()
        
        self.chaseMonthlyPaymentEntry = ctk.CTkEntry(self.chaseFrame, textvariable=self.chaseMonthlyPaymentVar, width=100)
        self.chaseMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        chaseMonthlyPaymentClickedBox = self.chaseMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.chaseMonthlyPaymentEntry, chaseMonthlyPaymentClickedBox))
        
        #calculate button
        self.button1 = ctk.CTkButton(self.chaseFrame, text='Calculate', width=20, height=10, command=self.chaseTab)
        self.button1.grid(row=8, column=1, pady=5, padx=5)    
        
        #reset button
        self.chaseResetButton = ctk.CTkButton(self.chaseFrame, text='Reset', width=20, height=10, command=self.chaseReset)
        self.chaseResetButton.grid(row=8, column=2, pady=5, padx=5)    
        
        #set entry boxes to zero
        self.chasePaymentVar.set("")
        self.chaseSettlementVar.set("")
        self.chaseDownPaymentVar.set("")
        self.chaseNumberOfPaymentsVar.set("")
        self.chaseFirstPaymentVar.set("MM/DD/YYYY")
        
        #----------------------------------------------------------------------------------------------------------------
        #CITI OTHER TAB
        self.citiOtherFrame = ctk.CTkFrame(self.tab('CITIBANK-OTHERS'))
        self.citiOtherFrame.pack(fill="both", expand=True)
        
        #payment entry label and variable
        self.citiOtherPaymentAmount = ctk.CTkLabel(self.citiOtherFrame, text='*ACCOUNT BALANCE:')
        self.citiOtherPaymentAmount.grid(row=1, column=0, pady=5, padx=5)
        self.citiOtherPaymentVar = ctk.StringVar()
    
        self.citiOtherPaymentAmountEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherPaymentVar)
        self.citiOtherPaymentAmountEntry.grid(row=1, column=1, pady=5, padx=5)
        
        #calculate button
        self.citiOtherButtonPayment = ctk.CTkButton(self.citiOtherFrame, text='Calculate', width=20, height=10, command=self.citiOtherSettlement)
        self.citiOtherButtonPayment.grid(row=2, column=1, pady=5, padx=5)
        
        #*ORIGINAL SETTLEMENT AMOUNT
        self.citiOtherSettlementLabel = ctk.CTkLabel(self.citiOtherFrame, text='*SETTLEMENT AMOUNT:')
        self.citiOtherSettlementLabel.grid(row=3, column=0, pady=5, padx=5)
        self.citiOtherSettlementVar = ctk.StringVar()
        
        self.citiOtherSettlementEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherSettlementVar)
        self.citiOtherSettlementEntry.grid(row=3, column=1, pady=5, padx=5)
        
        #INITIALPAYMENT
        self.citiOtherDownPaymentLabel = ctk.CTkLabel(self.citiOtherFrame, text='INITIAL PAYMENT:\n(DOWNPAYMENT)')
        self.citiOtherDownPaymentLabel.grid(row=4, column=0, pady=5, padx=5)
        self.citiOtherDownPaymentVar = ctk.StringVar()
        
        self.citiOtherDownPaymentEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherDownPaymentVar)
        self.citiOtherDownPaymentEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.citiOtherNumberOfPaymentsLabel = ctk.CTkLabel(self.citiOtherFrame, text='*NUMBER OF PAYMENTS:')
        self.citiOtherNumberOfPaymentsLabel.grid(row=5, column=0, pady=5, padx=5)
        self.citiOtherNumberOfPaymentsVar = ctk.StringVar()
        
        self.citiOtherNumberOfPaymentsEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherNumberOfPaymentsVar)
        self.citiOtherNumberOfPaymentsEntry.grid(row=5, column=1, pady=5, padx=5)
    
        #FIRST PAYMENT DATE
        self.citiOtherFirstPaymentLabel = ctk.CTkLabel(self.citiOtherFrame, text='*FIRST PAYMENT DATE:')
        self.citiOtherFirstPaymentLabel.grid(row=6, column=0, pady=5, padx=5)
        self.citiOtherFirstPaymentVar = ctk.StringVar()
        
        self.citiOtherFirstPaymentEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherFirstPaymentVar)
        self.citiOtherFirstPaymentEntry.grid(row=6, column=1, pady=5, padx=5)
        
        #clear date on left-click
        citiOtherFirstPaymentClear = self.citiOtherFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiOtherFirstPaymentEntry, citiOtherFirstPaymentClear))
        
        #set entry boxes to zero
        self.citiOtherPaymentVar.set("")
        self.citiOtherSettlementVar.set("")
        self.citiOtherDownPaymentVar.set("")
        self.citiOtherNumberOfPaymentsVar.set("")
        self.citiOtherFirstPaymentVar.set("MM/DD/YYYY")
        
        #blankspace
        citiOtherCalculations = ctk.CTkLabel(self.citiOtherFrame, text='                                         ')
        citiOtherCalculations.grid(row=4, column=3)
        citiOtherTopline = ctk.CTkLabel(self.citiOtherFrame, text='  ')
        citiOtherTopline.grid(row=0, column=1)
        
        #TEXT BOXES FOR CALCULATIONS        
        #LUMP SUM 90%
        self.citiOtherLumpSum90Label = ctk.CTkLabel(self.citiOtherFrame, text='LUMP SUM 90%:')
        self.citiOtherLumpSum90Label.grid(row=0, column=4, pady=5, padx=5)
        
        self.citiOtherLumpSum90Textbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherLumpSum90Textbox.grid(row=1, column=4, padx=5,pady=5,)
        self.citiOtherLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.citiOtherLumpSum85Label = ctk.CTkLabel(self.citiOtherFrame, text='LUMP SUM 85%:')
        self.citiOtherLumpSum85Label.grid(row=2, column=4, pady=5, padx=5)
        
        self.citiOtherLumpSum85Textbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherLumpSum85Textbox.grid(row=3, column=4, padx=5,pady=5,)
        self.citiOtherLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.citiOtherLumpSum80Label = ctk.CTkLabel(self.citiOtherFrame, text='LUMP SUM 80%:')
        self.citiOtherLumpSum80Label.grid(row=4, column=4, pady=5, padx=5)
        
        self.citiOtherLumpSum80Textbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherLumpSum80Textbox.grid(row=5, column=4, padx=5,pady=5,)
        self.citiOtherLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.citiOtherLumpSum75Label = ctk.CTkLabel(self.citiOtherFrame, text='LUMP SUM 75%:')
        self.citiOtherLumpSum75Label.grid(row=6, column=4, pady=5, padx=5)
        
        self.citiOtherLumpSum75Textbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherLumpSum75Textbox.grid(row=7, column=4, padx=5,pady=5,)
        self.citiOtherLumpSum75Textbox.configure(state="disabled")
     
        #FINAL PAYMENT
        self.citiOtherFinalPaymentLabel = ctk.CTkLabel(self.citiOtherFrame, text='FINAL PAYMENT:')
        self.citiOtherFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.citiOtherFinalPaymentTextbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5)
        self.citiOtherFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.citiOtherLastPaymentDateLabel = ctk.CTkLabel(self.citiOtherFrame, text='FINAL PAYMENT DATE:')
        self.citiOtherLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.citiOtherLastPaymentDateTextbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5)
        self.citiOtherLastPaymentDateTextbox.configure(state="disabled")
        
        #SIF EXPIRATION DATE
        self.citiOtherSifExpirationDateLabel = ctk.CTkLabel(self.citiOtherFrame, text='SIF EXPIRATION DATE:')
        self.citiOtherSifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.citiOtherSifExpirationDateTextbox = ctk.CTkTextbox(self.citiOtherFrame, width=100, height=5)
        self.citiOtherSifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5)
        self.citiOtherSifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.citiOtherMonthlyPaymentLabel = ctk.CTkLabel(self.citiOtherFrame, text='Custom Monthly Payment')
        self.citiOtherMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.citiOtherMonthlyPaymentVar = ctk.StringVar()
        
        self.citiOtherMonthlyPaymentEntry = ctk.CTkEntry(self.citiOtherFrame, textvariable=self.citiOtherMonthlyPaymentVar, width=100)
        self.citiOtherMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        citiOtherMonthlyPaymentClickedBox = self.citiOtherMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiOtherMonthlyPaymentEntry, citiOtherMonthlyPaymentClickedBox))

        #calculate button
        self.citiOtherButton1 = ctk.CTkButton(self.citiOtherFrame, text='Calculate', width=20, height=10, command=self.citiOtherTab)
        self.citiOtherButton1.grid(row=7, column=1, pady=5, padx=5)

        #reset button
        self.citiOtherResetButton = ctk.CTkButton(self.citiOtherFrame, text='Reset', width=20, height=10, command=self.citiOtherReset)
        self.citiOtherResetButton.grid(row=7, column=2, pady=5, padx=5)  
        
        #----------------------------------------------------------------------------------------------------------------------------------
        #CitiBank MACYS
        #CITI MACY TAB
        self.citiMacysFrame = ctk.CTkFrame(self.tab('CITIBANK-MACYS'))
        self.citiMacysFrame.pack(fill="both", expand=True)
        
        #payment entry label and variable
        self.citiMacysPaymentAmount = ctk.CTkLabel(self.citiMacysFrame, text='*ACCOUNT BALANCE:')
        self.citiMacysPaymentAmount.grid(row=1, column=0, pady=5, padx=5)
        self.citiMacysPaymentVar = ctk.StringVar()
    
        self.citiMacysPaymentAmountEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysPaymentVar)
        self.citiMacysPaymentAmountEntry.grid(row=1, column=1, pady=5, padx=5)
        
        #calculate button
        self.citiMacysButtonPayment = ctk.CTkButton(self.citiMacysFrame, text='Calculate', width=20, height=10, command=self.citiMacySettlement)
        self.citiMacysButtonPayment.grid(row=2, column=1, pady=5, padx=5)
        
        #*ORIGINAL SETTLEMENT AMOUNT
        self.citiMacysSettlementLabel = ctk.CTkLabel(self.citiMacysFrame, text='*SETTLEMENT AMOUNT:')
        self.citiMacysSettlementLabel.grid(row=3, column=0, pady=5, padx=5)
        self.citiMacysSettlementVar = ctk.StringVar()
        
        self.citiMacysSettlementEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysSettlementVar)
        self.citiMacysSettlementEntry.grid(row=3, column=1, pady=5, padx=5)
        
        #DOWN PAYMENT
        self.citiMacysDownPaymentLabel = ctk.CTkLabel(self.citiMacysFrame, text='INITIAL PAYMENT:\n(DOWN PAYMENT)')
        self.citiMacysDownPaymentLabel.grid(row=4, column=0, pady=5, padx=5)
        self.citiMacysDownPaymentVar = ctk.StringVar()
    
        self.citiMacysDownPaymentEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysDownPaymentVar)
        self.citiMacysDownPaymentEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.citiMacysNumberOfPaymentsLabel = ctk.CTkLabel(self.citiMacysFrame, text='*NUMBER OF PAYMENTS:')
        self.citiMacysNumberOfPaymentsLabel.grid(row=5, column=0, pady=5, padx=5)
        self.citiMacysNumberOfPaymentsVar = ctk.StringVar()
        
        self.citiMacysNumberOfPaymentsEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysNumberOfPaymentsVar)
        self.citiMacysNumberOfPaymentsEntry.grid(row=5, column=1, pady=5, padx=5)
        
        #FIRST PAYMENT DATE
        self.citiMacysFirstPaymentLabel = ctk.CTkLabel(self.citiMacysFrame, text='*FIRST PAYMENT DATE:')
        self.citiMacysFirstPaymentLabel.grid(row=6, column=0, pady=5, padx=5)
        self.citiMacysFirstPaymentVar = ctk.StringVar()
        
        self.citiMacysFirstPaymentEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysFirstPaymentVar)
        self.citiMacysFirstPaymentEntry.grid(row=6, column=1, pady=5, padx=5)
        
        #clear date on left-click
        citiMacysFirstPaymentClear = self.citiMacysFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiMacysFirstPaymentEntry, citiMacysFirstPaymentClear))
        
        #set entry boxes to zero
        self.citiMacysPaymentVar.set("")
        self.citiMacysSettlementVar.set("")
        self.citiMacysDownPaymentVar.set("")
        self.citiMacysNumberOfPaymentsVar.set("")
        self.citiMacysFirstPaymentVar.set("MM/DD/YYYY") 
        
        #blankspace
        citiMacysCalculations = ctk.CTkLabel(self.citiMacysFrame, text='                                     ')
        citiMacysCalculations.grid(row=4, column=3)
        citiMacysTopline = ctk.CTkLabel(self.citiMacysFrame, text='  ')
        citiMacysTopline.grid(row=0, column=1)
        
        #TEXT BOXES FOR CALCULATIONS        
        #LUMP SUM 90%
        self.citiMacysLumpSum90Label = ctk.CTkLabel(self.citiMacysFrame, text='LUMP SUM 90%:')
        self.citiMacysLumpSum90Label.grid(row=0, column=4, pady=5, padx=5)
        
        self.citiMacysLumpSum90Textbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysLumpSum90Textbox.grid(row=1, column=4, padx=5,pady=5,)
        self.citiMacysLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.citiMacysLumpSum85Label = ctk.CTkLabel(self.citiMacysFrame, text='LUMP SUM 85%:')
        self.citiMacysLumpSum85Label.grid(row=2, column=4, pady=5, padx=5)
        
        self.citiMacysLumpSum85Textbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysLumpSum85Textbox.grid(row=3, column=4, padx=5,pady=5,)
        self.citiMacysLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.citiMacysLumpSum80Label = ctk.CTkLabel(self.citiMacysFrame, text='LUMP SUM 80%:')
        self.citiMacysLumpSum80Label.grid(row=4, column=4, pady=5, padx=5)
        
        self.citiMacysLumpSum80Textbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysLumpSum80Textbox.grid(row=5, column=4, padx=5,pady=5,)
        self.citiMacysLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.citiMacysLumpSum75Label = ctk.CTkLabel(self.citiMacysFrame, text='LUMP SUM 75%:')
        self.citiMacysLumpSum75Label.grid(row=6, column=4, pady=5, padx=5)
        
        self.citiMacysLumpSum75Textbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysLumpSum75Textbox.grid(row=7, column=4, padx=5,pady=5,)
        self.citiMacysLumpSum75Textbox.configure(state="disabled")
        
        #FINAL PAYMENT
        self.citiMacysFinalPaymentLabel = ctk.CTkLabel(self.citiMacysFrame, text='FINAL PAYMENT:')
        self.citiMacysFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.citiMacysFinalPaymentTextbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5,)
        self.citiMacysFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.citiMacysLastPaymentDateLabel = ctk.CTkLabel(self.citiMacysFrame, text='FINAL PAYMENT DATE:')
        self.citiMacysLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.citiMacysLastPaymentDateTextbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5,)
        self.citiMacysLastPaymentDateTextbox.configure(state="disabled")
        
        #SIF EXPIRATION DATE
        self.citiMacysSifExpirationDateLabel = ctk.CTkLabel(self.citiMacysFrame, text='SIF EXPIRATION DATE:')
        self.citiMacysSifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.citiMacysSifExpirationDateTextbox = ctk.CTkTextbox(self.citiMacysFrame, width=100, height=5)
        self.citiMacysSifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5)
        self.citiMacysSifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.citiMacysMonthlyPaymentLabel = ctk.CTkLabel(self.citiMacysFrame, text='Custom Monthly Payment')
        self.citiMacysMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.citiMacysMonthlyPaymentVar = ctk.StringVar()
        
        self.citiMacysMonthlyPaymentEntry = ctk.CTkEntry(self.citiMacysFrame, textvariable=self.citiMacysMonthlyPaymentVar, width=100)
        self.citiMacysMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        citiMacysMonthlyPaymentClickedBox = self.citiMacysMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiMacysMonthlyPaymentEntry, citiMacysMonthlyPaymentClickedBox))

        
        #calculate button
        self.citiMacysButton1 = ctk.CTkButton(self.citiMacysFrame, text='Calculate', width=20, height=10, command=self.citiMacyTab)
        self.citiMacysButton1.grid(row=7, column=1, pady=5, padx=5)
        
        #Reset button
        self.citiMacysResetButton = ctk.CTkButton(self.citiMacysFrame, text='Reset', width=20, height=10, command=self.citiMacyReset)
        self.citiMacysResetButton.grid(row=7, column=2, pady=5, padx=5)  
        
        #-------------------------------------------------------------------------------------------------------------------------------
        #TARGET
        self.targetFrame = ctk.CTkFrame(self.tab('TARGET-TD'))
        self.targetFrame.pack(fill="both", expand=True)
        
        #payment entry label and variable
        self.targetPaymentAmount = ctk.CTkLabel(self.targetFrame, text='*ACCOUNT BALANCE:')
        self.targetPaymentAmount.grid(row=1, column=0, pady=5, padx=5)
        self.targetPaymentVar = ctk.StringVar()
    
        self.targetPaymentAmountEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetPaymentVar)
        self.targetPaymentAmountEntry.grid(row=1, column=1, pady=5, padx=5)
        
        #calculate button
        self.targetButtonPayment = ctk.CTkButton(self.targetFrame, text='Calculate', width=20, height=10, command=self.targetSettlement)
        self.targetButtonPayment.grid(row=2, column=1, pady=5, padx=5)
        
        #*ORIGINAL SETTLEMENT AMOUNT
        self.targetSettlementLabel = ctk.CTkLabel(self.targetFrame, text='*SETTLEMENT AMOUNT:')
        self.targetSettlementLabel.grid(row=3, column=0, pady=5, padx=5)
        self.targetSettlementVar = ctk.StringVar()
        
        self.targetSettlementEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetSettlementVar)
        self.targetSettlementEntry.grid(row=3, column=1, pady=5, padx=5)
        
        #DOWN PAYMENT
        self.targetDownPaymentLabel = ctk.CTkLabel(self.targetFrame, text='INITIAL PAYMENT:\n(DOWN PAYMENT)')
        self.targetDownPaymentLabel.grid(row=4, column=0, pady=5, padx=5)
        self.targetDownPaymentVar = ctk.StringVar()
        
        self.targetDownPaymentEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetDownPaymentVar)
        self.targetDownPaymentEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.targetNumberOfPaymentsLabel = ctk.CTkLabel(self.targetFrame, text='*NUMBER OF PAYMENTS:')
        self.targetNumberOfPaymentsLabel.grid(row=5, column=0, pady=5, padx=5)
        self.targetNumberOfPaymentsVar = ctk.StringVar()
        
        self.targetNumberOfPaymentsEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetNumberOfPaymentsVar)
        self.targetNumberOfPaymentsEntry.grid(row=5, column=1, pady=5, padx=5)
        
        #FIRST PAYMENT DATE
        self.targetFirstPaymentLabel = ctk.CTkLabel(self.targetFrame, text='*FIRST PAYMENT DATE:')
        self.targetFirstPaymentLabel.grid(row=6, column=0, pady=5, padx=5)
        self.targetFirstPaymentVar = ctk.StringVar()
        
        self.targetFirstPaymentEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetFirstPaymentVar)
        self.targetFirstPaymentEntry.grid(row=6, column=1, pady=5, padx=5)
        
        #clear date on left-click
        targetFirstPaymentClear = self.targetFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.targetFirstPaymentEntry, targetFirstPaymentClear))
        
        #set entry boxes to zero
        self.targetPaymentVar.set("")
        self.targetSettlementVar.set("")
        self.targetDownPaymentVar.set("")
        self.targetNumberOfPaymentsVar.set("")
        self.targetFirstPaymentVar.set("MM/DD/YYYY")
        
        #blankspace
        targetCalculations = ctk.CTkLabel(self.targetFrame, text='                                   ')
        targetCalculations.grid(row=4, column=3)
        targetTopline = ctk.CTkLabel(self.targetFrame, text='  ')
        targetTopline.grid(row=0, column=1)
        
        #TEXT BOXES FOR CALCULATIONS        
        #LUMP SUM 90%
        self.targetLumpSum90Label = ctk.CTkLabel(self.targetFrame, text='LUMP SUM 90%:')
        self.targetLumpSum90Label.grid(row=0, column=4, pady=5, padx=5)
        
        self.targetLumpSum90Textbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetLumpSum90Textbox.grid(row=1, column=4, padx=5,pady=5,)
        self.targetLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.targetLumpSum85Label = ctk.CTkLabel(self.targetFrame, text='LUMP SUM 85%:')
        self.targetLumpSum85Label.grid(row=2, column=4, pady=5, padx=5)
        
        self.targetLumpSum85Textbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetLumpSum85Textbox.grid(row=3, column=4, padx=5,pady=5,)
        self.targetLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.targetLumpSum80Label = ctk.CTkLabel(self.targetFrame, text='LUMP SUM 80%:')
        self.targetLumpSum80Label.grid(row=4, column=4, pady=5, padx=5)
        
        self.targetLumpSum80Textbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetLumpSum80Textbox.grid(row=5, column=4, padx=5,pady=5,)
        self.targetLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.targetLumpSum75Label = ctk.CTkLabel(self.targetFrame, text='LUMP SUM 75%:')
        self.targetLumpSum75Label.grid(row=6, column=4, pady=5, padx=5)
        
        self.targetLumpSum75Textbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetLumpSum75Textbox.grid(row=7, column=4, padx=5,pady=5,)
        self.targetLumpSum75Textbox.configure(state="disabled")
        
        #FINAL PAYMENT
        self.targetFinalPaymentLabel = ctk.CTkLabel(self.targetFrame, text='FINAL PAYMENT:')
        self.targetFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.targetFinalPaymentTextbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5,)
        self.targetFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.targetLastPaymentDateLabel = ctk.CTkLabel(self.targetFrame, text='FINAL PAYMENT DATE:')
        self.targetLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.targetLastPaymentDateTextbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5,)
        self.targetLastPaymentDateTextbox.configure(state="disabled")
    
        #SIF EXPIRATION DATE
        self.targetSifExpirationDateLabel = ctk.CTkLabel(self.targetFrame, text='SIF EXPIRATION DATE:')
        self.targetSifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.targetSifExpirationDateTextbox = ctk.CTkTextbox(self.targetFrame, width=100, height=5)
        self.targetSifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5)
        self.targetSifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.targetMonthlyPaymentLabel = ctk.CTkLabel(self.targetFrame, text='Custom Monthly Payment')
        self.targetMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.targetMonthlyPaymentVar = ctk.StringVar()
        
        self.targetMonthlyPaymentEntry = ctk.CTkEntry(self.targetFrame, textvariable=self.targetMonthlyPaymentVar, width=100)
        self.targetMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        targetMonthlyPaymentClickedBox = self.targetMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.targetMonthlyPaymentEntry, targetMonthlyPaymentClickedBox))

        
        #calculate button
        self.targetButton1 = ctk.CTkButton(self.targetFrame, text='Calculate', width=20, height=10, command=self.targetTab)
        self.targetButton1.grid(row=7, column=1, pady=5, padx=5)
        
        #reset button
        self.targetResetButton = ctk.CTkButton(self.targetFrame, text='Reset', width=20, height=10, command=self.targetReset)
        self.targetResetButton.grid(row=7, column=2, pady=5, padx=5)  
        
        #------------------------------------------------------------------------------------------------------------------
        #BQ TAB
        self.bqFrame = ctk.CTkFrame(self.tab('BQ'))
        self.bqFrame.pack(fill="both", expand=True)
        
        #PRESUIT--POSTSUIT OptionMenu
        self.bqSuitVar = ctk.StringVar()
        self.bqSuitOption = ctk.CTkOptionMenu(self.bqFrame, values=['PRE-SUIT', 'POST-SUIT'], variable=self.bqSuitVar)
        self.bqSuitOption.grid(row=1, column=1, pady=5, padx=5)
        self.bqSuitOption.set('PRE-SUIT')
        
        #payment entry label and variable
        self.bqPaymentAmount = ctk.CTkLabel(self.bqFrame, text='*ACCOUNT BALANCE:')
        self.bqPaymentAmount.grid(row=2, column=0, pady=5, padx=5)
        self.bqPaymentVar = ctk.StringVar()
    
        self.bqPaymentAmountEntry = ctk.CTkEntry(self.bqFrame, textvariable=self.bqPaymentVar)
        self.bqPaymentAmountEntry.grid(row=2, column=1, pady=5, padx=5)
        
        #DOWN PAYMENT
        self.bqDownPaymentLabel = ctk.CTkLabel(self.bqFrame, text='INITIAL PAYMENT:\n(DOWN PAYMENT)')
        self.bqDownPaymentLabel.grid(row=3, column=0, pady=5, padx=5)
        self.bqDownPaymentVar = ctk.StringVar()
        
        self.bqDownPaymentEntry = ctk.CTkEntry(self.bqFrame, textvariable=self.bqDownPaymentVar)
        self.bqDownPaymentEntry.grid(row=3, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.bqNumberOfPaymentsLabel = ctk.CTkLabel(self.bqFrame, text='*NUMBER OF PAYMENTS:')
        self.bqNumberOfPaymentsLabel.grid(row=4, column=0, pady=5, padx=5)
        self.bqNumberOfPaymentsVar = ctk.StringVar()
        
        self.bqNumberOfPaymentsEntry = ctk.CTkEntry(self.bqFrame, textvariable=self.bqNumberOfPaymentsVar)
        self.bqNumberOfPaymentsEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #FIRST PAYMENT DATE
        self.bqFirstPaymentLabel = ctk.CTkLabel(self.bqFrame, text='*FIRST PAYMENT DATE:')
        self.bqFirstPaymentLabel.grid(row=5, column=0, pady=5, padx=5)
        self.bqFirstPaymentVar = ctk.StringVar()
        
        self.bqFirstPaymentEntry = ctk.CTkEntry(self.bqFrame, textvariable=self.bqFirstPaymentVar)
        self.bqFirstPaymentEntry.grid(row=5, column=1, pady=5, padx=5)
        
        #clear date on left-click
        bqFirstPaymentClear = self.bqFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.bqFirstPaymentEntry, bqFirstPaymentClear))
        
        #set entry boxes to zero
        self.bqPaymentVar.set("")
        self.bqDownPaymentVar.set("")
        self.bqNumberOfPaymentsVar.set("")
        self.bqFirstPaymentVar.set("MM/DD/YYYY") 
        
        #blankspace
        bqCalculations = ctk.CTkLabel(self.bqFrame, text='                                     ')
        bqCalculations.grid(row=4, column=3)
        bqTopline = ctk.CTkLabel(self.bqFrame, text='  ')
        bqTopline.grid(row=0, column=1)
        
        #FINAL PAYMENT
        self.bqFinalPaymentLabel = ctk.CTkLabel(self.bqFrame, text='FINAL PAYMENT:')
        self.bqFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.bqFinalPaymentTextbox = ctk.CTkTextbox(self.bqFrame, width=100, height=5)
        self.bqFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5,)
        self.bqFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.bqLastPaymentDateLabel = ctk.CTkLabel(self.bqFrame, text='FINAL PAYMENT DATE:')
        self.bqLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.bqLastPaymentDateTextbox = ctk.CTkTextbox(self.bqFrame, width=100, height=5)
        self.bqLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5,)
        self.bqLastPaymentDateTextbox.configure(state="disabled")
        
        #ORIGINAL SETTLEMENT TEXTBOX
        self.bqOriginalSettlementTextboxLabel = ctk.CTkLabel(self.bqFrame, text='ORIGINAL SETTLEMENT:')
        self.bqOriginalSettlementTextboxLabel.grid(row=0, column=4, pady=5, padx=5)
        
        self.bqOriginalSettlementTextbox = ctk.CTkTextbox(self.bqFrame, width=100, height=5)
        self.bqOriginalSettlementTextbox.grid(row=1, column=4, padx=5,pady=5,)
        self.bqOriginalSettlementTextbox.configure(state="disabled")
        
        #SETTLEMENT TEXTBOX
        self.bqSettlementTextboxLabel = ctk.CTkLabel(self.bqFrame, text='SETTLEMENT AMOUNT:')
        self.bqSettlementTextboxLabel.grid(row=2, column=4, pady=5, padx=5)
        
        self.bqSettlementTextbox = ctk.CTkTextbox(self.bqFrame, width=100, height=5)
        self.bqSettlementTextbox.grid(row=3, column=4, padx=5,pady=5,)
        self.bqSettlementTextbox.configure(state="disabled")
        
        #SIF EXPIRATION DATE
        self.bqSifExpirationDateLabel = ctk.CTkLabel(self.bqFrame, text='SIF EXPIRATION DATE:')
        self.bqSifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.bqSifExpirationDateTextbox = ctk.CTkTextbox(self.bqFrame, width=100, height=5)
        self.bqSifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5)
        self.bqSifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.bqMonthlyPaymentLabel = ctk.CTkLabel(self.bqFrame, text='Custom Monthly Payment')
        self.bqMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.bqMonthlyPaymentVar = ctk.StringVar()
        
        self.bqMonthlyPaymentEntry = ctk.CTkEntry(self.bqFrame, textvariable=self.bqMonthlyPaymentVar, width=100)
        self.bqMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        bqMonthlyPaymentClickedBox = self.bqMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.bqMonthlyPaymentEntry, bqMonthlyPaymentClickedBox))

        #calculate button
        self.bqButton1 = ctk.CTkButton(self.bqFrame, text='Calculate', width=20, height=10, command=self.bqTab)
        self.bqButton1.grid(row=6, column=1, pady=5, padx=5)
        
        #reset button
        self.bqResetButton = ctk.CTkButton(self.bqFrame, text='Reset', width=20, height=10, command=self.bqReset)
        self.bqResetButton.grid(row=6, column=2, pady=5, padx=5)  
        
        #------------------------------------------------------------------------------------------------------
        #CAVALRY TAB
        self.cavalryFrame = ctk.CTkFrame(self.tab('CAVALRY'))
        self.cavalryFrame.pack(fill="both", expand=True)
        
        #payment entry label and variable
        self.cavalryPaymentAmount = ctk.CTkLabel(self.cavalryFrame, text='*ACCOUNT BALANCE:')
        self.cavalryPaymentAmount.grid(row=1, column=0, pady=5, padx=5)
        self.cavalryPaymentVar = ctk.StringVar()
        
        self.cavalryPaymentAmountEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalryPaymentVar)
        self.cavalryPaymentAmountEntry.grid(row=1, column=1, pady=5, padx=5)
        
        #calculate button
        self.cavalrybuttonPayment = ctk.CTkButton(self.cavalryFrame, text='Calculate', width=20, height=10, command=self.cavalryPrincipal)
        self.cavalrybuttonPayment.grid(row=2, column=1, pady=5, padx=5)
        
        #*SETTLEMENT AMOUNT
        self.cavalrySettlementLabel = ctk.CTkLabel(self.cavalryFrame, text='*SETTLEMENT AMOUNT:')
        self.cavalrySettlementLabel.grid(row=3, column=0, pady=5, padx=5)
        self.cavalrySettlementVar = ctk.StringVar()
        
        self.cavalrySettlementEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalrySettlementVar)
        self.cavalrySettlementEntry.grid(row=3, column=1, pady=5, padx=5)
        
        #DOWN PAYMENT
        self.cavalryDownPaymentLabel = ctk.CTkLabel(self.cavalryFrame, text='INITIAL PAYMENT:\n(DOWN PAYMENT)')
        self.cavalryDownPaymentLabel.grid(row=4, column=0, pady=5, padx=5)
        self.cavalryDownPaymentVar = ctk.StringVar()
        
        self.cavalryDownPaymentEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalryDownPaymentVar)
        self.cavalryDownPaymentEntry.grid(row=4, column=1, pady=5, padx=5)
        
        #NUMBER OF PAYMENTS
        self.cavalryNumberOfPaymentsLabel = ctk.CTkLabel(self.cavalryFrame, text='*NUMBER OF PAYMENTS:')
        self.cavalryNumberOfPaymentsLabel.grid(row=5, column=0, pady=5, padx=5)
        self.cavalryNumberOfPaymentsVar = ctk.StringVar()
        
        self.cavalryNumberOfPaymentsEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalryNumberOfPaymentsVar)
        self.cavalryNumberOfPaymentsEntry.grid(row=5, column=1, pady=5, padx=5)
        
        #FIRST PAYMENT DATE
        self.cavalryFirstPaymentLabel = ctk.CTkLabel(self.cavalryFrame, text='*FIRST PAYMENT DATE:')
        self.cavalryFirstPaymentLabel.grid(row=6, column=0, pady=5, padx=5)
        self.cavalryFirstPaymentVar = ctk.StringVar()
        
        self.cavalryFirstPaymentEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalryFirstPaymentVar)
        self.cavalryFirstPaymentEntry.grid(row=6, column=1, pady=5, padx=5)
        
        #clear date on left-click
        cavalryFirstPaymentClear = self.cavalryFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.cavalryFirstPaymentEntry, cavalryFirstPaymentClear))
        
        #Set entry boxes to zero
        self.cavalryPaymentVar.set("")
        self.cavalrySettlementVar.set("")
        self.cavalryDownPaymentVar.set("")
        self.cavalryNumberOfPaymentsVar.set("")
        self.cavalryFirstPaymentVar.set("MM/DD/YYYY") 
        
        #blankspace
        cavalrycalculations = ctk.CTkLabel(self.cavalryFrame, text='                                  ')
        cavalrycalculations.grid(row=4, column=3)
        cavalrytopline = ctk.CTkLabel(self.cavalryFrame, text='  ')
        cavalrytopline.grid(row=0, column=1)
        
        #TEXT BOXES FOR CALCULATIONS
        #LUMP SUM 85%
        self.cavalryLumpSum85Label = ctk.CTkLabel(self.cavalryFrame, text='LUMP SUM 85%:')
        self.cavalryLumpSum85Label.grid(row=0, column=4, pady=5, padx=5)
        
        self.cavalryLumpSum85Textbox = ctk.CTkTextbox(self.cavalryFrame, width=100, height=5)
        self.cavalryLumpSum85Textbox.grid(row=1, column=4, padx=5,pady=5,)
        self.cavalryLumpSum85Textbox.configure(state="disabled")
      
        #FINAL PAYMENT
        self.cavalryFinalPaymentLabel = ctk.CTkLabel(self.cavalryFrame, text='FINAL PAYMENT:')
        self.cavalryFinalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.cavalryFinalPaymentTextbox = ctk.CTkTextbox(self.cavalryFrame, width=100, height=5)
        self.cavalryFinalPaymentTextbox.grid(row=1, column=5, padx=5,pady=5,)
        self.cavalryFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.cavalryLastPaymentDateLabel = ctk.CTkLabel(self.cavalryFrame, text='FINAL PAYMENT DATE:')
        self.cavalryLastPaymentDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.cavalryLastPaymentDateTextbox = ctk.CTkTextbox(self.cavalryFrame, width=100, height=5)
        self.cavalryLastPaymentDateTextbox.grid(row=3, column=5, padx=5,pady=5,)
        self.cavalryLastPaymentDateTextbox.configure(state="disabled")
        
        #SIF EXPIRATION DATE
        self.cavalrySifExpirationDateLabel = ctk.CTkLabel(self.cavalryFrame, text='SIF EXPIRATION DATE:')
        self.cavalrySifExpirationDateLabel.grid(row=4, column=5, pady=5, padx=5)
        
        self.cavalrySifExpirationDateTextbox = ctk.CTkTextbox(self.cavalryFrame, width=100, height=5)
        self.cavalrySifExpirationDateTextbox.grid(row=5, column=5, padx=5,pady=5)
        self.cavalrySifExpirationDateTextbox.configure(state="disabled")
        
        #CUSTOM MONTHLY PAYMENT
        self.cavalryMonthlyPaymentLabel = ctk.CTkLabel(self.cavalryFrame, text='Custom Monthly Payment')
        self.cavalryMonthlyPaymentLabel.grid(row=6, column=5, pady=5, padx=5)
        self.cavalryMonthlyPaymentVar = ctk.StringVar()
        
        self.cavalryMonthlyPaymentEntry = ctk.CTkEntry(self.cavalryFrame, textvariable=self.cavalryMonthlyPaymentVar, width=100)
        self.cavalryMonthlyPaymentEntry.grid(row=7, column=5, pady=5, padx=5)
        cavalryMonthlyPaymentClickedBox = self.cavalryMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.cavalryMonthlyPaymentEntry, cavalryMonthlyPaymentClickedBox))
        
        #calculate button
        self.cavalrybutton1 = ctk.CTkButton(self.cavalryFrame, text='Calculate', width=20, height=10, command=self.cavalryTab)
        self.cavalrybutton1.grid(row=7, column=1, pady=5, padx=5) 
        
        #Reset button
        self.cavalryResetButton = ctk.CTkButton(self.cavalryFrame, text='Reset', width=20, height=10, command=self.cavalryReset)
        self.cavalryResetButton.grid(row=7, column=2, pady=5, padx=5) 
    
    def chaseReset(self):
        #Entry boxes
        self.chasePaymentVar.set("")
        self.chaseNRCVar.set("")
        self.chaseSettlementVar.set("")
        self.chaseDownPaymentVar.set("")
        self.chaseNumberOfPaymentsVar.set("")
        self.chaseFirstPaymentVar.set("MM/DD/YYYY")
        self.chaseMonthlyPaymentVar.set('')
        
        #clear date on left-click
        chaseDateClickedBox = self.chaseFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.chaseFirstPaymentEntry, chaseDateClickedBox)) 
        chaseMonthlyPaymentClickedBox = self.chaseMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.chaseMonthlyPaymentEntry, chaseMonthlyPaymentClickedBox))

        #LUMP SUM 90%
        self.chaseLumpSum90Textbox.configure(state="normal")
        self.chaseLumpSum90Textbox.delete("0.0", "end")
        self.chaseLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.chaseLumpSum85Textbox.configure(state="normal")
        self.chaseLumpSum85Textbox.delete("0.0", "end")
        self.chaseLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.chaseLumpSum80Textbox.configure(state="normal")
        self.chaseLumpSum80Textbox.delete("0.0", "end")
        self.chaseLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.chaseLumpSum75Textbox.configure(state="normal")
        self.chaseLumpSum75Textbox.delete("0.0", "end")
        self.chaseLumpSum75Textbox.configure(state="disabled")
        
        #FINAL PAYMENT
        self.chaseFinalPaymentTextbox.configure(state="normal")
        self.chaseFinalPaymentTextbox.delete("0.0", "end")
        self.chaseFinalPaymentTextbox.configure(state="disabled") 
        
        #final pay date
        self.chaseLastPaymentDateTextbox.configure(state="normal")
        self.chaseLastPaymentDateTextbox.delete("0.0", "end")
        self.chaseLastPaymentDateTextbox.configure(state="disabled") 
        
        self.chaseSifExpirationDateTextbox.configure(state="normal")
        self.chaseSifExpirationDateTextbox.delete("0.0", "end")
        self.chaseSifExpirationDateTextbox.configure(state="disabled") 
        
        root.geometry('800x560')

        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error)
        
    def chasePrincipal(self):            
        value = self.chasePaymentVar.get()
        nrcValue = self.chaseNRCVar.get()
        
        if nrcValue == None or nrcValue == "":
            nrcValue = 0
        
        #ChasePrincipalTotal
        chaseNRCPrincipalTotal = float(value) + float(nrcValue)
        
        #LUMP SUM 90%
        chase90 = chaseNRCPrincipalTotal * .90
        self.chaseLumpSum90Textbox.configure(state="normal")
        self.chaseLumpSum90Textbox.delete("0.0", "end")
        self.chaseLumpSum90Textbox.insert(ctk.END, f"{chase90:.2f}")
        self.chaseLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        chase85 = chaseNRCPrincipalTotal * .85
        self.chaseLumpSum85Textbox.configure(state="normal")
        self.chaseLumpSum85Textbox.delete("0.0", "end")
        self.chaseLumpSum85Textbox.insert(ctk.END, f"{chase85:.2f}")
        self.chaseLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        chase80 = chaseNRCPrincipalTotal * .80
        self.chaseLumpSum80Textbox.configure(state="normal")
        self.chaseLumpSum80Textbox.delete("0.0", "end")
        self.chaseLumpSum80Textbox.insert(ctk.END, f"{chase80:.2f}")
        self.chaseLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        chase75 = chaseNRCPrincipalTotal * .75
        self.chaseLumpSum75Textbox.configure(state="normal")
        self.chaseLumpSum75Textbox.delete("0.0", "end")
        self.chaseLumpSum75Textbox.insert(ctk.END, f"{chase75:.2f}")
        self.chaseLumpSum75Textbox.configure(state="disabled")
    
    def chaseTab(self):
        
        # If no down payment entered then set to 0
        if self.chaseDownPaymentVar.get() == '':
            self.chaseDownPaymentVar.set(0)
        
        isZero = True
        if self.chaseNumberOfPaymentsVar.get() == '' or self.chaseNumberOfPaymentsVar.get() == '0':
            self.chaseNumberOfPaymentsVar.set(0)
        else:
            isZero = False
        
        if self.chaseMonthlyPaymentVar.get() == '':
            chaseMonthly = 0
        else:
            chaseMonthly = float(self.chaseMonthlyPaymentVar.get())
        
        if isZero == False and chaseMonthly != 0:
            messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
        
        isDateEntered = False
        if self.chaseFirstPaymentVar.get() != '' or chaseMonthly != 0:
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')
        
        isInitialPayment = False
        try:    
            if float(self.chaseDownPaymentVar.get()) == 0 or self.chaseDownPaymentVar.get() == None or self.chaseDownPaymentVar.get() == '':
                isInitialPayment = True
                self.chaseDownPaymentVar.set('')
            else:
                isInitialPayment = True
        
        except ValueError as dateError:
            print("this is the exception - ", dateError)
       
        #print("number of payements entered as int: ", int(self.chaseNumberOfPaymentsVar.get()))
        print("number of payements entered as default: ", "*", self.chaseNumberOfPaymentsVar.get(),"*")
        # try/except for number of payments entered or not
        try:
            
            if int(self.chaseNumberOfPaymentsVar.get()) > 60:
                isDateEntered = False
                messagebox.showinfo('Ras Negotiator', 'No more than 60 payments!')
        
            elif not int((self.chaseNumberOfPaymentsVar.get())) and chaseMonthly == 0:
                isDateEntered = False
                self.chaseNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
             
            else:
                isDateEntered = True
        except ValueError:
            print('value error')
        
        chaseFirstPaymentDate = self.chaseFirstPaymentVar.get()
        passedDate = chaseFirstPaymentDate
            
        # try/except for incorrect date format (more error handling)
        try:
            passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
        except ValueError:
            messagebox.showinfo('Ras Negotiator', f"{ValueError}\nFirst payment date should be in the format \'MM/DD/YYYY\'")    
            isDateEntered = False
        while isDateEntered and isInitialPayment:
            value = self.chasePaymentVar.get()
            nRcValue = self.chaseNRCVar.get()
            
            #SETTLEMENT AMOUNT
            chaseSettlementAmount = float(self.chaseSettlementVar.get())
            
            # try/except for empty downpayment box (chase)
            try:
                chaseDownPaymentAmount = float(self.chaseDownPaymentVar.get())
            except ValueError as error:
                chaseDownPaymentAmount = 0
                
            if chaseMonthly == 0:
                if chaseDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    chaseNumPayments = float(self.chaseNumberOfPaymentsVar.get())
                    
                    chaseSettlementAmount = chaseSettlementAmount - chaseDownPaymentAmount 
                    chasePaymentAmount = chaseSettlementAmount / chaseNumPayments
                
                    chaseRoundedPayment = round(chasePaymentAmount, 2)
                    chaseFinalPayment = chaseSettlementAmount - chaseRoundedPayment * (chaseNumPayments - 1)
                else:
                    chaseNumPayments = float(self.chaseNumberOfPaymentsVar.get())
                    chaseNumPayments -= 1
                    chaseSettlementAmount -= chaseDownPaymentAmount 
                    chasePaymentAmount = chaseSettlementAmount / chaseNumPayments
                
                    chaseRoundedPayment = round(chasePaymentAmount, 2)
                    chaseFinalPayment = chaseSettlementAmount - chaseRoundedPayment * (chaseNumPayments - 1)
            
            else:
                chaseSettlementAmount -= chaseDownPaymentAmount 
                chaseNumPayments = chaseSettlementAmount / float(chaseMonthly)
                roundedNumPayments = floor(chaseNumPayments)
                difNumPayments = chaseNumPayments - roundedNumPayments
                
                chaseRoundedPayment = chaseMonthly
                
                chaseFinalPayment = chaseRoundedPayment * difNumPayments
                
                chasePaymentAmount = chaseMonthly
                print(chaseFinalPayment, f'monthly {.15 * chaseMonthly}')
                
                if chaseFinalPayment > 0.15 * chaseMonthly:
                    roundedNumPayments += 1
                    chaseNumPayments += 1
                else:
                    chaseFinalPayment += chaseMonthly
                
                if roundedNumPayments > 16:
                    messagebox.showinfo('Ras Negotiator', f"No more than 16 payments for chase!\nPlease enter a larger payment!")  
                
            self.chaseFinalPaymentTextbox.configure(state="normal")
            self.chaseFinalPaymentTextbox.delete("0.0", "end")
            self.chaseFinalPaymentTextbox.insert(ctk.END, f"{chaseRoundedPayment:.2f}")
            self.chaseFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            date = datetime.datetime.strptime(chaseFirstPaymentDate, "%m/%d/%Y")
            
            # calculate new final date
            newDate_dt = date + relativedelta(months=int(chaseNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
            
            self.chaseLastPaymentDateTextbox.configure(state="normal")
            self.chaseLastPaymentDateTextbox.delete("0.0", "end")
            self.chaseLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.chaseLastPaymentDateTextbox.configure(state="disabled") 
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            chaseSifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.chaseSifExpirationDateTextbox.configure(state="normal")
            self.chaseSifExpirationDateTextbox.delete("0.0", "end")
            self.chaseSifExpirationDateTextbox.insert(ctk.END, f"{chaseSifExpirationDate}")
            self.chaseSifExpirationDateTextbox.configure(state="disabled")
            
            print("passedDate: ", passedDate)
            print("newDate: ", newDate)

            # Try/except to delete table when re-calculating
            isDateEntered = False
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
            
            chaseDownPayment = self.chaseDownPaymentVar.get()
            # Amortization Table function call for chase tab
            self.amortization_table_maker(passedDate, chasePaymentAmount, 
                                          newDate, chaseFinalPayment, 
                                          chaseNumPayments, chaseDownPayment,
                                          chaseSifExpirationDate)
    
    def citiOtherReset(self):
        #entry reset
        self.citiOtherPaymentVar.set("")
        self.citiOtherSettlementVar.set("")
        self.citiOtherDownPaymentVar.set("")
        self.citiOtherNumberOfPaymentsVar.set("")
        self.citiOtherFirstPaymentVar.set("MM/DD/YYYY")
        self.citiOtherMonthlyPaymentVar.set('')
        
        #clear date on left-click
        citiOtherFirstPaymentClear = self.citiOtherFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiOtherFirstPaymentEntry, citiOtherFirstPaymentClear))
        citiOtherMonthlyPaymentClickedBox = self.citiOtherMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiOtherMonthlyPaymentEntry, citiOtherMonthlyPaymentClickedBox))

        #Textbox reset
        #LUMP SUM 90%
        self.citiOtherLumpSum90Textbox.configure(state="normal")
        self.citiOtherLumpSum90Textbox.delete("0.0", "end")
        self.citiOtherLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.citiOtherLumpSum85Textbox.configure(state="normal")
        self.citiOtherLumpSum85Textbox.delete("0.0", "end")
        self.citiOtherLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.citiOtherLumpSum80Textbox.configure(state="normal")
        self.citiOtherLumpSum80Textbox.delete("0.0", "end")
        self.citiOtherLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.citiOtherLumpSum75Textbox.configure(state="normal")
        self.citiOtherLumpSum75Textbox.delete("0.0", "end")
        self.citiOtherLumpSum75Textbox.configure(state="disabled") 

        #SIF EXPIRATION DATE
        self.citiOtherSifExpirationDateTextbox.configure(state="normal")
        self.citiOtherSifExpirationDateTextbox.delete("0.0", "end")
        self.citiOtherSifExpirationDateTextbox.configure(state="disabled") 
        
        #FINAL PAYMENT
        self.citiOtherFinalPaymentTextbox.configure(state="normal")
        self.citiOtherFinalPaymentTextbox.delete("0.0", "end")
        self.citiOtherFinalPaymentTextbox.configure(state="disabled") 

        #LAST PAYMENT DATE
        self.citiOtherLastPaymentDateTextbox.configure(state="normal")
        self.citiOtherLastPaymentDateTextbox.delete("0.0", "end")
        self.citiOtherLastPaymentDateTextbox.configure(state="disabled") 

        root.geometry('800x560')
    
        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error)

    def citiOtherSettlement(self):
        value = self.citiOtherPaymentVar.get()
        
        #Total
        value = float(value)
        
        #LUMP SUM 90%
        citiOther90 = value * .90
        self.citiOtherLumpSum90Textbox.configure(state="normal")
        self.citiOtherLumpSum90Textbox.delete("0.0", "end")
        self.citiOtherLumpSum90Textbox.insert(ctk.END, f"{citiOther90:.2f}")
        self.citiOtherLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        citiOther85 = value * .85
        self.citiOtherLumpSum85Textbox.configure(state="normal")
        self.citiOtherLumpSum85Textbox.delete("0.0", "end")
        self.citiOtherLumpSum85Textbox.insert(ctk.END, f"{citiOther85:.2f}")
        self.citiOtherLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        citiOther80 = value * .80
        self.citiOtherLumpSum80Textbox.configure(state="normal")
        self.citiOtherLumpSum80Textbox.delete("0.0", "end")
        self.citiOtherLumpSum80Textbox.insert(ctk.END, f"{citiOther80:.2f}")
        self.citiOtherLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        citiOther75 = value * .75
        self.citiOtherLumpSum75Textbox.configure(state="normal")
        self.citiOtherLumpSum75Textbox.delete("0.0", "end")
        self.citiOtherLumpSum75Textbox.insert(ctk.END, f"{citiOther75:.2f}")
        self.citiOtherLumpSum75Textbox.configure(state="disabled")
        
    def citiOtherTab(self):
        
        # Set values to 0 if empty for data value manipulation and error handling
        if self.citiOtherDownPaymentVar.get() == '':
            self.citiOtherDownPaymentVar.set(0)
        
        isZero = True
        if self.citiOtherNumberOfPaymentsVar.get() == '' or self.citiOtherNumberOfPaymentsVar.get() == '0':
            self.citiOtherNumberOfPaymentsVar.set(0)
        else:
            isZero = False
            
        if self.citiOtherMonthlyPaymentVar.get() == '':
            citiMonthly = 0
        else:
            citiMonthly = float(self.citiOtherMonthlyPaymentVar.get())
        
        if isZero == False and citiMonthly != 0:
            messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
        
        
        # DATE VALIDATION
        isDateEntered = False
        isInitialPayment = False
        
        if(self.citiOtherFirstPaymentVar.get() != ''):
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')
        
        try:        
            if float(self.citiOtherDownPaymentVar.get()) == 0 or self.citiOtherDownPaymentVar.get() == None or self.citiOtherDownPaymentVar.get() == '':
                isInitialPayment = True
                self.citiOtherDownPaymentVar.set('')
            else:
                isInitialPayment = True 
        
        except ValueError as dateError:
            print("this is the exception - ", dateError)
        
        # try/except if number of payments entered or not(citiOther)
        try:
            if not int((self.citiOtherNumberOfPaymentsVar.get())) and citiMonthly == 0:
                isDateEntered = False
                self.cavalryNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
            else:
                    isDateEntered = True
        except ValueError:
            print('')
          
        while isDateEntered and isInitialPayment:
            value = self.citiOtherPaymentVar.get()
            
            #SETTLEMENT AMOUNT
            citiOtherSettlementAmount = float(self.citiOtherSettlementVar.get())
            
            # try/except for empty downpayment box (citiOther)
            try:
                citiOtherDownPaymentAmount = float(self.citiOtherDownPaymentVar.get())
            except ValueError as error:
                citiOtherDownPaymentAmount = 0
            
            citiOtherSettlementAmount = citiOtherSettlementAmount - citiOtherDownPaymentAmount
            
            if citiMonthly == 0:
                if citiOtherDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    citiOtherNumPayments = float(self.citiOtherNumberOfPaymentsVar.get())
                    citiOtherPaymentAmount = citiOtherSettlementAmount / citiOtherNumPayments              
                    
                    #FINAL PAYMENT
                    citiOtherRoundedPayment = round(citiOtherPaymentAmount, 2)
                    citiOtherFinalPayment = citiOtherSettlementAmount - citiOtherRoundedPayment * (citiOtherNumPayments - 1)
                else:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    citiOtherNumPayments = float(self.citiOtherNumberOfPaymentsVar.get())
                    citiOtherNumPayments -= 1
                    citiOtherPaymentAmount = citiOtherSettlementAmount / citiOtherNumPayments              
                    
                    #FINAL PAYMENT
                    citiOtherRoundedPayment = round(citiOtherPaymentAmount, 2)
                    citiOtherFinalPayment = citiOtherSettlementAmount - citiOtherRoundedPayment * (citiOtherNumPayments - 1)
                  
            else: 
                citiOtherNumPayments = citiOtherSettlementAmount / float(citiMonthly)
                roundedNumPayments = floor(citiOtherNumPayments)
                difNumPayments = citiOtherNumPayments - roundedNumPayments
                
                
                citiOtherRoundedPayment = citiMonthly
                
                citiOtherFinalPayment = citiOtherRoundedPayment * difNumPayments
                citiOtherPaymentAmount = citiMonthly
                
                if citiOtherFinalPayment > 0.15 * citiMonthly:
                    roundedNumPayments += 1
                    citiOtherNumPayments += 1
                else:
                    citiOtherFinalPayment += citiMonthly
                
                if roundedNumPayments > 60:
                    messagebox.showinfo('Ras Negotiator', f"No more than 60 payments for Citi-Other!\nPlease enter a larger payment!")  
            
            self.citiOtherFinalPaymentTextbox.configure(state="normal")
            self.citiOtherFinalPaymentTextbox.delete("0.0", "end")
            self.citiOtherFinalPaymentTextbox.insert(ctk.END, f"{citiOtherRoundedPayment:.2f}")
            self.citiOtherFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            # Get date from user and validate input
            citiOtherFirstPaymentDate = self.citiOtherFirstPaymentVar.get()
            passedDate = citiOtherFirstPaymentDate
        
            # try/except for incorrect date format (more error handling, citiOther)
            try:
                passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
            except ValueError:
                messagebox.showinfo('Ras Negotiator', f'{ValueError}\nPlease enter the date in the format of MM//DD/YYYY')
                
            date = datetime.datetime.strptime(citiOtherFirstPaymentDate, "%m/%d/%Y")    
            newDate_dt = date + relativedelta(months=int(citiOtherNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
            
            self.citiOtherLastPaymentDateTextbox.configure(state="normal")
            self.citiOtherLastPaymentDateTextbox.delete("0.0", "end")
            self.citiOtherLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.citiOtherLastPaymentDateTextbox.configure(state="disabled") 
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            citiOtherSifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.citiOtherSifExpirationDateTextbox.configure(state="normal")
            self.citiOtherSifExpirationDateTextbox.delete("0.0", "end")
            self.citiOtherSifExpirationDateTextbox.insert(ctk.END, f"{citiOtherSifExpirationDate}")
            self.citiOtherSifExpirationDateTextbox.configure(state="disabled")

            isDateEntered = False
            
            # Clear text box then call function
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
                

            citiOtherDownPayment = self.citiOtherDownPaymentVar.get()    
            self.amortization_table_maker(passedDate, citiOtherPaymentAmount, newDate, citiOtherFinalPayment, citiOtherNumPayments, citiOtherDownPayment, citiOtherSifExpirationDate)
    
    def citiMacyReset(self):
        #entry boxes reset
        self.citiMacysPaymentVar.set("")
        self.citiMacysSettlementVar.set("")
        self.citiMacysDownPaymentVar.set("")
        self.citiMacysNumberOfPaymentsVar.set("")
        self.citiMacysFirstPaymentVar.set("MM/DD/YYYY") 
        self.citiMacysMonthlyPaymentVar.set('')
        
        #clear date on left-click
        citiMacysFirstPaymentClear = self.citiMacysFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiMacysFirstPaymentEntry, citiMacysFirstPaymentClear))
        citiMacysMonthlyPaymentClickedBox = self.citiMacysMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.citiMacysMonthlyPaymentEntry, citiMacysMonthlyPaymentClickedBox))

        #text boxes reset
        #LUMP SUM 90%
        self.citiMacysLumpSum90Textbox.configure(state="normal")
        self.citiMacysLumpSum90Textbox.delete("0.0", "end")
        self.citiMacysLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.citiMacysLumpSum85Textbox.configure(state="normal")
        self.citiMacysLumpSum85Textbox.delete("0.0", "end")
        self.citiMacysLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.citiMacysLumpSum80Textbox.configure(state="normal")
        self.citiMacysLumpSum80Textbox.delete("0.0", "end")
        self.citiMacysLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.citiMacysLumpSum75Textbox.configure(state="normal")
        self.citiMacysLumpSum75Textbox.delete("0.0", "end")
        self.citiMacysLumpSum75Textbox.configure(state="disabled") 
        
        #FINAL PAYMENT
        self.citiMacysFinalPaymentTextbox.configure(state="normal")
        self.citiMacysFinalPaymentTextbox.delete("0.0", "end")
        self.citiMacysFinalPaymentTextbox.configure(state="disabled")
        
        #LAST PAYMENT DATE
        self.citiMacysLastPaymentDateTextbox.configure(state="normal")
        self.citiMacysLastPaymentDateTextbox.delete("0.0", "end")
        self.citiMacysLastPaymentDateTextbox.configure(state="disabled") 
        
        #SIF EXPIRATION DATE
        self.citiMacysSifExpirationDateTextbox.configure(state="normal")
        self.citiMacysSifExpirationDateTextbox.delete("0.0", "end")
        self.citiMacysSifExpirationDateTextbox.configure(state="disabled") 
        
        root.geometry('800x560')
    
        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error)
    
    def citiMacySettlement(self):
        value = self.citiMacysPaymentVar.get()
        
        #Total
        value = float(value)
        
        #LUMP SUM 90%
        citiMacys90 = value * .90
        self.citiMacysLumpSum90Textbox.configure(state="normal")
        self.citiMacysLumpSum90Textbox.delete("0.0", "end")
        self.citiMacysLumpSum90Textbox.insert(ctk.END, f"{citiMacys90:.2f}")
        self.citiMacysLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        citiMacys85 = value * .85
        self.citiMacysLumpSum85Textbox.configure(state="normal")
        self.citiMacysLumpSum85Textbox.delete("0.0", "end")
        self.citiMacysLumpSum85Textbox.insert(ctk.END, f"{citiMacys85:.2f}")
        self.citiMacysLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        citiMacys80 = value * .80
        self.citiMacysLumpSum80Textbox.configure(state="normal")
        self.citiMacysLumpSum80Textbox.delete("0.0", "end")
        self.citiMacysLumpSum80Textbox.insert(ctk.END, f"{citiMacys80:.2f}")
        self.citiMacysLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        citiMacys75 = value * .75
        self.citiMacysLumpSum75Textbox.configure(state="normal")
        self.citiMacysLumpSum75Textbox.delete("0.0", "end")
        self.citiMacysLumpSum75Textbox.insert(ctk.END, f"{citiMacys75:.2f}")
        self.citiMacysLumpSum75Textbox.configure(state="disabled")
    
    def citiMacyTab(self):
        
        # Set values to 0 if empty for data value manipulation and error handling
        isZero = True
        if self.citiMacysNumberOfPaymentsVar.get() == '' or self.citiMacysNumberOfPaymentsVar.get() == '0':
            self.citiMacysNumberOfPaymentsVar.set(0)
        else:
            isZero = False
        
        if self.citiMacysDownPaymentVar.get() == '':
            self.citiMacysDownPaymentVar.set(0)
        
        if self.citiMacysMonthlyPaymentVar.get() == '':
            citiMonthly = 0
            isLessThan12 = False
        else:
            citiMonthly = float(self.citiMacysMonthlyPaymentVar.get())
            isLessThan12 = True
        
        if isZero == False and citiMonthly != 0:
            messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
        
        isDateEntered = False
        isInitialPayment = False
        
        if(self.citiMacysFirstPaymentVar.get() != ''):
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')
        
        try:     
            if float(self.citiMacysDownPaymentVar.get()) == 0 or self.citiMacysDownPaymentVar.get() == None or self.citiMacysDownPaymentVar.get() == '':
                isInitialPayment = True  
                self.citiMacysDownPaymentVar.set('')
            else:
                isInitialPayment = True 
                
        except ValueError as dateError:
            print("this is the exception - ", dateError)
        
        # try/except if number of payments entered or not (citiMacys) 
        try:
            if(int(self.citiMacysNumberOfPaymentsVar.get()) <= 12):
                isLessThan12 = True
            elif not int((self.citiMacysNumberOfPaymentsVar.get())) and citiMonthly == 0:
                isDateEntered = False
                self.citiMacysNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
            else:
                messagebox.showinfo('Ras Negotiator', 'No more than 12 payments for Macys!')
        except ValueError:
            print('')
            
        while isDateEntered == True and isLessThan12 == True and isInitialPayment == True:
            value = self.citiMacysPaymentVar.get()
            
            #SETTLEMENT AMOUNT
            citiMacysSettlementAmount = float(self.citiMacysSettlementVar.get())
            
            # try/except for empty downpayment box (citiMacys)
            try:
                citiMacysDownPaymentAmount = float(self.citiMacysDownPaymentVar.get())
            except ValueError as error:
                citiMacysDownPaymentAmount = 0
                
            citiMacysSettlementAmount = citiMacysSettlementAmount - citiMacysDownPaymentAmount
            
            if citiMonthly == 0:
                if citiMacysDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    citiMacysNumPayments = float(self.citiMacysNumberOfPaymentsVar.get())
                    citiMacysPaymentAmount = citiMacysSettlementAmount / citiMacysNumPayments             
                    
                    #FINAL PAYMENT
                    citiMacysRoundedPayment = round(citiMacysPaymentAmount, 2)
                    citiMacysFinalPayment = citiMacysSettlementAmount - citiMacysRoundedPayment * (citiMacysNumPayments - 1)
                else:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    citiMacysNumPayments = float(self.citiMacysNumberOfPaymentsVar.get())
                    citiMacysNumPayments -= 1
                    citiMacysPaymentAmount = citiMacysSettlementAmount / citiMacysNumPayments             
                    
                    #FINAL PAYMENT
                    citiMacysRoundedPayment = round(citiMacysPaymentAmount, 2)
                    citiMacysFinalPayment = citiMacysSettlementAmount - citiMacysRoundedPayment * (citiMacysNumPayments - 1)
            
            else:
                citiMacysNumPayments = citiMacysSettlementAmount / float(citiMonthly)
                roundedNumPayments = floor(citiMacysNumPayments)
                difNumPayments = citiMacysNumPayments - roundedNumPayments
                
                
                citiMacysRoundedPayment = citiMonthly
                
                citiMacysFinalPayment = citiMacysRoundedPayment * difNumPayments
                citiMacysPaymentAmount = citiMonthly
                
                if citiMacysFinalPayment > 0.15 * citiMonthly:
                    roundedNumPayments += 1
                    citiMacysNumPayments += 1
                else:
                    citiMacysFinalPayment += citiMonthly
                
                if roundedNumPayments > 12:
                    messagebox.showinfo('Ras Negotiator', f"No more than 12 payments for Citi-Macys!\nPlease enter a larger payment!")  
                
            self.citiMacysFinalPaymentTextbox.configure(state="normal")
            self.citiMacysFinalPaymentTextbox.delete("0.0", "end")
            self.citiMacysFinalPaymentTextbox.insert(ctk.END, f"{citiMacysRoundedPayment:.2f}")
            self.citiMacysFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            citiMacysFirstPaymentDate = self.citiMacysFirstPaymentVar.get()
            
            # try/except for incorrect date format (more error handling, citiMacys)
            try:
                date = datetime.datetime.strptime(citiMacysFirstPaymentDate, "%m/%d/%Y")
            except ValueError:
                messagebox.showinfo('Ras Negotiator', f'{ValueError}\nPlease enter the date in the format of MM//DD/YYYY')
                
            newDate_dt = date + relativedelta(months=int(citiMacysNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
            
            self.citiMacysLastPaymentDateTextbox.configure(state="normal")
            self.citiMacysLastPaymentDateTextbox.delete("0.0", "end")
            self.citiMacysLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.citiMacysLastPaymentDateTextbox.configure(state="disabled") 
            
            passedDate = citiMacysFirstPaymentDate
            passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            citiMacysSifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.citiMacysSifExpirationDateTextbox.configure(state="normal")
            self.citiMacysSifExpirationDateTextbox.delete("0.0", "end")
            self.citiMacysSifExpirationDateTextbox.insert(ctk.END, f"{citiMacysSifExpirationDate}")
            self.citiMacysSifExpirationDateTextbox.configure(state="disabled")
            
            isDateEntered = False
            isLessThan12 = False

            # Clear text box then call function
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
            
            citiMacysDownPayment = self.citiMacysDownPaymentVar.get()     
            self.amortization_table_maker(passedDate, citiMacysPaymentAmount, newDate, citiMacysFinalPayment, citiMacysNumPayments, citiMacysDownPayment, citiMacysSifExpirationDate)
    
    def targetReset(self):
        #entry boxes reset
        self.targetPaymentVar.set("")
        self.targetSettlementVar.set("")
        self.targetDownPaymentVar.set("")
        self.targetNumberOfPaymentsVar.set("")
        self.targetFirstPaymentVar.set("MM/DD/YYYY")
        self.targetMonthlyPaymentVar.set('') 
        
        #clear date on left-click
        targetFirstPaymentClear = self.targetFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.targetFirstPaymentEntry, targetFirstPaymentClear))
        targetMonthlyPaymentClickedBox = self.targetMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.targetMonthlyPaymentEntry, targetMonthlyPaymentClickedBox))

        #text boxes reset
        #LUMP SUM 90%
        self.targetLumpSum90Textbox.configure(state="normal")
        self.targetLumpSum90Textbox.delete("0.0", "end")
        self.targetLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        self.targetLumpSum85Textbox.configure(state="normal")
        self.targetLumpSum85Textbox.delete("0.0", "end")
        self.targetLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        self.targetLumpSum80Textbox.configure(state="normal")
        self.targetLumpSum80Textbox.delete("0.0", "end")
        self.targetLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        self.targetLumpSum75Textbox.configure(state="normal")
        self.targetLumpSum75Textbox.delete("0.0", "end")
        self.targetLumpSum75Textbox.configure(state="disabled")
        
        #FINAL PAYMENT
        self.targetFinalPaymentTextbox.configure(state="normal")
        self.targetFinalPaymentTextbox.delete("0.0", "end")
        self.targetFinalPaymentTextbox.configure(state="disabled") 
        
        #LAST PAYMENT DATE
        self.targetLastPaymentDateTextbox.configure(state="normal")
        self.targetLastPaymentDateTextbox.delete("0.0", "end")
        self.targetLastPaymentDateTextbox.configure(state="disabled") 
        
        #SIF EXPIRATION DATE
        self.targetSifExpirationDateTextbox.configure(state="normal")
        self.targetSifExpirationDateTextbox.delete("0.0", "end")
        self.targetSifExpirationDateTextbox.configure(state="disabled") 
        
        root.geometry('800x560')
    
        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error)
    
    def targetSettlement(self):
        value = self.targetPaymentVar.get()
        
        #Total
        value = float(value)
        
        #LUMP SUM 90%
        target90 = value * .90
        self.targetLumpSum90Textbox.configure(state="normal")
        self.targetLumpSum90Textbox.delete("0.0", "end")
        self.targetLumpSum90Textbox.insert(ctk.END, f"{target90:.2f}")
        self.targetLumpSum90Textbox.configure(state="disabled")
        
        #LUMP SUM 85%
        target85 = value * .85
        self.targetLumpSum85Textbox.configure(state="normal")
        self.targetLumpSum85Textbox.delete("0.0", "end")
        self.targetLumpSum85Textbox.insert(ctk.END, f"{target85:.2f}")
        self.targetLumpSum85Textbox.configure(state="disabled")
        
        #LUMP SUM 80%
        target80 = value * .80
        self.targetLumpSum80Textbox.configure(state="normal")
        self.targetLumpSum80Textbox.delete("0.0", "end")
        self.targetLumpSum80Textbox.insert(ctk.END, f"{target80:.2f}")
        self.targetLumpSum80Textbox.configure(state="disabled")
        
        #LUMP SUM 75%
        target75 = value * .75
        self.targetLumpSum75Textbox.configure(state="normal")
        self.targetLumpSum75Textbox.delete("0.0", "end")
        self.targetLumpSum75Textbox.insert(ctk.END, f"{target75:.2f}")
        self.targetLumpSum75Textbox.configure(state="disabled")
    
    def targetTab(self):
        
        # Set values to 0 if empty for data value manipulation and error handling
        isZero = True
        if self.targetNumberOfPaymentsVar.get() == '' or self.targetNumberOfPaymentsVar.get() == '0':
            self.targetNumberOfPaymentsVar.set(0)
        else:
            isZero = False
        
        if self.targetDownPaymentVar.get() == '':
            self.targetDownPaymentVar.set(0)
        
        if self.targetMonthlyPaymentVar.get() == '':
            targetMonthly = 0
        else:
            targetMonthly = float(self.targetMonthlyPaymentVar.get())
        
        if isZero == False and targetMonthly != 0:
            messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
        
        isDateEntered = False
        isInitialPayment = False
        
        if(self.targetFirstPaymentVar.get() != ''):
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')
        
        try:        
            if float(self.targetDownPaymentVar.get()) == 0 or self.targetDownPaymentVar.get() == None or self.targetDownPaymentVar.get() == '':
                isInitialPayment = True
                self.targetDownPaymentVar.set('')
            else:
                isInitialPayment = True 
        except ValueError as dateError:
            print("this is the exception - ", dateError)
        
        # try/except if number of payments entered or not(target-TD)
        try:
            if not int((self.targetNumberOfPaymentsVar.get())) and targetMonthly == 0:
                isDateEntered = False
                self.targetNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
            else:
                    isDateEntered = True
        except ValueError:
            print('')
            
        while isDateEntered and isInitialPayment:
            value = self.targetPaymentVar.get()
            
            #SETTLEMENT AMOUNT
            targetSettlementAmount = float(self.targetSettlementVar.get())
            
            # try/except for empty downpayment box (chase)
            try:
                targetDownPaymentAmount = float(self.targetDownPaymentVar.get())
            except ValueError as error:
                targetDownPaymentAmount = 0
                
            targetSettlementAmount = targetSettlementAmount - targetDownPaymentAmount
            
            if targetMonthly == 0: 
                if targetDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    targetNumPayments = float(self.targetNumberOfPaymentsVar.get())
                    targetPaymentAmount = targetSettlementAmount / targetNumPayments              
                    
                    #FINAL PAYMENT
                    targetRoundedPayment = round(targetPaymentAmount, 2)
                    targetFinalPayment = targetSettlementAmount - targetRoundedPayment * (targetNumPayments - 1)
                else:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    targetNumPayments = float(self.targetNumberOfPaymentsVar.get())
                    targetNumPayments -= 1
                    targetPaymentAmount = targetSettlementAmount / targetNumPayments              
                    
                    #FINAL PAYMENT
                    targetRoundedPayment = round(targetPaymentAmount, 2)
                    targetFinalPayment = targetSettlementAmount - targetRoundedPayment * (targetNumPayments - 1)
                
            
            else:
                targetNumPayments = targetSettlementAmount / float(targetMonthly)
                roundedNumPayments = floor(targetNumPayments)
                difNumPayments = targetNumPayments - roundedNumPayments
                
                
                targetRoundedPayment = targetMonthly
                
                targetFinalPayment = targetRoundedPayment * difNumPayments
                targetPaymentAmount = targetMonthly
                
                if targetFinalPayment > 0.15 * targetMonthly:
                    roundedNumPayments += 1
                    targetNumPayments += 1
                else:
                    targetFinalPayment += targetMonthly
                
                if roundedNumPayments > 60:
                    messagebox.showinfo('Ras Negotiator', f"No more than 60 payments for Target!\nPlease enter a larger payment!")  
                    
            self.targetFinalPaymentTextbox.configure(state="normal")
            self.targetFinalPaymentTextbox.delete("0.0", "end")
            self.targetFinalPaymentTextbox.insert(ctk.END, f"{targetRoundedPayment:.2f}")
            self.targetFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            targetFirstPaymentDate = self.targetFirstPaymentVar.get()
            
            # try/except for incorrect date format (more error handling, target-TD)
            try:
                date = datetime.datetime.strptime(targetFirstPaymentDate, "%m/%d/%Y")
            except ValueError:
                messagebox.showinfo('Ras Negotiator', f'{ValueError}\nPlease enter the date in the format of MM//DD/YYYY')
                    
            newDate_dt = date + relativedelta(months=int(targetNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
            
            self.targetLastPaymentDateTextbox.configure(state="normal")
            self.targetLastPaymentDateTextbox.delete("0.0", "end")
            self.targetLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.targetLastPaymentDateTextbox.configure(state="disabled") 
            
            passedDate = targetFirstPaymentDate
            passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            targetSifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.targetSifExpirationDateTextbox.configure(state="normal")
            self.targetSifExpirationDateTextbox.delete("0.0", "end")
            self.targetSifExpirationDateTextbox.insert(ctk.END, f"{targetSifExpirationDate}")
            self.targetSifExpirationDateTextbox.configure(state="disabled")
            
            isDateEntered = False
            
            # Clear text box then call function
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
                
            targetDownPayment = self.targetDownPaymentVar.get() 
            self.amortization_table_maker(passedDate, targetPaymentAmount, newDate, targetFinalPayment, targetNumPayments, targetDownPayment, targetSifExpirationDate)
            
    def bqReset(self):
        #entry boxes reset
        self.bqPaymentVar.set("")
        self.bqDownPaymentVar.set("")
        self.bqNumberOfPaymentsVar.set("")
        self.bqFirstPaymentVar.set("MM/DD/YYYY")
        self.bqMonthlyPaymentVar.set('')
        
        #clear date on left-click
        bqFirstPaymentClear = self.bqFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.bqFirstPaymentEntry, bqFirstPaymentClear))
        bqMonthlyPaymentClickedBox = self.bqMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.bqMonthlyPaymentEntry, bqMonthlyPaymentClickedBox))

        #text boxes reset 
        #*ORIGINAL SETTLEMENT AMOUNT
        self.bqOriginalSettlementTextbox.configure(state="normal")
        self.bqOriginalSettlementTextbox.delete("0.0", "end")
        self.bqOriginalSettlementTextbox.configure(state="disabled")
        
        #SETTLEMENT AMOUNT
        self.bqSettlementTextbox.configure(state="normal")
        self.bqSettlementTextbox.delete("0.0", "end")
        self.bqSettlementTextbox.configure(state="disabled") 
        
        #FINAL PAYMENT
        self.bqFinalPaymentTextbox.configure(state="normal")
        self.bqFinalPaymentTextbox.delete("0.0", "end")
        self.bqFinalPaymentTextbox.configure(state="disabled") 
        
        #LAST PAYMENT DATE
        self.bqLastPaymentDateTextbox.configure(state="normal")
        self.bqLastPaymentDateTextbox.delete("0.0", "end")
        self.bqLastPaymentDateTextbox.configure(state="disabled") 
        
        #SIF EXPIRATION DATE
        self.bqSifExpirationDateTextbox.configure(state="normal")
        self.bqSifExpirationDateTextbox.delete("0.0", "end")
        self.bqSifExpirationDateTextbox.configure(state="disabled") 
        
        root.geometry('800x560')
    
        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error) 
    
    def bqTab(self):
        
        # Set values to 0 if empty for data value manipulation and error handling
        isZero = True
        if self.bqNumberOfPaymentsVar.get() == '' or self.bqNumberOfPaymentsVar.get() == '0':
            self.bqNumberOfPaymentsVar.set(0)
        else:
            isZero = False
            
        if self.bqDownPaymentVar.get() == '':
            self.bqDownPaymentVar.set(0)
        
        if self.bqMonthlyPaymentVar.get() == '':
            bqMonthly = 0
        else:
            bqMonthly = float(self.bqMonthlyPaymentVar.get())
        
        if isZero == False and bqMonthly != 0:
            messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
        
        
        value = self.bqPaymentVar.get()
        suitChoice = self.bqSuitVar.get()
        value = float(value)
        
        #Total
        isDateEntered = False
        isInitialPayment = False
        
        try:
            if float(self.bqDownPaymentVar.get()) == 0 or self.bqDownPaymentVar.get() == None or self.bqDownPaymentVar.get() == '':
                isInitialPayment = True  
                self.bqDownPaymentVar.set('')
            else:
                isInitialPayment = True 
        except ValueError as dateError:
            print("this is the exception - ", dateError)
        
        if(self.bqFirstPaymentVar.get() != ''):
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')
        
        # try/except if number of payments entered or not(bqBank)  
        try:
            if int(self.bqNumberOfPaymentsVar.get()) > 48:
                isDateEntered = False
                messagebox.showinfo('Ras Negotiator', 'No more than 48 payments!')
                
            elif not int((self.bqNumberOfPaymentsVar.get())) and bqMonthly == 0:
                isDateEntered = False
                self.bqNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
            else:
                isDateEntered = True
        except ValueError:
            print("")
        
        while isDateEntered and isInitialPayment:
            if suitChoice == 'PRE-SUIT':
                settlementVar = .60
            elif suitChoice == 'POST-SUIT':
                settlementVar = .75
            
            #*ORIGINAL SETTLEMENT AMOUNT
            bqOriginalSettlementAmount = value * settlementVar
            
            self.bqOriginalSettlementTextbox.configure(state="normal")
            self.bqOriginalSettlementTextbox.delete("0.0", "end")
            self.bqOriginalSettlementTextbox.insert(ctk.END, f"{bqOriginalSettlementAmount:.2f}")
            self.bqOriginalSettlementTextbox.configure(state="disabled")
            
            #SETTLEMENT AMOUNT
            # try/except for empty downpayment box (chase)
            try:  
                bqDownPaymentAmount = float(self.bqDownPaymentVar.get())
            except ValueError as error:
                bqDownPaymentAmount = 0
                
            bqSettlementAmount = bqOriginalSettlementAmount - bqDownPaymentAmount
            
            self.bqSettlementTextbox.configure(state="normal")
            self.bqSettlementTextbox.delete("0.0", "end")
            self.bqSettlementTextbox.insert(ctk.END, f"{bqSettlementAmount:.2f}")
            self.bqSettlementTextbox.configure(state="disabled")
            
            if bqMonthly == 0:
                if bqDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    bqNumPayments = float(self.bqNumberOfPaymentsVar.get())
                    bqPaymentAmount = bqSettlementAmount / bqNumPayments            
                    
                    #FINAL PAYMENT
                    bqRoundedPayment = round(bqPaymentAmount, 2)
                    bqFinalPayment = bqSettlementAmount - bqRoundedPayment * (bqNumPayments - 1)
                else:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    bqNumPayments = float(self.bqNumberOfPaymentsVar.get())
                    bqNumPayments -= 1
                    bqPaymentAmount = bqSettlementAmount / bqNumPayments            
                    
                    #FINAL PAYMENT
                    bqRoundedPayment = round(bqPaymentAmount, 2)
                    bqFinalPayment = bqSettlementAmount - bqRoundedPayment * (bqNumPayments - 1)
                  
            else:
                bqNumPayments = bqSettlementAmount / float(bqMonthly)
                roundedNumPayments = floor(bqNumPayments)
                difNumPayments = bqNumPayments - roundedNumPayments
                
                
                bqRoundedPayment = bqMonthly
                
                bqFinalPayment = bqRoundedPayment * difNumPayments
                bqPaymentAmount = bqMonthly
                
                if bqFinalPayment > 0.15 * bqMonthly:
                    roundedNumPayments += 1
                    bqNumPayments += 1
                else:
                    bqFinalPayment += bqMonthly
                
                if roundedNumPayments > 48:
                    messagebox.showinfo('Ras Negotiator', f"No more than 48 payments for BQ!\nPlease enter a larger payment!")  
                    
            self.bqFinalPaymentTextbox.configure(state="normal")
            self.bqFinalPaymentTextbox.delete("0.0", "end")
            self.bqFinalPaymentTextbox.insert(ctk.END, f"{bqRoundedPayment:.2f}")
            self.bqFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            bqFirstPaymentDate = self.bqFirstPaymentVar.get()
            
            # try/except for incorrect date format (more error handling, bqBank)
            try:
                date = datetime.datetime.strptime(bqFirstPaymentDate, "%m/%d/%Y")
            except ValueError:
                messagebox.showinfo('Ras Negotiator', f'{ValueError}\nPlease enter the date in the format of MM//DD/YYYY')
            newDate_dt = date + relativedelta(months=int(bqNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
            
            self.bqLastPaymentDateTextbox.configure(state="normal")
            self.bqLastPaymentDateTextbox.delete("0.0", "end")
            self.bqLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.bqLastPaymentDateTextbox.configure(state="disabled") 
            
            passedDate = bqFirstPaymentDate
            passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            bqSifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.bqSifExpirationDateTextbox.configure(state="normal")
            self.bqSifExpirationDateTextbox.delete("0.0", "end")
            self.bqSifExpirationDateTextbox.insert(ctk.END, f"{bqSifExpirationDate}")
            self.bqSifExpirationDateTextbox.configure(state="disabled")
            
            isDateEntered = False
            
            # Clear text box then call function
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
            
            bqDownPayment = self.bqDownPaymentVar.get() 
            self.amortization_table_maker(passedDate, bqPaymentAmount, newDate, bqFinalPayment, bqNumPayments, bqDownPayment, bqSifExpirationDate)
            
    def cavalryReset(self):
        #entry boxes reset
        self.cavalryPaymentVar.set("")
        self.cavalrySettlementVar.set("")
        self.cavalryDownPaymentVar.set("")
        self.cavalryNumberOfPaymentsVar.set("")
        self.cavalryMonthlyPaymentVar.set('')
        self.cavalryFirstPaymentVar.set("MM/DD/YYYY") 
        
        #clear date on left-click
        cavalryFirstPaymentClear = self.cavalryFirstPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.cavalryFirstPaymentEntry, cavalryFirstPaymentClear))
        cavalryMonthlyPaymentClickedBox = self.cavalryMonthlyPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(self.cavalryMonthlyPaymentEntry, cavalryMonthlyPaymentClickedBox))

        #text boxes reset
        #lump sum 85%
        self.cavalryLumpSum85Textbox.configure(state="normal")
        self.cavalryLumpSum85Textbox.delete("0.0", "end")
        self.cavalryLumpSum85Textbox.configure(state="disabled")   
        
        #FINAL PAYMENT
        self.cavalryFinalPaymentTextbox.configure(state="normal")
        self.cavalryFinalPaymentTextbox.delete("0.0", "end")
        self.cavalryFinalPaymentTextbox.configure(state="disabled")  
        
        #LAST PAYMENT DATE
        self.cavalryLastPaymentDateTextbox.configure(state="normal")
        self.cavalryLastPaymentDateTextbox.delete("0.0", "end")
        self.cavalryLastPaymentDateTextbox.configure(state="disabled") 
        
        #SIF EXPIRATION DATE
        self.cavalrySifExpirationDateTextbox.configure(state="normal")
        self.cavalrySifExpirationDateTextbox.delete("0.0", "end")
        self.cavalrySifExpirationDateTextbox.configure(state="disabled")
        
        root.geometry('800x560')
    
        try:
            textbox.destroy()
            deliveryType.destroy()
            contactType.destroy()
            contactEntryBox.destroy()
            taxType.destroy()
            termsChoice.destroy()
            addButton.destroy()
            
        except Exception as error:
            print(error) 
    
    def cavalryPrincipal(self):
        value = self.cavalryPaymentVar.get()
        
        #LUMP SUM 85%
        try:
            cavalry85 = int(value) * .85
        except Exception as error:
            cavalry85 = float(value) * .85
            
        self.cavalryLumpSum85Textbox.configure(state="normal")
        self.cavalryLumpSum85Textbox.delete("0.0", "end")
        self.cavalryLumpSum85Textbox.insert(ctk.END, f"{cavalry85:.2f}")
        self.cavalryLumpSum85Textbox.configure(state="disabled")
    
    def cavalryTab(self):
        
        # Set values to 0 if empty for data value manipulation and error handling
        isZero = True
        if self.cavalryNumberOfPaymentsVar.get() == '' or self.cavalryNumberOfPaymentsVar.get() == '0':
            self.cavalryNumberOfPaymentsVar.set(0)
        else:
            isZero = False
        
        if self.cavalryDownPaymentVar.get() == '':
            self.cavalryDownPaymentVar.set(0)
            
        if self.cavalryMonthlyPaymentVar.get() == '':
            cavalryMonthly = 0
        else:
            cavalryMonthly = float(self.cavalryMonthlyPaymentVar.get())    
    
        if isZero == False and cavalryMonthly != 0:
                messagebox.showinfo('Ras Negotiator', 'Calculating Based off Custom Monthly Payment!')
    
        value = self.cavalryPaymentVar.get()
        value = float(value)

        #Total
        isDateEntered = False
        isInitialPayment = False
        
        if(self.cavalryFirstPaymentVar.get() != ''):
            isDateEntered = True
        else:
            messagebox.showinfo('Ras Negotiator', 'Please enter the first payment date!')

        try:      
            if float(self.cavalryDownPaymentVar.get()) == 0 or self.cavalryDownPaymentVar.get() == None or self.cavalryDownPaymentVar.get() == '':
                isInitialPayment = True 
                self.cavalryDownPaymentVar.set('')
            else:
                isInitialPayment = True 
        except ValueError as dateError:
            print("this is the exception - ", dateError)

        # try/except if number of payments entered or not (cavalry)
        try:    
            if int(self.cavalryNumberOfPaymentsVar.get()) > 24:
                isDateEntered = False
                messagebox.showinfo('Ras Negotiator', 'No more than 24 payments!')
                
            elif not int((self.cavalryNumberOfPaymentsVar.get())) and cavalryMonthly == 0:
                isDateEntered = False
                self.cavalryNumberOfPaymentsVar.set('')
                messagebox.showinfo('Ras Negotiator', 'Please enter the number of payments!')
            
            else:
                isDateEntered = True
        except ValueError:
           print('')
        
        while isDateEntered and isInitialPayment:
            
            #*ORIGINAL SETTLEMENT AMOUNT
            value = float(self.cavalrySettlementVar.get())
            
            #SETTLEMENT AMOUNT
            # try/except for empty downpayment box (chase)
            try:
                cavalryDownPaymentAmount = float(self.cavalryDownPaymentVar.get())
            except ValueError as error:
                cavalryDownPaymentAmount = 0
                
            cavalrySettlementAmount = value - cavalryDownPaymentAmount
            
            if cavalryMonthly == 0:
                if cavalryDownPaymentAmount == 0:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    cavalryNumPayments = float(self.cavalryNumberOfPaymentsVar.get())
                    cavalryPaymentAmount = cavalrySettlementAmount / cavalryNumPayments            
                    
                    #FINAL PAYMENT
                    cavalryRoundedPayment = round(cavalryPaymentAmount, 2)
                    cavalryFinalPayment = cavalrySettlementAmount - cavalryRoundedPayment * (cavalryNumPayments - 1)
                else:
                    #PAYMENT AMOUNT (BIF OVER PAYS)
                    cavalryNumPayments = float(self.cavalryNumberOfPaymentsVar.get())
                    cavalryNumPayments -= 1
                    cavalryPaymentAmount = cavalrySettlementAmount / cavalryNumPayments            
                    
                    #FINAL PAYMENT
                    cavalryRoundedPayment = round(cavalryPaymentAmount, 2)
                    cavalryFinalPayment = cavalrySettlementAmount - cavalryRoundedPayment * (cavalryNumPayments - 1)
                
            else:
                cavalryNumPayments = cavalrySettlementAmount / float(cavalryMonthly)
                roundedNumPayments = floor(cavalryNumPayments)
                difNumPayments = cavalryNumPayments - roundedNumPayments
                
                cavalryRoundedPayment = cavalryMonthly
                
                cavalryFinalPayment = cavalryRoundedPayment * difNumPayments
                cavalryPaymentAmount = cavalryMonthly
                
                if cavalryFinalPayment > 0.15 * cavalryMonthly:
                    roundedNumPayments += 1
                    cavalryNumPayments += 1
                else:
                    cavalryFinalPayment += cavalryMonthly
                
                if roundedNumPayments > 24:
                    messagebox.showinfo('Ras Negotiator', f"No more than 24 payments for Cavalry!\nPlease enter a larger payment!")  
                    
                
            self.cavalryFinalPaymentTextbox.configure(state="normal")
            self.cavalryFinalPaymentTextbox.delete("0.0", "end")
            self.cavalryFinalPaymentTextbox.insert(ctk.END, f"{cavalryRoundedPayment:.2f}")
            self.cavalryFinalPaymentTextbox.configure(state="disabled") 
            
            #LAST PAYMENT DATE
            today = datetime.date.today()
            year = today.year
            
            cavalryFirstPaymentDate = self.cavalryFirstPaymentVar.get()
            
            # try/except for incorrect date format (more error handling)
            try:
                date = datetime.datetime.strptime(cavalryFirstPaymentDate, "%m/%d/%Y")
            except ValueError:
                messagebox.showinfo('Ras Negotiator', f'{ValueError}\nPlease enter the date in the format of MM//DD/YYYY')
                
            newDate_dt = date + relativedelta(months=int(cavalryNumPayments) - 1)
            newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")

            self.cavalryLastPaymentDateTextbox.configure(state="normal")
            self.cavalryLastPaymentDateTextbox.delete("0.0", "end")
            self.cavalryLastPaymentDateTextbox.insert(ctk.END, f"{newDate}")
            self.cavalryLastPaymentDateTextbox.configure(state="disabled") 
            
            passedDate = cavalryFirstPaymentDate
            passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
            
            # SIF Expiration Date contents (chase)
            newDate_dtObj = newDate_dt + relativedelta(days=10)
            cavalrySifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
            
            self.cavalrySifExpirationDateTextbox.configure(state="normal")
            self.cavalrySifExpirationDateTextbox.delete("0.0", "end")
            self.cavalrySifExpirationDateTextbox.insert(ctk.END, f"{cavalrySifExpirationDate}")
            self.cavalrySifExpirationDateTextbox.configure(state="disabled")
            
            isDateEntered = False
            
            # Clear text box then call function
            try:
                textbox.destroy()
                deliveryType.destroy()
                contactType.destroy()
                contactEntryBox.destroy()
                taxType.destroy()
                termsChoice.destroy()
                addButton.destroy()
                
            except Exception as error:
                print("textbox clear error - ", error)
                
            cavalryDownPayment = self.cavalryDownPaymentVar.get() 
            
            self.amortization_table_maker(passedDate, cavalryPaymentAmount, newDate, cavalryFinalPayment, cavalryNumPayments, cavalryDownPayment, cavalrySifExpirationDate)

    # Date validator function
    def validate_date(self, d):
        try:
            if len(d) == 10: 
                datetime.datetime.strptime(d, '%m/%d/%Y')
                return True
            else: 
                return False

        except ValueError:
            messagebox.showinfo('Ras Negotiator', 'Date must be in format MM/DD/YYYY')
            return False       
        
    def amortization_table_maker(self, first_payment_date, first_monthly_payment, last_payment_date, 
                                 last_monthly_payment, total_payments, downPayment,
                                 sif_expiration_date):
 
        # Date conversion logic for proper formatting
        first_payment_date = datetime.datetime.strftime(first_payment_date, '%Y-%m-%d')
        first_payment_date = datetime.datetime.strptime(first_payment_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        first_payment_date = datetime.datetime.strptime(first_payment_date, '%m/%d/%Y').date()
        
        bank_num_payments = total_payments 
        
        # run calculations
        self.backend_table_calculations(first_payment_date, first_monthly_payment, last_payment_date,
                                        last_monthly_payment, bank_num_payments, downPayment,
                                        sif_expiration_date)

    # Backend logic that returns "amortization_table" variable
    def backend_table_calculations(self, first_payment_date, first_monthly_payment, 
                                   last_payment_date, last_monthly_payment, 
                                   bank_num_payments, downPayment, sif_expiration_date):
        
        if downPayment == '0' or downPayment == '':
            self.downPayment = 0
        else:
            self.downPayment = downPayment
            
        self.first_payment_date = first_payment_date
        self.first_monthly_payment = first_monthly_payment
        self.last_monthly_payment = last_monthly_payment
        self.bank_num_payments = bank_num_payments
        self.last_payment_date = last_payment_date
        self.sif_expiration_date = sif_expiration_date
        
        # First date displayed in table
        self.formatted_first_date = first_payment_date
        self.formatted_first_date = self.formatted_first_date.strftime("%m/%d/%Y")
        
        # Call table window and (re-)initialize textbox
        self.tableWindow()
        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        user = os.getlogin()
        self.totalPayments = 0
        # Display header row, first date, monthly paymens
        textbox.insert(ctk.END, "Payment Dates\t\tMonthly Payments") 
        textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        
        if self.downPayment == 0 or self.downPayment == None or self.downPayment == '':
            self.downPayment = 0       
            self.first_monthly_payment = round(first_monthly_payment, 2)
            self.last_monthly_payment = round(last_monthly_payment, 2)
            self.finalPayment = 0.0
            self.finalPayment += self.downPayment
            textbox.insert(ctk.END, f"\n1. {self.formatted_first_date}\t\t\t${self.last_monthly_payment:.2f}")
            self.totalPayments += 1
            self.finalPayment += float(self.first_monthly_payment)
        
            # for loop through num of payments
            for i in range(1, (int(self.bank_num_payments - 1))):
                self.totalPayments += 1
                # if there is only one payment
                if int(self.bank_num_payments == 0):
                    break
                
                # calculate next payment date, increment to next month
                self.next_payment_date = self.first_payment_date + relativedelta(months=int(i))
                self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
                
                # Display next payment dates in text box
                textbox.insert(ctk.END, f"\n{i + 1}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}") 
                self.finalPayment += float(self.first_monthly_payment)
                
                # Display last payment date in list and first/last payments in footer
                # if bank payments is more than one, display last payment (last payment not needed if only one payment)
            self.next_payment_date = self.first_payment_date + relativedelta(months=int(self.bank_num_payments - 1))
            self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
            if int(self.bank_num_payments) != 1:
                self.totalPayments += 1
                textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments)))}. {self.last_payment_date}\t\t\t${self.first_monthly_payment:.2f}")
                self.finalPayment += float(self.last_monthly_payment)
                pass
        else:
            self.downPayment = float(self.downPayment)
            
            self.first_monthly_payment = round(first_monthly_payment, 2)
            self.last_monthly_payment = round(last_monthly_payment, 2)
            self.finalPayment = 0.0
            self.finalPayment += self.downPayment
            
            self.next_payment_date = self.first_payment_date + relativedelta(months=int(1))
            self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
            
            textbox.insert(ctk.END, f"\n1. {self.formatted_first_date}\t\t\t${self.downPayment:.2f}")
            textbox.insert(ctk.END, f"\n2. {self.next_payment_date}\t\t\t${self.last_monthly_payment:.2f}") 
            self.totalPayments += 2
            self.finalPayment += float(self.first_monthly_payment)
        
            # for loop through num of payments
            for i in range(1, (int(self.bank_num_payments - 1))):
                self.totalPayments += 1
                # if there is only one payment
                if int(self.bank_num_payments == 0):
                    break
                
                # calculate next payment date, increment to next month
                self.next_payment_date = self.first_payment_date + relativedelta(months=int(i + 1))
                self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
                
                # Display next payment dates in text box
                textbox.insert(ctk.END, f"\n{i + 2}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}") 
                self.finalPayment += float(self.first_monthly_payment)  
        
            # Display last payment date in list and first/last payments in footer
                # if bank payments is more than one, display last payment (last payment not needed if only one payment)
            self.next_payment_date = self.first_payment_date + relativedelta(months=int(self.bank_num_payments))
            self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
            if int(self.bank_num_payments) != 1:
                self.totalPayments += 1
                textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments) + 1))}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}")
                self.finalPayment += float(self.last_monthly_payment)
                pass

        self.sif_expiration_date = self.first_payment_date + relativedelta(months=int(self.totalPayments - 1))
        self.sif_expiration_date = self.sif_expiration_date + relativedelta(days=int(10))
        self.sif_expiration_date = datetime.datetime.strftime(self.sif_expiration_date, "%m/%d/%Y")
        
        textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        
        if self.downPayment:
            textbox.insert(ctk.END, f"\nFirst payment:\t\t\t${self.downPayment:.2f}")
        elif not self.downPayment:
            textbox.insert(ctk.END, f"\nFirst payment:\t\t\t${self.last_monthly_payment:.2f}")
        
        textbox.insert(ctk.END, f"\nLast payment:\t\t\t${self.first_monthly_payment:.2f}")
        textbox.insert(ctk.END, f"\nTotal Payment:\t\t\t${self.finalPayment:.2f}")
        textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        textbox.insert(ctk.END, f"\nFirst Payment Date:\t\t\t{self.formatted_first_date}")
        textbox.insert(ctk.END, f"\nLast Payment Date:\t\t\t{self.next_payment_date}")
        
        textbox.insert(ctk.END, f"\nSIF Expiration Date:\t\t\t{self.sif_expiration_date}")
        textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        textbox.insert(ctk.END, f"\nRESPONSIBLE: {user}")
        textbox.configure(state="disabled")     
        
    # Function to clear entry box on left-click 
    def clearEntryOnclick(self, event, clicked):
        event.configure(state='normal')
        event.delete(0, 'end')
        event.unbind('<Button-1>', clicked)
        
    # Function for table window creation       
    def tableWindow(self):
        try:
            root.geometry("800x800")
            currentTab = self.get()

            # Initialize textbox container for amortization table
            global textbox, deliveryType, contactType, contactEntryBox, taxType, termsChoice, addButton, deliveryVar, contactVar, contactEntryVar, taxVar, termsVar
            textbox = ctk.CTkTextbox(self.tab(currentTab), width=600, height=200)
            textbox.pack(side='bottom', anchor='sw', pady=5,padx=5)
            textbox.configure(state="disabled")
            
            # Delivery type box - BIF, PPA, SIF
            deliveryVar = ctk.StringVar()
            deliveryType = ctk.CTkOptionMenu(self.tab(currentTab), variable=deliveryVar, values=['BIF', 'PPA', 'SIF'])
            deliveryType.pack(side='left', anchor='n', pady=5, padx=5)
            deliveryVar.set('Payment Type')
            
            # Contact type box - Email, Mail, Fax, E-Sign
            contactVar = ctk.StringVar()
            contactType = ctk.CTkOptionMenu(self.tab(currentTab), variable=contactVar, values=['Email', 'Mail','Fax','E-Sign'])
            contactType.pack(side='left', anchor='n', pady=5, padx=5)
            contactVar.set('Delivery Method')
           
            # Method of contact box, user entered information
            contactEntryVar = ctk.StringVar()
            contactEntryBox = ctk.CTkEntry(self.tab(currentTab), textvariable=contactEntryVar)
            contactEntryBox.pack(side='left', anchor='n', pady=5, padx=5)
            contactEntryVar.set('Enter Details')
            clickedBox = contactEntryBox.bind('<Button-1>', lambda event: self.clearEntryOnclick(contactEntryBox, clickedBox))
            
            # 1099 - Provided box - Yes, No
            taxVar = ctk.StringVar()
            taxType = ctk.CTkOptionMenu(self.tab(currentTab), variable=taxVar, values=['Yes', 'No'])
            taxType.pack(side='left', anchor='n', pady=5, padx=8)
            taxVar.set('1099 - Provided')
            
            # Payment terms box - Weekly, Bi-Weekly, Monthly
            termsVar = ctk.StringVar()
            termsChoice = ctk.CTkOptionMenu(self.tab(currentTab), variable=termsVar, values=['Weekly','Bi-Weekly','Monthly'])
            termsChoice.pack(side='left', anchor='n', pady=5, padx=8)
            termsVar.set('Terms')
            
            # Add to table button
            addButton = ctk.CTkButton(self.tab(currentTab), text='Add to Table', command=lambda:self.addToTable())
            addButton.place(x=615, y=480)
            
            global pressedCounter
            pressedCounter = 0
            
        except Exception as error:
            print(error)
          
    def addToTable(self):
        
        # Counter to check if function has been run
        global pressedCounter
        date=''
        date = datetime.datetime.today().strftime('%m/%d/%Y')
        # If function has not been run, display contents
        if pressedCounter == 0:
            textbox.configure(state="normal")  
            textbox.insert(ctk.END, f"\nBALANCE: ${self.finalPayment:.2f}")
            textbox.insert(ctk.END, f"\nPAYMENT TYPE: {deliveryVar.get()}")
            
            if self.downPayment == 0:
                textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments} {termsVar.get()} payments with the first payment of ${self.last_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and the final payment of ${self.first_monthly_payment:.2f} ending on {self.next_payment_date}"))         
            else:
                textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, a payment of "
                                        f"${self.last_monthly_payment:.2f}, and then {self.totalPayments - 2}\npayments of ${self.first_monthly_payment:.2f}"))
                    
            textbox.insert(ctk.END, f"\nDELIVERY TYPE: {contactVar.get()}: {contactEntryVar.get()}")
            textbox.insert(ctk.END, f"\n1099 C GIVEN: {taxVar.get()}")
            textbox.insert(ctk.END, f"\nRECAP: Consumer VERBALLY AGREED TO THE ABOVE TERMS ON ({date})")
            textbox.configure(state="disabled")  
            pressedCounter += 1
        
        # If function has been run, clear previous contents (last 7 lines) and display contents
        elif pressedCounter == 1:
            textbox.configure(state="normal")  
            textbox.delete("end-7l", "end")
            textbox.insert(ctk.END, f"\nBALANCE: ${self.finalPayment:.2f}")
            textbox.insert(ctk.END, f"\nPAYMENT TYPE: {deliveryVar.get()}")
            
            if self.downPayment == 0:
                textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments} {termsVar.get()} payments with the first payment of ${self.last_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and the final payment of ${self.first_monthly_payment:.2f} ending on {self.next_payment_date}"))         
            else:
                textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, a payment of "
                                        f"${self.last_monthly_payment:.2f}, and then {self.totalPayments - 2}\npayments of ${self.first_monthly_payment:.2f}"))
                    
            textbox.insert(ctk.END, f"\nDELIVERY TYPE: {contactVar.get()}: {contactEntryVar.get()}")
            textbox.insert(ctk.END, f"\n1099 C GIVEN: {taxVar.get()}")
            textbox.insert(ctk.END, f"\nRECAP: Consumer VERBALLY AGREED TO THE ABOVE TERMS ON ({date})")
            textbox.configure(state="disabled")
        
class CalculatorGui(ctk.CTk):    

    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
       
        self.title("RAS Negotiator") 
        
        window_width = 800
        window_height = 560
 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.resizable(False, False)
        
        datafile2 = "logo.png"
        if not hasattr(sys, "frozen"):
            datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
        else:
            datafile2 = os.path.join(sys.prefix, datafile2)
        image= ctk.CTkImage(Image.open(datafile2), size=(150,85))
        self.img_label = ctk.CTkLabel(self, image=image, text="")
        self.img_label.pack()
        
        self.tab_view = MyTabView(master=self, command=lambda:resetSize(self))
        self.tab_view.pack(expand=True, fill='both')

def resetSize(self):
    self.geometry('800x560')
    
    try:
        textbox.destroy()
        deliveryType.destroy()
        contactType.destroy()
        contactEntryBox.destroy()
        taxType.destroy()
        termsChoice.destroy()
        addButton.destroy()
    except Exception as error:
        print(error, ": Tried Resetting Geometry")
    
if __name__ == "__main__":
    root = CalculatorGui()
    root.mainloop()
import datetime
import os
import sys
from PIL import Image
import customtkinter as ctk
from PIL import ImageTk
from dateutil.relativedelta import relativedelta
from numpy import floor

class CalculatorGui(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("RAS Negotiator v25") 
        
        window_width = 1025
        window_height = 700
 
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate - 50))
        self.resizable(False, False)
        
        self.logo = "logo.png"
        if not hasattr(sys, "frozen"):
            self.logo = os.path.join(os.path.dirname(__file__), self.logo)
        else:
            self.logo = os.path.join(sys.prefix, self.logo)
        self.image= ctk.CTkImage(Image.open(self.logo), size=(150,85))
        self.img_label = ctk.CTkLabel(self, image=self.image, text="")
        self.img_label.pack()

        self.img_label.bind("<Button-1>", lambda event: self.easterEgg())
        self.easterEggCount = 0

        self.bankOption = ctk.CTkSegmentedButton(self, values=['CHASE', "CITIBANK-OTHER", 'CITIBANK-MACYS','TARGET-TD','BQ','CAVALRY'], command=self.setBank)
        self.bankOption.pack(side= 'top', pady=5)
        self.bankOption.set('CHASE')

        self.textbox = ctk.CTkTextbox(self, width=1025, height=200)
        self.textbox.pack(side='bottom')

        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill='both',expand='true')

        # Delivery type box - BIF, PPA, SIF
        self.deliveryVar = ctk.StringVar()
        deliveryType = ctk.CTkOptionMenu(self, variable=self.deliveryVar, values=['BIF', 'PPA', 'SIF'])
        deliveryType.pack(side='left', anchor='n', padx=3, pady=3)
        self.deliveryVar.set('Payment Type')
        
        # Contact type box - Email, Mail, Fax, E-Sign
        self.contactVar = ctk.StringVar()
        contactType = ctk.CTkOptionMenu(self, variable=self.contactVar, values=['Email', 'Mail','Fax','E-Sign'], command=self.setContactEntry)
        contactType.pack(side='left', anchor='n', padx=3, pady=3)
        self.contactVar.set('Delivery Method')
        
        # Method of contact box, user entered information
        self.contactEntryVar = ctk.StringVar()
        contactEntryBox = ctk.CTkEntry(self, textvariable=self.contactEntryVar)
        contactEntryBox.pack(side='left', anchor='n', padx=3, pady=3)
        self.contactEntryVar.set('Enter Details')
        contactEntryBox.bind('<Button-1>', lambda event: self.clearTableEntry(contactEntryBox))
        
        # 1099 - Provided box - Yes, No
        self.taxVar = ctk.StringVar()
        taxType = ctk.CTkOptionMenu(self, variable=self.taxVar, values=['Yes', 'No'])
        taxType.pack(side='left', anchor='n', padx=3, pady=3)
        self.taxVar.set('1099 - Provided')
        
        # Payment terms box - Weekly, Bi-Weekly, Monthly
        self.termsVar = ctk.StringVar()
        termsChoice = ctk.CTkOptionMenu(self, variable=self.termsVar, values=['Weekly','Bi-Weekly','Monthly'])
        termsChoice.pack(side='left', anchor='n', padx=3, pady=3)
        self.termsVar.set('Terms')
        
        #Set the agreement line at the end of the textbox
        self.verbalAgreement = ctk.StringVar()
        verbalChoice = ctk.CTkOptionMenu(self, variable=self.verbalAgreement, values=['CONSUMER','DMC'])
        verbalChoice.pack(side='left', anchor='n', padx=3, pady=3)
        self.verbalAgreement.set('RECAP')
        
        # Add to table button
        addButton = ctk.CTkButton(self, text='Add to Table', command=lambda:self.addToTable())
        addButton.pack(side='left', anchor='n', padx=3, pady=3)
        
        self.setBank('CHASE')

    def setBank(self, value):
        try:
            self.destroy_widgets()
        except:
            print('No Widgets')

        self.bankOption = value

        if self.bankOption == 'CHASE':
            self.maxPayments = 60

        elif self.bankOption == 'CITIBANK-OTHER':
            self.maxPayments = 60

        elif self.bankOption == 'CITIBANK-MACYS':
            self.maxPayments = 60

        elif self.bankOption == 'TARGET-TD':
            self.maxPayments = 60

        elif self.bankOption == 'BQ':
            self.maxPayments = 48

        elif self.bankOption == 'CAVALRY':
            self.maxPayments = 24
        
        self.setGui()
    
    def destroy_widgets(self):
        # Destroy all widgets on self.mainFrame
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        # Clear the main textbox
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")

    def clearEntryOnclick(self, event):
        event.configure(state='normal')
        event.delete(0, 'end')

    def clearTableEntry(self, event):
        event.configure(state='normal')
        event.delete(0, 'end')

    def setGui(self):
        if self.bankOption == 'BQ':
            #PRESUIT--POSTSUIT OptionMenu
            self.bqSuitVar = ctk.StringVar()
            bqSuitOption = ctk.CTkOptionMenu(self.mainFrame, values=['PRE-SUIT', 'POST-SUIT'], variable=self.bqSuitVar)
            bqSuitOption.grid(row=0, column=1, pady=5, padx=5)
            bqSuitOption.set('PRE-SUIT')
            
            # Label for Account Balance
            accountBalanceLabel = ctk.CTkLabel(self.mainFrame, text='*Account Balance:')
            accountBalanceLabel.grid(row=1, column=0, padx=5, pady=10)

            # Account Balance Value Stored Here self.accountBalance.get()
            self.accountBalance = ctk.StringVar()
            accountBalanceEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.accountBalance)
            accountBalanceEntry.grid(row=1, column=1,padx=5, pady=10)
            accountBalanceEntry.bind('<KeyRelease>', self.calculateLumpSum)
            accountBalanceEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(accountBalanceEntry))
        
        else:
            # Label for Account Balance
            accountBalanceLabel = ctk.CTkLabel(self.mainFrame, text='*Account Balance:')
            accountBalanceLabel.grid(row=0, column=0, padx=5, pady=10)

            # Account Balance Value Stored Here self.accountBalance.get()
            self.accountBalance = ctk.StringVar()
            accountBalanceEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.accountBalance)
            accountBalanceEntry.grid(row=0, column=1,padx=5, pady=10)
            accountBalanceEntry.bind('<KeyRelease>', self.calculateLumpSum)
            accountBalanceEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(accountBalanceEntry))

        if self.bankOption == 'CHASE':
            # NRC LABEL
            nrcLabel = ctk.CTkLabel(self.mainFrame, text='Enter NRC USD:')
            nrcLabel.grid(row=1, column=0, padx=5, pady=10)
            
            # NRC Balance value stored in self.nrcBalance.get()
            self.nrcBalance = ctk.StringVar()
            nrcBalanceEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.nrcBalance)
            nrcBalanceEntry.grid(row=1, column=1, padx=5, pady=10)
            nrcBalanceEntry.bind('<KeyRelease>', self.calculateLumpSum)
            nrcBalanceEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(nrcBalanceEntry))
        
        #Label for spacing
        spacingLabel = ctk.CTkLabel(self.mainFrame, text='----------------------------------')
        spacingLabel.grid(row=2, column=1, pady=10)

        # Label for Settlement Balance
        settlementBalanceLabel = ctk.CTkLabel(self.mainFrame, text='*SETTLEMENT AMOUNT:')
        settlementBalanceLabel.grid(row=3, column=0, padx=5, pady=10)

        # settlement balance stored in self.settlementBalance.get()
        self.settlementBalance = ctk.StringVar()
        settlementBalanceEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.settlementBalance)
        settlementBalanceEntry.grid(row=3, column=1,padx=5, pady=10)
        settlementBalanceEntry.bind('<KeyRelease>', self.calculatePayments)
        settlementBalanceEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(settlementBalanceEntry))

        # Label for Settlement Balance
        intitialPaymentLabel = ctk.CTkLabel(self.mainFrame, text='INITIAL PAYMENT:\n(Down Payment)')
        intitialPaymentLabel.grid(row=4, column=0, padx=5, pady=10)

        # initial payment strored in self.initialPayment.get()
        self.initialPayment = ctk.StringVar()
        initialPaymentEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.initialPayment)
        initialPaymentEntry.grid(row=4, column=1,padx=5, pady=10)
        initialPaymentEntry.bind('<KeyRelease>', self.calculatePayments)
        initialPaymentEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(initialPaymentEntry))

        # Label for Number of Payments
        paymentNumberLabel = ctk.CTkLabel(self.mainFrame, text=f'*NUMBER OF PAYMENTS:\n(Max {self.maxPayments})')
        paymentNumberLabel.grid(row=5, column=0, padx=5, pady=10)
        
        # Number of payments 
        self.paymentNumber = ctk.StringVar()
        paymentNumberEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.paymentNumber)
        paymentNumberEntry.grid(row=5, column=1,padx=5, pady=10)
        paymentNumberEntry.bind('<KeyRelease>', self.calculatePayments)
        paymentNumberEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(paymentNumberEntry))

        # Label for first payment date
        paymentDateLabel = ctk.CTkLabel(self.mainFrame, text='*FIRST PAYMENT DATE:')
        paymentDateLabel.grid(row=6, column=0, padx=5, pady=10)
        
        # Number of payments 
        self.paymentDate = ctk.StringVar()
        paymentDateEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.paymentDate)
        paymentDateEntry.grid(row=6, column=1,padx=5, pady=10)
        self.paymentDate.set('MM/DD/YYYY')
        paymentDateEntry.bind('<KeyRelease>', self.calculatePayments)
        paymentDateEntry.bind('<Button-1>', lambda event: self.clearEntryOnclick(paymentDateEntry))
        
        # Reset Button
        resetButton = ctk.CTkButton(self.mainFrame, text='Reset', width=30, height=20, command=self.resetEntries)
        resetButton.grid(row=6, column=2)
        
        # Spacing for textboxes on the right
        spaceLabel2 = ctk.CTkLabel(self.mainFrame, text="                                                ")
        spaceLabel2.grid(row=0, column=2)

        #---------------------------------------TEXTBOXES-------------------------------------------
        if self.bankOption != 'BQ':
            
            if self.bankOption != 'CAVALRY':
                # Lump Sum 90%
                lump90Label = ctk.CTkLabel(self.mainFrame, text='LUMP SUM 90%:')
                lump90Label.grid(row=0, column=3)

                self.lump90Textbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state='disabled')
                self.lump90Textbox.grid(row=0, column=4)

                #LUMP SUM 85%
                lump85Label = ctk.CTkLabel(self.mainFrame, text='LUMP SUM 85%:')
                lump85Label.grid(row=1, column=3, pady=5, padx=5)
                
                self.lump85Textbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
                self.lump85Textbox.grid(row=1, column=4, padx=5,pady=5)

                # Lump Sum 80%
                lump80Label = ctk.CTkLabel(self.mainFrame, text='LUMP SUM 80%:')
                lump80Label.grid(row=2, column=3, pady=5, padx=5)
                
                self.lump80Textbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
                self.lump80Textbox.grid(row=2, column=4, padx=5,pady=5)

                # Lump Sum 75%
                lump75Label = ctk.CTkLabel(self.mainFrame, text='LUMP SUM 75%:')
                lump75Label.grid(row=3, column=3, pady=5, padx=5)
                
                self.lump75Textbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
                self.lump75Textbox.grid(row=3, column=4, padx=5,pady=5)
            else:
                #LUMP SUM 85%
                lump85Label = ctk.CTkLabel(self.mainFrame, text='LUMP SUM 85%:')
                lump85Label.grid(row=0, column=3, pady=5, padx=5)
                
                self.lump85Textbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
                self.lump85Textbox.grid(row=0, column=4, padx=5,pady=5)
        else:
            # Original Settlement
            originalSettlementLabel = ctk.CTkLabel(self.mainFrame, text='Original Settlement:')
            originalSettlementLabel.grid(row=0, column=3)

            self.originalSettlementTextbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state='disabled')
            self.originalSettlementTextbox.grid(row=0, column=4)

            # Settlement Amount
            settlementAmountLabel = ctk.CTkLabel(self.mainFrame, text='Settlement Amount:')
            settlementAmountLabel.grid(row=1, column=3, pady=5, padx=5)
            
            self.settlementAmountTextbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
            self.settlementAmountTextbox.grid(row=1, column=4, padx=5,pady=5)

        #Final Payment Textbox
        finalPaymentLabel = ctk.CTkLabel(self.mainFrame, text='FINAL PAYMENT:')
        finalPaymentLabel.grid(row=0, column=5, pady=5, padx=5)
        
        self.finalPaymentTextbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
        self.finalPaymentTextbox.grid(row=0, column=6, padx=5,pady=5)

        #Final Payment Date Textbox
        finalPaymentDateLabel = ctk.CTkLabel(self.mainFrame, text='FINAL PAYMENT DATE:')
        finalPaymentDateLabel.grid(row=1, column=5, pady=5, padx=5)
        
        self.finalPaymentDateTextbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
        self.finalPaymentDateTextbox.grid(row=1, column=6, padx=5,pady=5)

        # SIF EXPIRATION DATE
        sifExpDateLabel = ctk.CTkLabel(self.mainFrame, text='SIF EXPIRATION DATE:')
        sifExpDateLabel.grid(row=2, column=5, pady=5, padx=5)
        
        self.sifExpDateTextbox = ctk.CTkTextbox(self.mainFrame, width=100, height=5, state="disabled")
        self.sifExpDateTextbox.grid(row=2, column=6, padx=5,pady=5)

        # Custom Monthly Payment Label
        customMonthlyLabel = ctk.CTkLabel(self.mainFrame, text='CUSTOM MONTHLY\nPAYMENT:')
        customMonthlyLabel.grid(row=3, column=5, padx=5, pady=10)

        # Custom Monthly Payment
        self.customMonthly = ctk.StringVar()
        customMonthlyEntry = ctk.CTkEntry(self.mainFrame, textvariable=self.customMonthly, width=100)
        customMonthlyEntry.grid(row=3, column=6,padx=5, pady=10)
        customMonthlyEntry.bind('<KeyRelease>', self.calculatePayments)
        
        self.pressedCounter = 0

    def resetEntries(self):
        self.accountBalance.set('')
        try:
            self.nrcBalance.set('')
        except:
            print('NotChase')
        
        self.settlementBalance.set('')
        self.initialPayment.set('')
        self.paymentNumber.set('')
        self.paymentDate.set('MM/DD/YYYY')
        
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")
        
        if self.bankOption == 'CAVALRY':
            
            self.lump85Textbox.configure(state="normal")
            self.lump85Textbox.delete("0.0", "end")
            self.lump85Textbox.configure(state="disabled")
            
        elif self.bankOption == 'BQ':
            
            self.originalSettlementTextbox.configure(state="normal")
            self.originalSettlementTextbox.delete("0.0", "end")
            self.originalSettlementTextbox.configure(state="disabled")  

            self.settlementAmountTextbox.configure(state="normal") 
            self.settlementAmountTextbox.delete("0.0", "end")   
            self.settlementAmountTextbox.configure(state="disabled")   
            
        else:
            self.lump90Textbox.configure(state="normal")
            self.lump90Textbox.delete("0.0", "end")
            self.lump90Textbox.configure(state="disabled")

            # 85% of the account balance
            self.lump85Textbox.configure(state="normal")
            self.lump85Textbox.delete("0.0", "end")
            self.lump85Textbox.configure(state="disabled")

            # 80% of the account balan
            self.lump80Textbox.configure(state="normal")
            self.lump80Textbox.delete("0.0", "end")
            self.lump80Textbox.configure(state="disabled")

            # 75% of the account balance
            self.lump75Textbox.configure(state="normal")
            self.lump75Textbox.delete("0.0", "end")
            self.lump75Textbox.configure(state="disabled")
            
        self.finalPaymentTextbox.configure(state="normal")
        self.finalPaymentTextbox.delete("0.0", "end")
        self.finalPaymentTextbox.configure(state="disabled") 
        
        self.finalPaymentDateTextbox.configure(state="normal")
        self.finalPaymentDateTextbox.delete("0.0", "end")
        self.finalPaymentDateTextbox.configure(state="disabled") 
        
        self.sifExpDateTextbox.configure(state="normal")
        self.sifExpDateTextbox.delete("0.0", "end")
        self.sifExpDateTextbox.configure(state="disabled")

        

    def setContactEntry(self, value):
        if value == 'Mail':
            self.contactEntryVar.set('Address on File')
    
    def calculateLumpSum(self, value):
        value = float(self.accountBalance.get())

        try:
            value += float(self.nrcBalance.get())
        except:
            print('No NRC')

        #BQ Does not have these textboxes populated
        if self.bankOption != 'BQ':
            if self.bankOption != 'CAVALRY':
                # 90% of the account balance
                value90 = .90 * value
                self.lump90Textbox.configure(state="normal")
                self.lump90Textbox.delete("0.0", "end")
                self.lump90Textbox.insert(ctk.END, f"{value90:.2f}")
                self.lump90Textbox.configure(state="disabled")

                # 85% of the account balance
                value85 = .85 * value
                self.lump85Textbox.configure(state="normal")
                self.lump85Textbox.delete("0.0", "end")
                self.lump85Textbox.insert(ctk.END, f"{value85:.2f}")
                self.lump85Textbox.configure(state="disabled")

                # 80% of the account balance
                value80 = .80 * value
                self.lump80Textbox.configure(state="normal")
                self.lump80Textbox.delete("0.0", "end")
                self.lump80Textbox.insert(ctk.END, f"{value80:.2f}")
                self.lump80Textbox.configure(state="disabled")

                # 75% of the account balance
                value75 = .75 * value
                self.lump75Textbox.configure(state="normal")
                self.lump75Textbox.delete("0.0", "end")
                self.lump75Textbox.insert(ctk.END, f"{value75:.2f}")
                self.lump75Textbox.configure(state="disabled") 
            else:
                # 85% of the account balance
                value85 = .85 * value
                self.lump85Textbox.configure(state="normal")
                self.lump85Textbox.delete("0.0", "end")
                self.lump85Textbox.insert(ctk.END, f"{value85:.2f}")
                self.lump85Textbox.configure(state="disabled")
        else:
            # Pre-Suit is 60% and Post-Suit is 75% of the account balance
            if self.bqSuitVar.get() == 'PRE-SUIT':
                bqValue = .60
            elif self.bqSuitVar.get() == 'POST-SUIT':
                bqValue = .75

            # Add original settlement value to the textbox
            self.bqCalc = bqValue * value            
            self.originalSettlementTextbox.configure(state="normal")
            self.originalSettlementTextbox.delete("0.0", "end")
            self.originalSettlementTextbox.insert(ctk.END, f"{self.bqCalc}")
            self.originalSettlementTextbox.configure(state="disabled")  

    def calculatePayments(self, value):
        try:
            # If the initial payment and monthly payments both have values in their entryboxes print to the textbox.
            if self.customMonthly.get() != '' and self.paymentNumber.get() != '':
                if self.paymentNumber.get() != 0:
                    self.textbox.configure(state="normal")
                    self.textbox.delete("0.0", "end")
                    self.textbox.insert(ctk.END, f"Calculating based of Custom Monthly Payment!\n")
                    self.textbox.configure(state="disabled") 
        except:
            print('Not using number of payments')   

        try:
            if int(self.paymentNumber.get()) > self.maxPayments:
                return
        except:
            print('using custom monthly')
            
        try:
            if self.bankOption == 'CITIBANK-MACYS':
                if int(self.paymentNumber.get()) > 12 and float(self.accountBalance.get()) != float(self.settlementBalance.get()):
                    self.textbox.configure(state="normal")
                    self.textbox.delete("0.0", "end")
                    self.textbox.insert(ctk.END, f"No more than 12 payments for CitiBank-Macys unless balance in full!\n")
                    self.textbox.configure(state="disabled") 
                    return
        except:
            print('CITIBANK MACYS PAYMENT MAX')  
              
        # To avoid value errors
        if self.customMonthly.get() != '':
            customMonthly = float(self.customMonthly.get())
        else:
            customMonthly = 0
        
        # If no down payment make it zero
        if self.initialPayment.get() == '':
            initialPayment = 0
        elif self.initialPayment.get() == 0:
            initialPayment = 0
        else:
            initialPayment = float(self.initialPayment.get())
        
        settlementBalance = float(self.settlementBalance.get())

        try:
            if self.bankOption == 'BQ':
                bqSettlementAmount = self.bqCalc - initialPayment
                self.settlementAmountTextbox.configure(state="normal") 
                self.settlementAmountTextbox.delete("0.0", "end")   
                self.settlementAmountTextbox.insert(ctk.END, f"{bqSettlementAmount}")   
                self.settlementAmountTextbox.configure(state="disabled")   
        except:
            print('BQ Value Error')

        # Custom monthly payment must be zero to calculate based off number of payments
        if customMonthly == 0:
            #if no down payments
            if initialPayment == 0:
                #PAYMENT AMOUNT (BIF OVER PAYS)
                numPayments = float(self.paymentNumber.get())
            
                paymentAmount = settlementBalance / numPayments
            
                roundedPayment = round(paymentAmount, 2)
                firstPayment = settlementBalance - roundedPayment * (numPayments - 1)
            else:
                numPayments = float(self.paymentNumber.get())
                numPayments -= 1
                settlementBalance -= initialPayment
                paymentAmount = settlementBalance / numPayments
            
                roundedPayment = round(paymentAmount, 2)
                firstPayment = settlementBalance - roundedPayment * (numPayments - 1)
        # Calculate off custom monthly payment
        else:
            settlementBalance -= initialPayment 
            numPayments = settlementBalance / float(customMonthly)
            roundedNumPayments = floor(numPayments)
            difNumPayments = numPayments - roundedNumPayments
            
            roundedPayment = round(customMonthly, 2)
            
            firstPayment = roundedPayment * difNumPayments
            
            
            print(firstPayment, f'monthly {.15 * customMonthly}')
            
            if firstPayment > 0.15 * customMonthly:
                roundedNumPayments += 1
                numPayments += 1
            else:
                firstPayment += customMonthly
            
            if roundedNumPayments > self.maxPayments:
                self.textbox.configure(state="normal")
                self.textbox.insert(ctk.END, f"No Payments Larger than {self.maxPayments} for {self.bankOption}\n")
                self.textbox.configure(state="disabled") 
                return
        try:
            print(firstPayment)
            print(paymentAmount)
        except:
            print(customMonthly)

        try:
            self.finalPaymentTextbox.configure(state="normal")
            self.finalPaymentTextbox.delete("0.0", "end")
            self.finalPaymentTextbox.insert(ctk.END, f"{paymentAmount:.2f}")
            self.finalPaymentTextbox.configure(state="disabled") 
        except:
            self.finalPaymentTextbox.configure(state="normal")
            self.finalPaymentTextbox.delete("0.0", "end")
            self.finalPaymentTextbox.insert(ctk.END, f"{customMonthly:.2f}")
            self.finalPaymentTextbox.configure(state="disabled") 
            paymentAmount = customMonthly

        firstPaymentDate = self.paymentDate.get()
        passedDate = firstPaymentDate
        passedDate = datetime.datetime.strptime(passedDate, "%m/%d/%Y").date()
        
        today = datetime.date.today()
        year = today.year
        
        date = datetime.datetime.strptime(firstPaymentDate, "%m/%d/%Y")
        
        # calculate new final date
        newDate_dt = date + relativedelta(months=int(numPayments) - 1)
        newDate = datetime.datetime.strftime(newDate_dt, "%m/%d/%Y")
        
        self.finalPaymentDateTextbox.configure(state="normal")
        self.finalPaymentDateTextbox.delete("0.0", "end")
        self.finalPaymentDateTextbox.insert(ctk.END, f"{newDate}")
        self.finalPaymentDateTextbox.configure(state="disabled") 
        
        # SIF Expiration Date contents (chase)
        newDate_dtObj = newDate_dt + relativedelta(days=10)
        sifExpirationDate = datetime.datetime.strftime(newDate_dtObj, "%m/%d/%Y")
        
        self.sifExpDateTextbox.configure(state="normal")
        self.sifExpDateTextbox.delete("0.0", "end")
        self.sifExpDateTextbox.insert(ctk.END, f"{sifExpirationDate}")
        self.sifExpDateTextbox.configure(state="disabled")

        #Clear self.textbox if successful
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")
        self.pressedCounter = 0
        self.amorTable(passedDate, paymentAmount, newDate, firstPayment, numPayments, initialPayment, sifExpirationDate)

    def amorTable(self, first_payment_date, first_monthly_payment, last_payment_date, last_monthly_payment, total_payments, downPayment, sif_expiration_date):
        # Date conversion logic for proper formatting
        first_payment_date = datetime.datetime.strftime(first_payment_date, '%Y-%m-%d')
        first_payment_date = datetime.datetime.strptime(first_payment_date, '%Y-%m-%d').strftime('%m/%d/%Y')
        first_payment_date = datetime.datetime.strptime(first_payment_date, '%m/%d/%Y').date()
        
        bank_num_payments = total_payments 
        self.accountBal = float(self.accountBalance.get())
        
        # run calculations
        self.backend_table_calculations(first_payment_date, first_monthly_payment, last_payment_date,
                                        last_monthly_payment, bank_num_payments, downPayment,
                                        sif_expiration_date)
        
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
        global onTop
        if self.last_monthly_payment >= self.first_monthly_payment:
            onTop = True
        else:
            onTop = False
        
        # First date displayed in table
        self.formatted_first_date = first_payment_date
        self.formatted_first_date = self.formatted_first_date.strftime("%m/%d/%Y")
        
        # Call table window and (re-)initialize self.textbox
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")

        self.totalPayments = 0
        # Display header row, first date, monthly paymens
        self.textbox.insert(ctk.END, "Payment Dates\t\tMonthly Payments") 
        self.textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        
        if self.downPayment == 0 or self.downPayment == None or self.downPayment == '':
            self.downPayment = 0       
            self.first_monthly_payment = round(first_monthly_payment, 2)
            self.last_monthly_payment = round(last_monthly_payment, 2)
            self.finalPayment = 0.0
            self.finalPayment += self.downPayment
            
            if onTop:
                self.textbox.insert(ctk.END, f"\n1. {self.formatted_first_date}\t\t\t${self.last_monthly_payment:.2f}")
            else:
                self.textbox.insert(ctk.END, f"\n1. {self.formatted_first_date}\t\t\t${self.first_monthly_payment:.2f}")
            
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
                self.textbox.insert(ctk.END, f"\n{i + 1}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}") 
                self.finalPayment += float(self.first_monthly_payment)
                
                # Display last payment date in list and first/last payments in footer
                # if bank payments is more than one, display last payment (last payment not needed if only one payment)
            self.next_payment_date = self.first_payment_date + relativedelta(months=int(self.bank_num_payments - 1))
            self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
            if int(self.bank_num_payments) != 1:
                self.totalPayments += 1
                
                if onTop:
                    self.textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments)))}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}")
                else:
                    self.textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments)))}. {self.next_payment_date}\t\t\t${self.last_monthly_payment:.2f}")
                
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
            
            self.startdifPayment = self.first_payment_date + relativedelta(months=int(1))
            self.startdifPayment = datetime.datetime.strftime(self.startdifPayment, "%m/%d/%Y")
            
            self.startMonthPayments = self.first_payment_date + relativedelta(months=int(2))
            self.startMonthPayments = datetime.datetime.strftime(self.startMonthPayments, "%m/%d/%Y")
            
            self.textbox.insert(ctk.END, f"\n1. {self.formatted_first_date}\t\t\t${self.downPayment:.2f}")
            
            if onTop:
                self.textbox.insert(ctk.END, f"\n2. {self.next_payment_date}\t\t\t${self.last_monthly_payment:.2f}")
            else:
                self.textbox.insert(ctk.END, f"\n2. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}")
                
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
                self.textbox.insert(ctk.END, f"\n{i + 2}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}") 
                self.finalPayment += float(self.first_monthly_payment)  
        
            # Display last payment date in list and first/last payments in footer
                # if bank payments is more than one, display last payment (last payment not needed if only one payment)
            self.next_payment_date = self.first_payment_date + relativedelta(months=int(self.bank_num_payments))
            self.next_payment_date = datetime.datetime.strftime(self.next_payment_date, "%m/%d/%Y")
            if int(self.bank_num_payments) != 1:
                self.totalPayments += 1
                
                if onTop:
                    self.textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments) + 1))}. {self.next_payment_date}\t\t\t${self.first_monthly_payment:.2f}")
                else:    
                    self.textbox.insert(ctk.END, f"\n{len(range(int(self.bank_num_payments) + 1))}. {self.next_payment_date}\t\t\t${self.last_monthly_payment:.2f}")
                
                
                self.finalPayment += float(self.last_monthly_payment)
                pass

        self.sif_expiration_date = self.first_payment_date + relativedelta(months=int(self.totalPayments - 1))
        self.sif_expiration_date = self.sif_expiration_date + relativedelta(days=int(10))
        self.sif_expiration_date = datetime.datetime.strftime(self.sif_expiration_date, "%m/%d/%Y")
        
        self.textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        
        if self.downPayment:
            self.textbox.insert(ctk.END, f"\nFirst payment:\t\t\t${self.downPayment:.2f}")
        elif not self.downPayment:
            if onTop:
                self.textbox.insert(ctk.END, f"\nFirst payment:\t\t\t${self.last_monthly_payment:.2f}")
            else:
                self.textbox.insert(ctk.END, f"\nFirst payment:\t\t\t${self.first_monthly_payment:.2f}")
        
        if onTop:  
            self.textbox.insert(ctk.END, f"\nLast payment:\t\t\t${self.first_monthly_payment:.2f}")
        else:
            self.textbox.insert(ctk.END, f"\nLast payment:\t\t\t${self.last_monthly_payment:.2f}")
            
        self.textbox.insert(ctk.END, f"\nTotal Payment:\t\t\t${self.finalPayment:.2f}")
        self.textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        self.textbox.insert(ctk.END, f"\nFirst Payment Date:\t\t\t{self.formatted_first_date}")
        self.textbox.insert(ctk.END, f"\nLast Payment Date:\t\t\t{self.next_payment_date}")
        self.isSif = False
        if round(self.finalPayment, 2) != round(self.accountBal, 2):
            print(self.accountBal, " ", self.finalPayment)
            self.isSif = True
            self.textbox.insert(ctk.END, f"\nSIF Expiration Date:\t\t\t{self.sif_expiration_date}")
            
        self.textbox.insert(ctk.END, "\n-----------------------------------------------------------")
        self.textbox.configure(state="disabled")  

    def addToTable(self):
        
        # Counter to check if function has been run
        user = os.getlogin()
        date=''
        date = datetime.datetime.today().strftime('%m/%d/%Y')
        
        # If function has not been run, display contents
        if self.pressedCounter == 0:
            self.textbox.configure(state="normal")  
            self.textbox.insert(ctk.END, f"\nRESPONSIBLE: {user}")
            self.textbox.insert(ctk.END, f"\nBALANCE: ${self.accountBal:.2f}")
            self.textbox.insert(ctk.END, f"\nPAYMENT TYPE: {self.deliveryVar.get()}")
            
            if self.downPayment == 0:
                if onTop:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments} {self.termsVar.get()} payments with the first payment of ${self.last_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and {self.totalPayments - 1} payment of ${self.first_monthly_payment:.2f}."))         
                else:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments - 1} {self.termsVar.get()} payments of ${self.first_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and the final payment of ${self.last_monthly_payment:.2f}."))
            
            else:
                if onTop:                    
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, on {self.startdifPayment} a payment of\n"
                                        f"${self.last_monthly_payment:.2f} , and then on {self.startMonthPayments} {self.totalPayments - 2} {self.termsVar.get()} payments of ${self.first_monthly_payment:.2f}"))
                else:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, on {self.startdifPayment} {self.totalPayments - 2} {self.termsVar.get()} payments of\n"
                                        f"${self.first_monthly_payment:.2f} , and then on {self.next_payment_date} a payment of ${self.last_monthly_payment:.2f}"))
            
            if self.isSif:
                self.textbox.insert(ctk.END, f"\nTOTAL SIF AMOUNT: ${self.finalPayment:.2f}") 
                self.isSif = True  
            else:
                self.isSif = False
                                 
            self.textbox.insert(ctk.END, f"\nDELIVERY TYPE: {self.contactVar.get()}: {self.contactEntryVar.get()}")
            self.textbox.insert(ctk.END, f"\n1099 C GIVEN: {self.taxVar.get()}")
            self.textbox.insert(ctk.END, f"\nRECAP: {self.verbalAgreement.get()} VERBALLY AGREED TO THE ABOVE TERMS ON ({date})")
            self.textbox.configure(state="disabled")  
            self.pressedCounter += 1
        
        # If function has been run, clear previous contents (last 7 lines) and display contents
        elif self.pressedCounter == 1:
            self.textbox.configure(state="normal")  
            if self.isSif:
                self.textbox.delete("end-9l", "end")
            else:
                self.textbox.delete("end-8l", "end")
                
            self.textbox.insert(ctk.END, f"\nRESPONSIBLE: {user}")
            self.textbox.insert(ctk.END, f"\nBALANCE: ${self.accountBal:.2f}")
            self.textbox.insert(ctk.END, f"\nPAYMENT TYPE: {self.deliveryVar.get()}")
            
            if self.downPayment == 0:
                if onTop:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments} {self.termsVar.get()} payments with the first payment of ${self.last_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and {self.totalPayments - 1} payment of ${self.first_monthly_payment:.2f}."))         
                else:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: ${self.finalPayment:.2f} paid over {self.totalPayments - 1} {self.termsVar.get()} payments of ${self.first_monthly_payment:.2f}\nbeginning on {self.formatted_first_date} "
                            f"and the final payment of ${self.last_monthly_payment:.2f}."))
            
            else:
                if onTop:                    
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, on {self.startdifPayment} a payment of\n"
                                        f"${self.last_monthly_payment:.2f} , and then on {self.startMonthPayments} {self.totalPayments - 2} {self.termsVar.get()} payments of ${self.first_monthly_payment:.2f}"))
                else:
                    self.textbox.insert(ctk.END, (f"\nPAYMENT TERMS: Starting on {self.formatted_first_date} a payment of ${self.downPayment}, on {self.startdifPayment} {self.totalPayments - 2} {self.termsVar.get()} payments of\n"
                                        f"${self.first_monthly_payment:.2f} , and then on {self.next_payment_date} a payment of ${self.last_monthly_payment:.2f}"))
            
            if self.isSif:
                self.textbox.insert(ctk.END, f"\nTOTAL SIF AMOUNT: ${self.finalPayment:.2f}")
                                
            self.textbox.insert(ctk.END, f"\nDELIVERY TYPE: {self.contactVar.get()}: {self.contactEntryVar.get()}")
            self.textbox.insert(ctk.END, f"\n1099 C GIVEN: {self.taxVar.get()}")
            self.textbox.insert(ctk.END, f"\nRECAP: {self.verbalAgreement.get()} VERBALLY AGREED TO THE ABOVE TERMS ON ({date})")
            self.textbox.configure(state="disabled")

    def update_gif(self, frame_index):
            try:
                frame = self.frames[frame_index]
                image = ImageTk.PhotoImage(frame.resize((150, 85)))

                self.img_label.configure(image=image)

                frame_index = (frame_index + 1) % len(self.frames)
                if self.easterEggCount == 10:
                    self.after(15, self.update_gif, frame_index)  # Update every 100 milliseconds (adjust the interval as needed)
                else:
                    self.img_label.configure(image=self.image)
            except IndexError:
                pass

    def easterEgg(self):
        self.easterEggCount += 1
        if self.easterEggCount == 10:
            self.frames = []
            datafile2 = "cat-spinning.gif"
            if not hasattr(sys, "frozen"):
                datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
            else:
                datafile2 = os.path.join(sys.prefix, datafile2)
            gif = Image.open(datafile2)
            try:
                while True:
                    self.frames.append(gif.copy())
                    gif.seek(len(self.frames))
            except EOFError:
                pass

            self.update_gif(0) # Start updating and playing the GIF
            
        elif self.easterEggCount > 10:
            self.easterEggCount = 0

if __name__ == "__main__":
    root = CalculatorGui()
    root.mainloop()
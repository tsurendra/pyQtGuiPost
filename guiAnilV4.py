#Author : Kunchala Anil
#Date : 28 Aug 2016
#Email : anilkunchalaece@gmail.com

#Check the Automatic Button Genration Clearly - Ref guiAnilV3.py

#Import the Layout
from orgLayout import Ui_prepare2Pg
#import csv for TestData
import csv
#import the TestData
from testData import TestData
#Import the PyQt Core and Gui Libraries
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
"""
The Function of Buttons are as follows:

PREVIOUS BUTTON :
    it is used to move to i.e displays the previous Question

NEXT BUTTON :
    it is used to move to i.e displays the next question

SUBMIT BUTTON ;
    it is used to submit the Answer for the respective Question
    when user clicks the submit button, it changes the color to green
    
MARK FOR REVIEW :
    it is used to select the Respective question to review later. When User clicks this button
    respective button changes the color to red

END TEST :
    this is used to display the "resDict" which stores the Uid as key and user option as Value


Question Index is the anchor of total Program we use Question Index to Move to the Next and Previous Question

In Scroll area Buttons are created using the for loop.
Each button name i.e text is set as its Uid Number so we will make a dict "btn" and store the Uid as key and
and generated object as value. it is useful when we try to access the questions when corresponding button is clicked
in scroll area

TestData Object will generate a Few instanece Variable named as queDict,optADict,optBDict,
optCDict.optDDict and keys which holds the Question,optA,optB,optC,optD as Dictionaries where keys
is the key value for Each Dict variables


"""

class guiLogic(Ui_prepare2Pg):
    def __init__(self):
        self.questionIndex = 1 #variable to hold the questionIndex it is hero of our movie
        self.data = TestData() # Create a TestData Object which supply necessary Ingredients
        self.maxQuestions = len(self.data.queDict) # 
        self.rows = 5 # it is used to hold the  max no of rows we want in scroll widget
        self.rowAddition = self.rows #this is just a copy of rows value which is used in Automatic generation of btn's in Scroll Area
        self.resultDict = { } # it holds the user selected Options
        self.selectedOption = 'n' # Default option
        self.x = 0 # x and y values supply as co-ordinates in grid layout in Scroll widget 
        self.y = 0
        self.btn = {} #this will hold the ScrollArea Btn's with name and Object as Key and Value Pairs

        self.addScrollArea() #add scroll area when object is called
        self.setupLogic()#start the logic.. (I dont find a Good name for that method)
        self.timerValue = 0;
        self.startTimer();

    def addScrollArea(self):
        for key in range (len(self.data.keys)):
            self.btnKey = str(key+1) #added 1 to key since for loop starts from '0' and Question Index starts from 1
            self.btn[self.btnKey] = QtGui.QPushButton(ui.scrollAreaWidgetContents) # generate pushbutton object and add that object to dictionary for future Reference
            self.btn[self.btnKey].setMaximumSize(QtCore.QSize(30, 30))
            self.btnText = str(key+1) #set the text as key value which is used as reference to Respectiv Question
            self.btn[self.btnKey].setText(self.btnText) #Add the test to the btn
            #self.btn[self.btnKey].setCheckable(True)
            #self.btn.setMaximumSize(QtCore.QSize(100, 70))
            self.btn[self.btnKey].toggle()
            self.btn[self.btnKey].clicked.connect(self.scrollFcn) #Add the event handler to the Btn.. all the Btns in Scroll area are assigned to same Callback Function i.e scrollFcn
        #Take some time and look at this Logic.. it eats more time for me
            if key < self.rows:
                if key == 0:
                    self.y = 0
                    self.x = 0
                else:
                    self.y = self.y + 1

            else:
                self.x = self.x+1
                self.y = 0
                self.rows = self.rows + self.rowAddition #Particularly this line
#           print "x" + str(self.x)
#            print "y" + str(self.y)
#            print "key" + str(key)
#            print "self.rows" + str(self.rows)
            
            ui.gridLayout.addWidget(self.btn[self.btnKey],self.x,self.y) # Add the Button to Widget
#            print self.btn[self.btnKey]

    def scrollFcn(self):
        print "Scroll Btn Clicked"
        print MainWindow.sender().text() #this will grab the Pushbutton Reference Object From Mainwindow which is used to access the Btn Data
        #when the scroll Btn is Pressed with Reference Key Id call retranslateUi with key function
        self.questionIndex = int(MainWindow.sender().text())# from the Object get the Text of Function which is Same as Uid of Question
        self.retranslateUi(self.questionIndex) # Display the respscted QUestion using Question Index
        self.showPreviosOption(self.questionIndex)

    def showPreviosOption(self,QIndex):
        #TO Highlight the user Selected Option If user Comes back - Check Issue : https://github.com/anilkunchalaece/pyQtGuiImproved/issues/1
        self.checked = self.resultDict.get(QIndex,False)
        if self.checked:
            print self.checked
            if self.checked == 'A':
                ui.optARadioButton.setChecked(True)
            elif self.checked == 'B':
                ui.optBRadioButton.setChecked(True)
            elif self.checked == 'C':
                ui.optCRadioButton.setChecked(True)
            elif self.checked == 'D':
                ui.optDRadioButton.setChecked(True)
                
                

    def updateLcd(self):
        ##http://stackoverflow.com/questions/775049/python-time-seconds-to-hms
        # this function increments the self.timerValue variable which is converted to hh:mm:ss 
        m, s = divmod(self.timerValue, 60)
        h, m = divmod(m, 60)
        self.time = str(h) + ':' + str(m)+':'+str(s) 
        ui.lcdNumber.display(self.time)
        self.timerValue = self.timerValue + 1

    def startTimer(self):
        #Start the timer at the Begining of the Test
        #for every 1 sec call the updateLcd Function 
        ui.lcdNumber.setDigitCount(8)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateLcd)
        self.timer.start(1000) 
        ui.lcdNumber.show() 
        ui.lcdNumber.display('0:0:0')
    
    def setupLogic(self):
        #Assign the Duties for Buttons
        ui.nextBtn.clicked.connect(self.nextFcn)
        ui.reviewBtn.clicked.connect(self.reviewFcn)
        ui.submitBtn.clicked.connect(self.submitFcn)
        ui.endTestBtn.clicked.connect(self.endTestFcn)
        ui.previousBtn.clicked.connect(self.previousFcn)
      
    def nextFcn(self):
        #when next Btn is pressed increment the questionIndex and Display the Question using Index
        print "Next Btn Selected"
        self.questionIndex=newLogic.questionIndex+1
        if self.questionIndex > self.maxQuestions :
            self.questionIndex = 1
        self.retranslateUi(newLogic.questionIndex)
        self.showPreviosOption(self.questionIndex)

    def reviewFcn(self):
        #when Review Btn is Pressed change the color of respective Btn
        print "Review Btn Pressed"
        self.changeColor(self.questionIndex,'r')

    def changeColor(self,Qindex,color):
        #this function takes Qindex and Color as arguments
        #Using QIndex we Access the respective Object using "btn" Dictonary created in the Automatic scrollArea Button Addition
        #we change the Qindex to str since Dic Key value is String
#        print self.btn[str(Qindex)]
        if color == 'r':
            bgColor = "background-color: red"
        elif color == 'g' :
            bgColor = "background-color: green"
        elif color == 'y' :
            bgColor = "background-color: yellow"
        self.btn[str(Qindex)].setStyleSheet(bgColor) #Change the color of Respective Btn
        
    def submitFcn(self):
        # When submit button is pressed see which of the toggle button is checked and select the option accordingly
        # and the store the respective value to the resulDict with QIndex as Key
        # then Change the color of the Respective Button is Scroll btn usinf Qindex 
        
        print "Submit Btn Pressed"

        if ui.optARadioButton.isChecked():
            print "Option A is Selected"
            self.selectedOption = 'A'
        elif ui.optBRadioButton.isChecked():
            print "Option Bis Selected"
            self.selectedOption = 'B'
        elif ui.optCRadioButton.isChecked():
            print "Option C is Selected"
            self.selectedOption = 'C'
        elif ui.optDRadioButton.isChecked():
            print"Option D is Selected"
            self.selectedOption = 'D'
        else:
            print "No Option selected"
            self.selectedOption = 'N'
        self.resultDict[self.questionIndex] = self.selectedOption #Store the Result in Dict
        self.changeColor(self.questionIndex,'g') #Change the Color
        
    def endTestFcn(self):
        #when endTest btn is clicked Print the Resulting Dict
        
        print "endTest Btn Pressed"
        print "Output Dict is "
        print self.resultDict

    def previousFcn(self):
        #when previous btn is clicked decrement the Qindex value and Display the respective Question using Qindex
        print "Previous Btn Pressed"
        newLogic.questionIndex=newLogic.questionIndex-1
        if self.questionIndex == 0:
            self.questionIndex = self.maxQuestions
            
        newLogic.retranslateUi(newLogic.questionIndex)
        self.showPreviosOption(self.questionIndex)

    def retranslateUi(self,QIndex):
        #this function takes QIndex as argument
        #where Qindex is Key value in Data
        #using key values we set the Text of Question label and optA,B,C and D Radio Buttons 
        ui.testNameLabel.setText(_translate("prepare2Pg", "TEST NAME", None))
        ui.QuestionLabel.setText(_translate("prepare2Pg", newLogic.data.queDict[str(QIndex)], None))
        ui.optARadioButton.setText(_translate("prepare2Pg", newLogic.data.optADict[str(QIndex)], None))
        ui.optBRadioButton.setText(_translate("prepare2Pg", newLogic.data.optBDict[str(QIndex)], None))
        ui.optCRadioButton.setText(_translate("prepare2Pg", newLogic.data.optCDict[str(QIndex)], None))
        ui.optDRadioButton.setText(_translate("prepare2Pg", newLogic.data.optDDict[str(QIndex)], None))
        
        #this logic has to be worked On.. This is A "BUG" i cant Find
        # Aug 28 -Create A Button Group - http://stackoverflow.com/questions/29270307/how-can-i-change-the-name-of-a-qbuttongroup-in-qt-designer
        # http://stackoverflow.com/questions/8689909/uncheck-radiobutton-pyqt4
        ui.buttonGroup.setExclusive(False)
        ui.optARadioButton.setChecked(False)
        ui.optBRadioButton.setChecked(False)
        ui.optCRadioButton.setChecked(False)
        ui.optDRadioButton.setChecked(False)
        ui.buttonGroup.setExclusive(True)
                  
        



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_prepare2Pg()
    ui.setupUi(MainWindow)
    MainWindow.show()
    newLogic = guiLogic()
    newLogic.retranslateUi(newLogic.questionIndex)
    
    sys.exit(app.exec_())
    

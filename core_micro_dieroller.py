#
#   CORE Micro DieRoller 0.1.5 Beta
#   Written for Python 3.11.6
#
###################################

"""
CORE Micro DieRoller 0.1.5 Beta
-------------------------------

This program rolls 6-sided dice and calculates their results.
"""
#import vlc

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from PyQt5 import uic
import PyQt5.QtMultimedia as MM
import time
from mainwindow import Ui_MainWindow
from aboutdialog import Ui_aboutDialog
from alertdialog import Ui_alertDialog
from random import randint
from rpg_tools.pydice import roll
import sys
import os
import logging

__author__ = 'Shawn Driscoll <shawndriscoll@hotmail.com>\nshawndriscoll.blogspot.com'
__app__ = 'CORE Micro DieRoller 0.1.5 Beta'
__version__ = '0.1.5b'
__py_version__ = '3.11.6'
__expired_tag__ = False

#form_class = uic.loadUiType("mainwindow.ui")[0]

class aboutDialog(QDialog, Ui_aboutDialog):
    def __init__(self):
        '''
        Open the About dialog window
        '''
        super().__init__()
        log.info('PyQt5 aboutDialog initializing...')
        self.setWindowFlags(Qt.Drawer | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        log.info('PyQt5 aboutDialog initialized.')
        
    def acceptOKButtonClicked(self):
        '''
        Close the About dialog window
        '''
        log.info('PyQt5 aboutDialog closing...')
        self.close()

class alertDialog(QDialog, Ui_alertDialog):
    def __init__(self):
        '''
        Open the Alert dialog window
        '''
        super().__init__()
        log.info('PyQt5 alertDialog initializing...')
        self.setWindowFlags(Qt.Drawer | Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.aboutOKButton.clicked.connect(self.acceptOKButtonClicked)
        log.info('PyQt5 alertDialog initialized.')
        
    def acceptOKButtonClicked(self):
        '''
        Close the Alert dialog window
        '''
        log.info('PyQt5 alertDialog closing...')
        self.close()

#class MainWindow(QMainWindow):
#class MainWindow(QMainWindow, form_class):
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        '''
        Display the main app window.
        Connect all the buttons to their functions.
        Initialize their value ranges.
        '''
        super().__init__()
        
        #uic.loadUi("mainwindow.ui", self)
        
        log.info('PyQt5 MainWindow initializing...')
        self.setupUi(self)
        self.rollButton.clicked.connect(self.rollButtonClicked)
        self.clearAll_Button.clicked.connect(self.clearall_buttonClicked)
        self.action_ClearAll.triggered.connect(self.clearall_buttonClicked)
        self.actionVisit_Blog.triggered.connect(self.Visit_Blog)
        self.actionFeedback.triggered.connect(self.Feedback)
        self.actionOverview.triggered.connect(self.Overview_menu)
        self.actionAbout_CoreMicro.triggered.connect(self.actionAbout_triggered)
        self.actionQuit.triggered.connect(self.quitButton_clicked)
        self.input1dice.valueChanged.connect(self.input1dice_valueChanged)
        self.dice1box = True
        self.input1dice.setDisabled(self.dice1box)
        self.input1skill.valueChanged.connect(self.input1skill_valueChanged)
        self.level1box = True
        self.input1skill.setDisabled(self.level1box)
        self.input1DM.valueChanged.connect(self.input1DM_valueChanged)
        self.DM1box = True
        self.input1DM.setDisabled(self.DM1box)
        self.pushingit1 = False
        self.selPushingit1.toggled.connect(self.selPushingit1_valueChanged)
        self.pushingit1box = True
        self.selPushingit1.setDisabled(self.pushingit1box)
        self.input2dice.valueChanged.connect(self.input2dice_valueChanged)
        self.dice2box = True
        self.input2dice.setDisabled(self.dice2box)
        self.input2skill.valueChanged.connect(self.input2skill_valueChanged)
        self.level2box = True
        self.input2skill.setDisabled(self.level2box)
        self.input2DM.valueChanged.connect(self.input2DM_valueChanged)
        self.DM2box = True
        self.input2DM.setDisabled(self.DM2box)
        self.pushingit2 = False
        self.selPushingit2.toggled.connect(self.selPushingit2_valueChanged)
        self.pushingit2box = True
        self.selPushingit2.setDisabled(self.pushingit2box)
        self.rollbox = True
        self.rollButton.setDisabled(self.rollbox)
        self.selDiff.addItem('    Choose One')
        self.selDiff.addItem('1 = Simple')
        self.selDiff.addItem('2 = Easy')
        self.selDiff.addItem('3 = Challenging')
        self.selDiff.addItem('4 = Difficult')
        self.selDiff.addItem('5 = Hard')
        self.selDiff.addItem('6 = Very Hard')
        self.selDiff.addItem('7 = Unlikely')
        self.selDiff.addItem('8 = Ridiculous')
        self.selDiff.addItem('9 = Absurd')
        self.selDiff.addItem('10 = Insane')
        self.selDiff.addItem('Random')
        self.selDiff.addItem('Unknown')
        self.selDiff.addItem('Gradiated')
        self.selDiff.addItem('Opposed')
        self.selDiff.setCurrentIndex(0)
        self.selDiff.currentIndexChanged.connect(self.selDiff_valueChanged)
        self.rollInput.returnPressed.connect(self.manual_roll)
        self.clearRollHistory.clicked.connect(self.clearRollHistoryClicked)
        self.action_ClearRollHistory.triggered.connect(self.clearRollHistoryClicked)

        self.prompts = ['NO AND something negative *',
                        'NO BUT something positive',
                        'YES BUT something negative',
                        'YES (nailed it precisely)',
                        'YES AND something positive *']

        #self.le = QLineEdit()
        #self.le.returnPressed.connect(self.append_text)

        # Is the difficulty known?
        self.unknown = False

        # Set difficulty to not chosen yet
        self.target_num = 0

        # Set the About menu item
        self.popAboutDialog=aboutDialog()

        # Set the Alert menu item
        self.popAlertDialog=alertDialog()

        log.info('PyQt5 MainWindow initialized.')

        if __expired_tag__ == True:
            '''
            Beta for this app has expired!
            '''
            log.warning(__app__ + ' expiration detected...')
            self.alert_window()
            '''
            display alert message and disable all the things
            '''
            self.selDiff.setDisabled(True)
            self.rollButton.setDisabled(True)
            self.clearAll_Button.setDisabled(True)
            self.action_ClearAll.setDisabled(True)
            self.actionVisit_Blog.setDisabled(True)
            self.actionFeedback.setDisabled(True)
            self.actionOverview.setDisabled(True)
            self.actionAbout_CoreMicro.setDisabled(True)
            self.rollInput.setDisabled(True)
            self.clearRollHistory.setDisabled(True)
            self.rollBrowser.setDisabled(True)
            self.action_ClearRollHistory.setDisabled(True)
            self.rollButton.setDisabled(True)

    def selDiff_valueChanged(self):
        '''
        Choose the Difficulty Level for the roll
        '''
        difficulty_level = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if self.selDiff.currentIndex() == 0:
            self.target_num = 0
        elif self.selDiff.currentIndex() == 11:
            
            # A random Difficulty Level has been asked for
            log.debug('Difficulty Level is random')
            self.unknown = False
            self.selDiff.setCurrentIndex(randint(1,10))
            self.target_num = difficulty_level[self.selDiff.currentIndex()]
        elif self.selDiff.currentIndex() == 12:
            
            # The Difficulty Level is unknown to the player.
            # The Referee can see the Difficulty Level shown on their console.
            self.unknown = True
            self.target_num = difficulty_level[randint(1,10)]
            log.debug('Difficulty Level is unknown: %d' % self.target_num)
            print('The unknown Difficulty Level is %d' % self.target_num)
        elif self.selDiff.currentIndex() >= 1 and self.selDiff.currentIndex() <= 10:
            
            # A regular Difficulty Level has been given to the player to input
            self.unknown = False
            self.target_num = difficulty_level[self.selDiff.currentIndex()]
            log.debug('Buttons initialized for Difficulty Level: %d' % self.target_num)
        elif self.selDiff.currentIndex() == 13:
            self.unknown = False
            self.target_num = 13
            log.debug('Gradiated Roll has been asked for')
        elif self.selDiff.currentIndex() == 14:
            self.unknown = False
            self.target_num = 14
            log.debug('Opposed Roll has been asked for')
        
        # Reset the buttons whenever a Difficulty Level has been chosen
        if self.target_num == 0:
            self.dice1box = True
            self.level1box = True
            self.DM1box = True
            self.pushingit1box = True
            self.dice2box = True
            self.level2box = True
            self.DM2box = True
            self.pushingit2box = True
            self.rollbox = True
        elif self.target_num >= 1 and self.target_num <= 10:
            self.dice1box = False
            self.level1box = False
            self.DM1box = False
            self.pushingit1box = False
            self.dice2box = True
            self.level2box = True
            self.DM2box = True
            self.pushingit2box = True
            self.rollbox = False
        elif self.target_num == 13:
            self.dice1box = False
            self.level1box = False
            self.DM1box = False
            self.pushingit1box = False
            self.dice2box = True
            self.level2box = True
            self.DM2box = True
            self.pushingit2box = True
            self.rollbox = False
        elif self.target_num == 14:
            self.dice1box = False
            self.level1box = False
            self.DM1box = False
            self.pushingit1box = False
            self.dice2box = False
            self.level2box = False
            self.DM2box = False
            self.pushingit2box = False
            self.rollbox = False
        self.input1dice.setDisabled(self.dice1box)
        self.input1skill.setDisabled(self.level1box)
        self.input1DM.setDisabled(self.DM1box)
        self.selPushingit1.setDisabled(self.pushingit1box)
        self.input1dice.setValue(1)
        self.input1skill.setValue(0)
        self.input1DM.setValue(0)
        self.selPushingit1.setChecked(False)
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.input2dice.setDisabled(self.dice2box)
        self.input2skill.setDisabled(self.level2box)
        self.input2DM.setDisabled(self.DM2box)
        self.selPushingit2.setDisabled(self.pushingit2box)
        self.input2dice.setValue(1)
        self.input2skill.setValue(0)
        self.input2DM.setValue(0)
        self.selPushingit2.setChecked(False)
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        self.rollButton.setDisabled(self.rollbox)

    def input1dice_valueChanged(self):
        '''
        Number of dice was entered.
        '''
        
        # reset the screen
        self.input1skill.setValue(0)
        self.input1DM.setValue(0)
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.selPushingit1.setChecked(False)
    
    def input2dice_valueChanged(self):
        '''
        Number of dice was entered (defending).
        '''
        
        # reset the screen
        self.input2skill.setValue(0)
        self.input2DM.setValue(0)
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        self.selPushingit2.setChecked(False)
    
    def input1skill_valueChanged(self):
        '''
        A skill level was entered.
        Add it to the DM total.
        '''
        
        # reset the screen
        self.input1DM.setValue(0)
        self.selPushingit1.setChecked(False)
        if self.pushingit1:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value() + 1))
        else:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value()))
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        log.debug('Skill level set at: %d' % self.input1skill.value())
    
    def input2skill_valueChanged(self):
        '''
        A skill level was entered (defending).
        Add it to the DM total.
        '''
        
        # reset the screen
        self.input2DM.setValue(0)
        self.selPushingit2.setChecked(False)
        if self.pushingit2:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value() + 1))
        else:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value()))
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        log.debug('Defending Skill level set at: %d' % self.input2skill.value())
        
    def input1DM_valueChanged(self):
        '''
        A DM was entered.
        Add it to the DM total.
        '''
        
        # reset the screen
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        self.selPushingit1.setChecked(False)
        if self.pushingit1:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value() + 1))
        else:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value()))
    
    def input2DM_valueChanged(self):
        '''
        A DM was entered (defending).
        Add it to the DM total.
        '''
        
        # reset the screen
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        self.selPushingit2.setChecked(False)
        if self.pushingit2:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value() + 1))
        else:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value()))
        
    def selPushingit1_valueChanged(self):
        '''
        Action might be being pushed.
        Add 1 to DM if so.
        '''
        self.pushingit1 = self.selPushingit1.isChecked()
        if self.pushingit1:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value() + 1))
        else:
            self.total1DM.setText(str(self.input1skill.value() + self.input1DM.value()))

        # reset the screen
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
    
    def selPushingit2_valueChanged(self):
        '''
        Action might be being pushed (defending).
        Add 1 to DM if so.
        '''
        self.pushingit2 = self.selPushingit2.isChecked()
        if self.pushingit2:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value() + 1))
        else:
            self.total2DM.setText(str(self.input2skill.value() + self.input2DM.value()))

        # reset the screen
        self.roll1result.setText('')
        self.prompt1.setText('')
        self.harm1.setText('')
        self.roll2result.setText('')
        self.prompt2.setText('')
        self.harm2.setText('')
        
    def rollButtonClicked(self):
        '''
        Roll the dice.
        '''
        self.roll1_type = str(self.input1dice.value()) + 'd6h1'
        self.action1_roll = roll(self.roll1_type)
        log.debug('Action Roll %s: %d' % (self.roll1_type, self.action1_roll))
        if self.pushingit1:
            self.total1_rolled = self.action1_roll + self.input1skill.value() + self.input1DM.value() + 1
        else:
            self.total1_rolled = self.action1_roll + self.input1skill.value() + self.input1DM.value()
        self.roll1result.setText(str(self.total1_rolled))
        if self.target_num >= 1 and self.target_num <= 10:
            self.roll1_prompt = self.total1_rolled - self.target_num
            if self.roll1_prompt <= -2:
                self.prompt1index = 0
            if self.roll1_prompt == -1:
                self.prompt1index = 1
            if self.roll1_prompt == 0:
                self.prompt1index = 2
            if self.roll1_prompt == 1:
                self.prompt1index = 3
            if self.roll1_prompt >= 2:
                self.prompt1index = 4
            self.prompt1.setText('%d: %s' % (self.roll1_prompt, self.prompts[self.prompt1index]))
            if self.pushingit1:
                temp = 'Harm 1'
                if self.prompts[self.prompt1index][0:6] == 'NO AND':
                    temp += ', incapacited for ' + str(roll('1d6')) + ' minutes'
                self.harm1.setText(temp)
        elif self.target_num == 13:
            self.roll1_prompt = self.total1_rolled
            if self.roll1_prompt > 11:
                self.roll1_gradiated = 9
            else:
                self.roll1_gradiated = self.roll1_prompt - 2
            self.dls = ['DL 1 = Simple',
                        'DL 2 = Easy',
                        'DL 3 = Challenging',
                        'DL 4 = Difficult',
                        'DL 5 = Hard',
                        'DL 6 = Very Hard',
                        'DL 7 = Unlikely',
                        'DL 8 = Ridiculous',
                        'DL 9 = Absurd',
                        'DL 10 = Insane']
            if self.roll1_prompt == 1:
                self.prompt1.setText('')
            else:
                self.prompt1.setText(self.dls[self.roll1_gradiated])
            if self.pushingit1:
                temp = 'Harm 1'
                self.harm1.setText(temp)
        elif self.target_num == 14:
            # Defending Roll...
            self.roll2_type = str(self.input2dice.value()) + 'd6h1'
            self.action2_roll = roll(self.roll2_type)
            log.debug('Defending Roll being made %s: %d' % (self.roll2_type, self.action2_roll))
            if self.pushingit2:
                self.total2_rolled = self.action2_roll + self.input2skill.value() + self.input2DM.value() + 1
            else:
                self.total2_rolled = self.action2_roll + self.input2skill.value() + self.input2DM.value()
            self.roll2result.setText(str(self.total2_rolled))
            self.prompt2.setText('DL %d' % self.total2_rolled)
            # ...becomes DL for Active Roll to beat
            self.DL_roll = self.total2_rolled
            self.roll1_prompt = self.total1_rolled - self.DL_roll
            if self.roll1_prompt <= -2:
                self.prompt1index = 0
            if self.roll1_prompt == -1:
                self.prompt1index = 1
            if self.roll1_prompt == 0:
                self.prompt1index = 2
            if self.roll1_prompt == 1:
                self.prompt1index = 3
            if self.roll1_prompt >= 2:
                self.prompt1index = 4
            self.prompt1.setText('%d: %s' % (self.roll1_prompt, self.prompts[self.prompt1index]))
            if self.pushingit1:
                temp = 'Harm 1'
                if self.prompts[self.prompt1index][0:6] == 'NO AND':
                    temp += ', incapacited for ' + str(roll('1d6')) + ' minutes'
                self.harm1.setText(temp)
            if self.pushingit2:
                temp = 'Harm 1'
                self.harm2.setText(temp)

    def clearall_buttonClicked(self):
        '''
        Clear all the fields
        '''
        log.debug('Clear all fields')
        self.target_num = 0
        self.selDiff.setCurrentIndex(self.target_num)
        self.unknown = False
        self.rollInput.clear()
        self.rollBrowser.clear()

    def Visit_Blog(self):
        '''
        open web browser to blog URL
        '''
        os.startfile('http://shawndriscoll.blogspot.com')
        
    def Feedback(self):
        '''
        open an email letter to send as feedback to the author
        '''
        os.startfile('mailto:shawndriscoll@hotmail.com?subject=Feedback: ' + __app__)
        
    def Overview_menu(self):
        '''
        open this app's PDF manual
        '''
        log.info(__app__ + ' looking for PDF manual...')
        os.startfile('core_micro_dieroller_manual.pdf')
        log.info(__app__ + ' found PDF manual. Opening...')
        
    def actionAbout_triggered(self):
        '''
        open the About window
        '''
        log.info(__app__ + ' show about...')
        self.popAboutDialog.show()
    
    def manual_roll(self):
        '''
        A roll was inputed manually
        '''
        log.debug('Manually entered')
        dice_entered = self.rollInput.text()
        roll_returned = roll(dice_entered)
        if roll_returned == -9999:
            returned_line = dice_entered + ' = ' + '<span style=" color:#ff0000;">' + str(roll_returned) + '</span>'
        else:
            returned_line = dice_entered + ' = ' + str(roll_returned)
        self.rollBrowser.append(returned_line)

    def clearRollHistoryClicked(self):
        '''
        Clear the roll history
        '''
        log.debug('Clear roll history')
        self.rollInput.clear()
        self.rollBrowser.clear()
    
    def alert_window(self):
        '''
        open the Alert window
        '''
        log.warning(__app__ + ' show Beta expired PyQt5 alertDialog...')
        self.popAlertDialog.show()

    def quitButton_clicked(self):
        '''
        select "Quit" from the drop-down menu
        '''
        log.info(__app__ + ' quiting...')
        log.info(__app__ + ' DONE.')
        self.close()


if __name__ == '__main__':

    '''
    Technically, this program starts right here when run.
    If this program is imported instead of run, none of the code below is executed.
    '''

#     logging.basicConfig(filename = 'COREMicro.log',
#                         level = logging.DEBUG,
#                         format = '%(asctime)s %(levelname)s %(name)s - %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filemode = 'w')

    log = logging.getLogger('COREMicro')
    log.setLevel(logging.DEBUG)

    if not os.path.exists('Logs'):
        os.mkdir('Logs')
    
    fh = logging.FileHandler('Logs/COREMicro.log', 'w')
 
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s', datefmt = '%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    log.addHandler(fh)

    log.info('Logging started.')
    log.info(__app__ + ' starting...')

    trange = time.localtime()

    log.info(__app__ + ' started, and running...')
    
    if len(sys.argv) < 2:

        if trange[0] > 2024 or trange[1] > 12:
            __expired_tag__ = True
            __app__ += ' [EXPIRED]'

        app = QApplication(sys.argv)
        
        # Use print(QStyleFactory.keys()) to find a setStyle you like, instead of 'Fusion'

        # app.setStyle('Fusion')
        
        # darkPalette = QPalette()
        # darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        # darkPalette.setColor(QPalette.WindowText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        # darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        # darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        # darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        # darkPalette.setColor(QPalette.Text, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        # darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        # darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        # darkPalette.setColor(QPalette.ButtonText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        # darkPalette.setColor(QPalette.BrightText, Qt.red)
        # darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        # darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        # darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        # darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        # darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))
        
        mainApp = MainWindow()
        mainApp.show()

        # app.setPalette(darkPalette)

        #CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        #print(CURRENT_DIR)       

        app.exec_()
    
    elif trange[0] > 2024 or trange[1] > 12:
        __app__ += ' [EXPIRED]'
        '''
        Beta for this app has expired!
        '''
        log.warning(__app__)
        print()
        print(__app__)
        
    elif sys.argv[1] in ['-h', '/h', '--help', '-?', '/?']:
        print()
        print('     Using the CMD prompt to make dice rolls:')
        print("     C:\>core_micro_dieroller.py roll('2d6')")
        print()
        print('     Or just:')
        print('     C:\>core_micro_dieroller.py 2d6')
    elif sys.argv[1] in ['-v', '/v', '--version']:
        print()
        print('     CORE Micro DieRoller, release version ' + __version__ + ' for Python ' + __py_version__)
    else:
        print()
        dice = ''
        if len(sys.argv) > 2:
            for i in range(len(sys.argv)):
                if i > 0:
                    dice += sys.argv[i]
        else:
            dice = sys.argv[1]
        if "roll('" in dice:
            num = dice.find("')")
            if num != -1:
                dice = dice[6:num]
                dice = str(dice).upper().strip()
                if dice == '':
                    dice = '2D6'
                    log.debug('Default roll was made')
                num = roll(dice)
                if dice != 'TEST' and dice != 'INFO':
                    print("Your '%s' roll is %d." % (dice, num))
                    log.info("The direct call to CORE Micro DieRoller with '%s' resulted in %d." % (dice, num))
                elif dice == 'INFO':
                    print('CORE Micro DieRoller, release version ' + __version__ + ' for Python ' + __py_version__)
            else:
                print('Typo of some sort --> ' + dice)
        else:
            dice = str(dice).upper().strip()
            if dice == 'ROLL()':
                dice = '2D6'
                log.debug('Default roll was made')
            num = roll(dice)
            if dice != 'TEST' and dice != 'INFO':
                print("Your '%s' roll is %d." % (dice, num))
                log.info("The direct call to CORE Micro DieRoller with '%s' resulted in %d." % (dice, num))
            elif dice == 'INFO':
                print('CORE Micro DieRoller, release version ' + __version__ + ' for Python ' + __py_version__)

'''
Created on 30.12.2018

@author: ED
'''

if __name__ == '__main__':
    pass

import PyTrinamic
from PyTrinamic.connections.SerialInterface import SerialInterface
from PyTrinamic.modules.TMCM_0010_OPC import TMCM_0010_OPC

PyTrinamic.showInfo()
PyTrinamic.showAvailableComPorts()

myInterface = SerialInterface('COM5')
brakeChopper = TMCM_0010_OPC(myInterface)

" enable break chopper "
myInterface.setAndStoreAxisParameter(brakeChopper.AP_Enable, 0, 1)

" set voltage limit to 50V and hysteresis to 1V"
myInterface.setAndStoreAxisParameter(brakeChopper.AP_VoltageLimit, 0, 500)
myInterface.setAndStoreAxisParameter(brakeChopper.AP_Hysteresis, 0, 10)

" show new config "
brakeChopper.showConfiguration()

myInterface.close()
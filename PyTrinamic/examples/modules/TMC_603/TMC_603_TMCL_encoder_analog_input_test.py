#!/usr/bin/env python3
'''
Created on 07.02.2020

@author: JM
'''

if __name__ == '__main__':
    pass

import time
import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMC603.TMC_603 import TMC_603

PyTrinamic.showInfo()
connectionManager = ConnectionManager()
myInterface = connectionManager.connect()

module = TMC_603(myInterface)

"""
    Define all motor configurations for the the TMC-603.

    The configuration is based on our standard BLDC motor (QBL4208-61-04-013-1024-AT).
    If you use a different motor be sure you have the right configuration setup otherwise the script may not working.
"""

" motor configuration "
module.setMotorPoles(4)
module.setMaxTorque(2000)
module.showMotorConfiguration()

" hall configuration "
module.setHallInvert(0)
module.showHallConfiguration()

" encoder configuration "
module.setOpenLoopTorque(1500)
module.setEncoderResolution(2048)
module.setEncoderDirection(0)
module.setEncoderInitMode(module.ENUMs.ENCODER_INIT_MODE_1)
module.showEncoderConfiguration()

" motion settings "
module.setMaxVelocity(2048)
module.setAcceleration(10000)
module.setRampEnabled(1)
module.setTargetReachedVelocity(500)
module.setTargetReachedDistance(5)
module.showMotionConfiguration()

" PI configuration "
module.setTorquePParameter(600)
module.setTorqueIParameter(600)
module.setVelocityPParameter(800)
module.setVelocityIParameter(600)
module.setPositionPParameter(300)
module.showPIConfiguration()

" set commutation mode to FOC based on hall sensor signals "
module.setCommutationMode(module.ENUMs.COMM_MODE_FOC_ENCODER)

" read adc value and compute new target velocity "
while True:
    adcValue = module.analogInput(0)
    targetVelocity = (adcValue - 1024) * 2
    module.rotate(targetVelocity)
    print("adc value: " + str(adcValue) + " target velocity: " + str(targetVelocity) + " actual velocity: " + str(module.actualVelocity()))
    time.sleep(0.2)

print("Ready.")
myInterface.close()
'''
using MODULE_1161 to connect to two 1161 modules each connected to 1 motor
move both and print position while moving
if reset is true both will move every time the file is executed.
if reset is false, both will run on the first execution then only one moves on every execution.

Created on 17.07.2020
@author: AT
Asyncio routine adapted for python 3.6, might not work in python 3.8
'''
import asyncio
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM1161.TMCM_1161 import TMCM_1161


async def move(ax, mode, to, at, id=''):
    old_position = ax.getActualPosition()
    print(f'{id} was at {old_position}')
    if mode == 'abs':
        ax.moveTo(to, at)
    elif mode == 'rel':
        ax.moveBy(to, at)
    else:
        print('unknown mode')
        return
    while not ax.positionReached():
        print(id, ax.getActualPosition())
        await asyncio.sleep(0.25)
    await asyncio.sleep(0.02)
    print(id, ax.getActualPosition())




if __name__ == '__main__':
    connectionManager = ConnectionManager(argList='--port 0')
    connectionManager2 = ConnectionManager(argList='--port 1')

    x = TMCM_1161(connectionManager.connect())
    y = TMCM_1161(connectionManager2.connect())

    reset = False
    # stop motors before setActualPosition (data sheet p76/110, table 15)
    if reset:
        x.stop()
        y.stop()
        x.setActualPosition(0)
        y.setActualPosition(0)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        move(x, 'rel', 50000, 1000, 'x'),
        move(y, 'abs', -50000, 1000, 'y'),
    ))
    loop.close()


    if x.positionReached() and y.positionReached():
        print('Finished successfully')
        x.stop()
        y.stop()

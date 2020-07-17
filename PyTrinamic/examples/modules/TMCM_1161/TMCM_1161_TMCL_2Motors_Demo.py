'''
Move two motors using rotate and monitoring position value.
Buggy since this way of controlling target position is not precise

Created on 17.07.2020

@author: AT
Asyncio routin adapted for python 3.6
'''

import asyncio
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM1161.TMCM_1161 import TMCM_1161


async def move(ax, to, at, id=''):
    if at > 2047:
        at = 2047
    if at < 0:
        if at > 2047:
            at = -at
        else:
            at = -2047

    if to < ax.getActualPosition():
        to = -to
        at = - at
    print(f'to {to} at {at}')
    ax.rotate(at)
    while True:
        p = ax.getActualPosition()

        if abs(p) + 250 >= to:
            ax.stop()
            break
        print(id, p)
        await asyncio.sleep(0.01)
    print(id, p)
    print(id, ax.getActualPosition())


if __name__ == '__main__':

    connectionManager = ConnectionManager(argList='--port 0')
    connectionManager2 = ConnectionManager(argList='--port 1')

    x = TMCM_1161(connectionManager.connect())
    y = TMCM_1161(connectionManager2.connect())

    x.setMaxAcceleration(1000)
    y.setMaxAcceleration(1000)
    x.setActualPosition(0)
    y.setActualPosition(0)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        move(x, 50000, 1000, 'x'),
        move(y, -50000, 1000, 'y'),
    ))
    loop.close()

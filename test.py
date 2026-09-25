import gdsfactory as gf

from technology.pdk import AN800_PDK

from blocks.ring_test_block import ring_array
from components.heater_pad import heater_pad

AN800_PDK.activate()

c = heater_pad()

c.draw_ports()
c.show()
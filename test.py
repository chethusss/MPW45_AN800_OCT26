import gdsfactory as gf

from technology.pdk import AN800_PDK
from components.pring import ring_resonator
from blocks.ring_test_block import ring_array

AN800_PDK.activate()

c = ring_array()

c.draw_ports()
c.show()
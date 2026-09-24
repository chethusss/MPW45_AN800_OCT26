import gdsfactory as gf

from technology.pdk import AN800_PDK

from blocks.ring_test_block import ring_array

AN800_PDK.activate()

c = ring_array()

c.draw_ports()
c.show()
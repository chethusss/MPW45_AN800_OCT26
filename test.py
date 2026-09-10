import gdsfactory as gf

from technology.pdk import AN800_PDK
from components.amzi_comp import x_amzi
from components.BB_import import MMI2x2
from blocks.amzi_test_block import amzi_block
AN800_PDK.activate()

c = amzi_block()

c.draw_ports()
c.show()
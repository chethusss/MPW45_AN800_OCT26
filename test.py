import gdsfactory as gf

from technology.pdk import AN800_PDK
from components.pring import ring_resonator
from components.bent_coupler import broadband_dc_withbends, broadband_dc_withbendsR, broadband_dc_withbendsL
from blocks.bbdc_amzi_block import bbdc_amzi_block

AN800_PDK.activate()

c = bbdc_amzi_block()

c.draw_ports()
c.show()
import gdsfactory as gf

from technology.pdk import AN800_PDK
from components.pring import ring_resonator
from components.bent_coupler import broadband_dc_withbends, broadband_dc_withbendsR, broadband_dc_withbendsL
from blocks.mzi_lattice_test import mzilatticetest

AN800_PDK.activate()

c = mzilatticetest()

c.draw_ports()
c.show()
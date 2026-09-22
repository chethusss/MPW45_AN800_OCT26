import gdsfactory as gf
import numpy as np

from technology.pdk import AN800_PDK
from blocks.spiral_block import spiral_block
from blocks.amzi_test_block import amzi_block
from blocks.ring_test_block import ring_array
from blocks.mzi_lattice_test import mzilatticetest


# ----------------------------------------------------------
# Activate AN800 PDK - custom made
# ----------------------------------------------------------

AN800_PDK.activate()


# ----------------------------------------------------------
# Top-level chip
# ----------------------------------------------------------

chip = gf.Component()

pic_5a = gf.Component()
pic_5b = gf.Component()


# ----------------------------------------------------------
# Chip dimensions
# ----------------------------------------------------------

csl_x = 5210
csl_y = 4870

chs_x = 5190
chs_y = 4850

top_csl_x = 2 * csl_x + 100


# ----------------------------------------------------------
# CSL layer
# ----------------------------------------------------------

csl = chip.add_polygon(
    [(0, 0),(top_csl_x, 0),(top_csl_x, csl_y),(0, csl_y)],layer="CSL")


# ----------------------------------------------------------
# CHS blocks
# ----------------------------------------------------------

chs_pic_5a = pic_5a.add_polygon(
    [(10, 10),(10 + chs_x, 10),(10 + chs_x, 10 + chs_y),(10, 10 + chs_y)],layer="CHS")

chs_pic_5b = pic_5b.add_polygon(
    [(10, 10),(10 + chs_x, 10),(10 + chs_x, 10 + chs_y),(10, 10 + chs_y)],layer="CHS")


# ----------------------------------------------------------
# Spiral test structure
# ----------------------------------------------------------

spiraltest = pic_5b.add_ref(
    spiral_block()
)
shift1 = 1200 + 280
spiraltest.move(
    spiraltest.ports["ref1"].center,
    (0, csl_y - shift1 + 127*5),
)


AMZItest1 = pic_5a.add_ref(
    amzi_block()
)

AMZItest1.move(
    (10, 800),
)
Ring_block = pic_5a.add_ref(ring_array())
Ring_block.move(origin=Ring_block.ports["ref1"].center,destination=(10,AMZItest1.ports["ref1"].y+127*31))


mzilattest = pic_5b.add_ref(mzilatticetest())
mzilattest.move(
    mzilattest.ports["ref"].center,
    (10, csl_y - shift1),
)

# ----------------------------------------------------------
# Add PIC blocks to chip
# ----------------------------------------------------------

chip.add_ref(pic_5a)
chip.add_ref(pic_5b)


# ----------------------------------------------------------
# Position PIC 5b
# ----------------------------------------------------------

pic_5b.move(
    [chs_x + 120, 0]
)


# ----------------------------------------------------------
# Show chip
# ----------------------------------------------------------

chip.show()
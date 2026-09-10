from gdsfactory.technology import LayerMap
from gdsfactory.typings import Layer


class MPW45LayerMap(LayerMap):
    ALLB: Layer = (0, 1)
    CELLNAME: Layer = (15, 2)
    CELLSIZE: Layer = (13, 2)

    CHS: Layer = (100, 0)
    CSL: Layer = (100, 2)
    EXCPT: Layer = (0, 3)
    FPIN: Layer = (101, 2)

    LC1: Layer = (50, 0)
    LC2: Layer = (51, 0)
    LCS: Layer = (60, 0)

    M1B: Layer = (40, 1)
    M1PAD: Layer = (41, 0)
    M1PIN: Layer = (40, 2)
    M1P: Layer = (40, 0)

    P1B: Layer = (30, 1)
    P1PAD: Layer = (33, 0)
    P1PIN: Layer = (30, 2)
    P1P: Layer = (30, 0)

    P1RB: Layer = (32, 1)
    P1R: Layer = (32, 0)

    RIBA: Layer = (10, 4)
    RIBC: Layer = (10, 0)

    TRN: Layer = (100, 4)
    VIA: Layer = (31, 0)

    X1B: Layer = (2, 1)
    X1PIN: Layer = (2, 2)
    X1P: Layer = (2, 0)

    X2B: Layer = (20, 1)
    X2PIN: Layer = (20, 2)
    X2P: Layer = (20, 0)


LAYER = MPW45LayerMap
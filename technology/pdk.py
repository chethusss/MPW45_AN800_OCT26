import gdsfactory as gf

from technology.layer_map import LAYER
from technology.cross_sections import (
    x_strip_lig,
    x_strip_spir,
    x1p_width_taper,
)


AN800_PDK = gf.Pdk(
    name="AN800_PDK",
    layers=LAYER,
    cross_sections={
        "SM": x_strip_lig,
        "MM": x_strip_spir,
    },
    cells={
        "straight": gf.components.straight,
        "bend_euler": gf.components.bend_euler,
        "bend_s": gf.components.bend_s,
    },
    layer_transitions={
        LAYER.X1P: x1p_width_taper,
    },
)
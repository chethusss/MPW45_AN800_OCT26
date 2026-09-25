import gdsfactory as gf

from technology.layer_map import LAYER


def x_strip_lig(
    width: float = 1.0,
    radius: float = 50.0,
):
    return gf.cross_section.cross_section(
        width=width,
        layer=LAYER.X1P,
        radius=radius,
    )


def x_strip_spir(
    width: float = 2.3,
    radius: float = 50.0,
):
    return gf.cross_section.cross_section(
        width=width,
        layer=LAYER.X1P,
        radius=radius,
    )

def p1p_strip(
    width: float = 2.0,
    radius: float = 50.0,
):
    return gf.cross_section.cross_section(
        width=width,
        layer=LAYER.P1P,
        radius=radius,
    )

def x1p_width_taper(
    length=300.0,
    width1=1.0,
    width2=2.3,
):
    return gf.components.taper(
        length=length,
        width1=width1,
        width2=width2,
        layer = LAYER.X1P,
    )

def p1p_width_taper(
    length=300.0,
    width1=1.0,
    width2=2.3,
):
    return gf.components.taper(
        length=length,
        width1=width1,
        width2=width2,
        layer = LAYER.P1P,
    )
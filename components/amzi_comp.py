import gdsfactory as gf
import numpy as np
from components.BB_import import MMI2x2
from components.spirals import x_double_spiral

@gf.cell
def x_amzi(
    L=3000,
    n=5,
    radius=250,
    spacing=3,
    X1=2000,
    X2=3000,
    Y2=-110,
):
    c = gf.Component()

    # ==========================================================
    # MMI 1
    # ==========================================================

    mmi1 = c << MMI2x2()

    # MMI1 is the reference position
    mmi1.move(
        mmi1.ports["o1"].center,
        (0, 0),
    )

    # ==========================================================
    # MMI 2
    # Place MMI2 at horizontal offset X1 from MMI1.o1
    # ==========================================================

    mmi2 = c << MMI2x2()

    mmi2.move(
        mmi2.ports["o1"].center,
        (
            X1,
            0,
        ),
    )

    # ==========================================================
    # Double spiral
    # Place spiral.o1 at (X2, Y2) relative to MMI1.o1
    # ==========================================================

    spiral = c << x_double_spiral(
        L=L,
        n=n,
        radius=radius,
        spacing=spacing,
    )

    spiral.move(
        spiral.ports["o1"].center,
        (
            X2,
            Y2,
        ),
    )

    # ==========================================================
    # Reference arm - TOP
    #
    # MMI1.o3 -> MMI2.o1
    # ==========================================================

    reference_length = (
        mmi2.ports["o1"].center[0]
        - mmi1.ports["o3"].center[0]
    )

    reference = c << gf.components.straight(
        length=reference_length,
        cross_section="SM",
    )

    reference.connect(
        "o1",
        mmi1.ports["o3"],
    )

    # ==========================================================
    # Delay arm - BOTTOM
    #
    # MMI1.o4 -> spiral.o1
    # spiral.o2 -> MMI2.o2
    # ==========================================================

    route1 = gf.routing.route_single(
        c,
        port1=mmi1.ports["o4"],
        port2=spiral.ports["o2"],
        cross_section="SM",
    )

    route2 = gf.routing.route_single(
        c,
        port1=spiral.ports["o1"],
        port2=mmi2.ports["o2"],
        cross_section="SM",
    )
    # ==========================================================
    # External AMZI ports
    #
    # MMI1 left side  -> inputs
    # MMI2 right side -> outputs
    # ==========================================================

    c.add_port(
        name="o1",
        port=mmi1.ports["o1"],
    )

    c.add_port(
        name="o2",
        port=mmi1.ports["o2"],
    )

    c.add_port(
        name="o3",
        port=mmi2.ports["o3"],
    )

    c.add_port(
        name="o4",
        port=mmi2.ports["o4"],
    )

    return c
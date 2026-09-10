import gdsfactory as gf

from components.amzi_comp import x_amzi
from components.BB_import import exspot_packaging


@gf.cell
def amzi_block(
    # ==========================================================
    # Edge coupler array
    # ==========================================================
    pitch=127.0,

    # ==========================================================
    # AMZI position
    #
    # AMZI.o1 is positioned at (X0, Y0) relative to
    # the first edge coupler.
    # ==========================================================
    X0=500.0,
    Y0=200.0,

    # ==========================================================
    # x_amzi variables
    # ==========================================================
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
    # 4 edge couplers
    #
    # All couplers are flipped about the Y axis.
    # Their o2 ports are aligned on x = 0.
    # ==========================================================

    exspot1 = c << exspot_packaging()
    exspot2 = c << exspot_packaging()
    exspot3 = c << exspot_packaging()
    exspot4 = c << exspot_packaging()

    # Flip all edge couplers about the Y axis
    exspot1.mirror(p1=(0, 0), p2=(0, 1))
    exspot2.mirror(p1=(0, 0), p2=(0, 1))
    exspot3.mirror(p1=(0, 0), p2=(0, 1))
    exspot4.mirror(p1=(0, 0), p2=(0, 1))

    # Align o2 ports vertically at x = 0
    exspot1.move(
        origin=exspot1.ports["o2"].center,
        destination=(0, 0),
    )

    exspot2.move(
        origin=exspot2.ports["o2"].center,
        destination=(0, pitch),
    )

    exspot3.move(
        origin=exspot3.ports["o2"].center,
        destination=(0, 2 * pitch),
    )

    exspot4.move(
        origin=exspot4.ports["o2"].center,
        destination=(0, 3 * pitch),
    )
    # ==========================================================
    # AMZI
    # ==========================================================

    amzi = c << x_amzi(
        L=L,
        n=n,
        radius=radius,
        spacing=spacing,
        X1=X1,
        X2=X2,
        Y2=Y2,
    )

    # ==========================================================
    # Position AMZI
    #
    # AMZI.o1 is placed at:
    #
    #   EXSPOT1.o1 + (X0, Y0)
    # ==========================================================

    amzi.move(
        origin=amzi.ports["o1"].center,
        destination=(
            exspot1.ports["o1"].center[0] + X0,
            exspot1.ports["o1"].center[1] + Y0,
        ),
    )

    # ==========================================================
    # Route AMZI ports to edge couplers
    # ==========================================================

    route1 = gf.routing.route_single(
        c,
        port1=amzi.ports["o2"],
        port2=exspot1.ports["o1"],
        cross_section="SM",
    )

    route2 = gf.routing.route_single(
        c,
        port1=amzi.ports["o1"],
        port2=exspot2.ports["o1"],
        cross_section="SM",
    )

    route3 = gf.routing.route_single(
        c,
        port1=amzi.ports["o4"],
        port2=exspot3.ports["o1"],
        cross_section="SM",
        )
    route4 = gf.routing.route_single(
        c,
        port1=amzi.ports["o3"],
        port2=exspot4.ports["o1"],
        steps=[
            {"x": amzi.ports["o3"].center[0] + 70},
            {"y": exspot4.ports["o1"].center[1]},
        ],
        cross_section="SM",
    )

    return c
import gdsfactory as gf

from components.amzi_comp import x_amzi
from components.BB_import import exspot_packaging, PBS


@gf.cell
def amzi_block():

    pitch=127.0
    X0=1000.0
    L=4000
    n=6
    radius=250
    spacing=3
    X1=1000
    X2=1900-330
    Y2=-120
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
    exspot5 = c << exspot_packaging()

    # Flip all edge couplers about the Y axis
    exspot1.mirror(p1=(0, 0), p2=(0, 1))
    exspot2.mirror(p1=(0, 0), p2=(0, 1))
    exspot3.mirror(p1=(0, 0), p2=(0, 1))
    exspot4.mirror(p1=(0, 0), p2=(0, 1))
    exspot5.mirror(p1=(0, 0), p2=(0, 1))

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

    exspot5.move(
        origin=exspot5.ports["o2"].center,
        destination=(0, 4 * pitch),
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
    pbs_1 = c<<PBS()
    pbs_1.move(         
        origin=pbs_1.ports["o3"].center,
        destination=(
            exspot1.ports["o1"].center[0]+X0,
            exspot1.ports["o1"].center[1] 
        ))
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
            pbs_1.ports["o3"].center[0] + X0,
            pbs_1.ports["o3"].center[1] ,
        ),
    )


    pbs_2 = c<<PBS()
    pbs_2.mirror_x()
    pbs_2.move(         
        origin=pbs_2.ports["o1"].center,
        destination=(
            pbs_1.ports["o2"].center[0],
            pbs_1.ports["o2"].center[1]+200
        ))

    pbs_3 = c<<PBS()
    pbs_3.mirror_x()
    pbs_3.move(         
        origin=pbs_3.ports["o1"].center,
        destination=(
            pbs_2.ports["o2"].center[0]-250,
            pbs_2.ports["o2"].center[1]+195
        ))

    gf.routing.route_single(
    c,
    port1=pbs_1.ports["o1"],
    port2=exspot1.ports["o1"],
    cross_section="SM",
    )

    gf.routing.route_single(
    c,
    port1=pbs_1.ports["o3"],
    port2=amzi.ports["o1"],
    cross_section="SM",
    )

    
    gf.routing.route_single(
    c,
    port1=pbs_1.ports["o2"],
    port2=exspot2.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": 50},
            {"dy": 120},
            {"dx": -500},
            {"y":exspot2.ports["o1"].y-100},
            {"dx":-100},
            {"y":exspot2.ports["o1"].y}
        ]
    )

    gf.routing.route_single(
    c,
    port1=amzi.ports["o4"],
    port2=pbs_2.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": 90},
            {"dy": -100},
            {"dx": 220},
            {"y":amzi.ymax+40},
            {"x":pbs_1.ports["o2"].x+400},
            {"y":pbs_2.ports["o1"].y}
        ]
    )

    gf.routing.route_single(
    c,
    port1=amzi.ports["o3"],
    port2=exspot3.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": 100},
            {"dy": -100},
            {"dx": 100},
            {"y":amzi.ymax+20},
            {"x":pbs_1.ports["o2"].x+300},
            {"y":pbs_2.ports["o3"].y-20},
            {"dx":-700},
            {"dy":200},
            {"dx":-100},
            {"y":exspot3.ports["o1"].y},
        ]
    )
    gf.routing.route_single(
    c,
    port1=pbs_2.ports["o3"],
    port2=pbs_3.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": -100},
            {"y": pbs_3.ports["o1"].y}]
    )

    gf.routing.route_single(
    c,
    port1=pbs_2.ports["o2"],
    port2=exspot5.ports["o1"],
    cross_section="SM",
    )
    
    
    gf.routing.route_single(
    c,
    port1=pbs_3.ports["o3"],
    port2=exspot4.ports["o1"],
    cross_section="SM",
    )
    c.add_port(name="ref1", port=exspot1.ports["o2"])
    #########################################################################
    exspot6 = c << exspot_packaging()
    exspot7 = c << exspot_packaging()
    exspot8 = c << exspot_packaging()
    exspot9 = c << exspot_packaging()
    exspot10 = c << exspot_packaging()


    # Align o2 ports vertically at x = 0
    exspot6.move(
        origin=exspot6.ports["o2"].center,
        destination=(5190, exspot1.ports["o2"].y),
    )

    exspot7.move(
        origin=exspot7.ports["o2"].center,
        destination=(5190, exspot1.ports["o2"].y+pitch),
    )

    exspot8.move(
        origin=exspot8.ports["o2"].center,
        destination=(5190, exspot1.ports["o2"].y+2*pitch),
    )

    exspot9.move(
        origin=exspot9.ports["o2"].center,
        destination=(5190, exspot1.ports["o2"].y+3*pitch),
    )

    exspot10.move(
        origin=exspot10.ports["o2"].center,
        destination=(5190, exspot1.ports["o2"].y+4*pitch),
    )

    amzi2 = c << x_amzi(
        L=0.01,
        n=n,
        radius=radius,
        spacing=spacing,
        X1=350,
        X2=350,
        Y2=-110,)

    pbs_a1 = c<<PBS()
    pbs_a1.mirror_x()
    pbs_a1.move(         
        origin=pbs_a1.ports["o1"].center,
        destination=(
            exspot9.ports["o1"].center[0]-500,
            exspot9.ports["o1"].center[1]+250
        ))
    
    amzi2.mirror_x()
    amzi2.move(
        origin=amzi2.ports["o1"].center,
        destination=(
            pbs_a1.ports["o3"].center[0] - 300,
            pbs_a1.ports["o3"].center[1] +250,
        ),
    )


    pbs_a2 = c<<PBS()
    pbs_a2.move(         
        origin=pbs_a2.ports["o1"].center,
        destination=(
            pbs_a1.ports["o2"].center[0]-200,
            pbs_a1.ports["o2"].center[1]-200
        ))

    pbs_a3 = c<<PBS()
    pbs_a3.move(         
        origin=pbs_a3.ports["o1"].center,
        destination=(
            pbs_a2.ports["o2"].center[0]+200,
            pbs_a2.ports["o2"].center[1]-200
        ))
    gf.routing.route_single(
    c,
    port1=pbs_a1.ports["o1"],
    port2=exspot9.ports["o1"],
    cross_section="SM",
    )

    gf.routing.route_single(
    c,
    port1=pbs_a1.ports["o2"],
    port2=exspot10.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": -50},
            {"dy": 100},
            {"dx": 400},
            {"y":exspot10.ports["o1"].y},
        ]
    )
    gf.routing.route_single(
    c,
    port1=pbs_a1.ports["o3"],
    port2=amzi2.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": -200},
            {"y":amzi2.ports["o1"].y},
        ]
    )
    gf.routing.route_single(
    c,
    port1=amzi2.ports["o4"],
    port2=pbs_a2.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": -720},
            {"dy": -750},
            {"dx": 1200},
            {"y":pbs_a2.ports["o1"].y},
        ]
    )
    gf.routing.route_single(
    c,
    port1=amzi2.ports["o3"],
    port2=exspot6.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": -730},
            {"dy": -780},
            {"dx": 2120},
            {"dy":-175},
            {"dx":100},
            {"y":exspot6.ports["o1"].y},
        ]
    )
    gf.routing.route_single(
    c,
    port1=pbs_a2.ports["o3"],
    port2=pbs_a3.ports["o1"],
    cross_section="SM",
    )

    gf.routing.route_single(
    c,
    port1=pbs_a2.ports["o2"],
    port2=exspot8.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": 200},
            {"y": exspot8.ports["o1"].y}
        ]
    )

    gf.routing.route_single(
    c,
    port1=pbs_a3.ports["o3"],
    port2=exspot7.ports["o1"],
    cross_section="SM",
    steps=[ {"dx": 50},
            {"dy": -180},
            {"dx": 100},
            {"y": exspot7.ports["o1"].y}
        ]

    )
    return c



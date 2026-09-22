import gdsfactory as gf
from components.BB_import import exspot_packaging, PBS
from components.bent_coupler import broadband_dc
from blocks.exspot_array_block import exspot_array


@gf.cell
def bbdc_amzi(
    spacing=550.0,
    k=0.5,
    L=320,
) -> gf.Component:
    """
    BBDC-based AMZI using BBDC couplers without bends.

    Parameters
    ----------
    spacing : float
        Horizontal spacing between the output ports of BBDC1
        and the corresponding input ports of BBDC2.

    k : float
        Power coupling ratio of both BBDCs.

    L : float
        Additional delay length on the top arm.

    Ports
    -----
    i1, i2 : inputs of BBDC1
    o1, o2 : outputs of BBDC2
    """

    c = gf.Component()

    # ==========================================================
    # BBDC 1
    # ==========================================================

    bbdc1 = c << broadband_dc(
        k=k,
    )

    # ==========================================================
    # BBDC 2
    # ==========================================================

    bbdc2 = c << broadband_dc(
        k=k,
    )

    bend = c << gf.components.bend_euler(angle=180,cross_section="SM")
    sbend = c << gf.components.bend_s(size=(180,90), npoints=500, cross_section="SM")

    # ==========================================================
    # PLACE BBDC2
    # ==========================================================

    bbdc2.move(
        origin=bbdc2.ports["i1"].center,
        destination=(
            bbdc1.ports["o1"].center[0] + spacing,
            bbdc1.ports["o1"].center[1],
        ),
    )

    bend.move(origin=bend.ports["o1"].center,destination=(bbdc1.ports["o1"].center[0]+110+L+180,bbdc1.ports["o1"].center[1]-110))
    sbend.connect("o2",bend.ports["o2"])


    # ==========================================================
    # BOTTOM ARM
    #
    # BBDC1.o2 -> BBDC2.i2
    # ==========================================================

    gf.routing.route_single(
        component=c,
        port1=bbdc1.ports["o2"],
        port2=bbdc2.ports["i2"],
        cross_section="SM",
        bend="bend_euler",
    )

    gf.routing.route_single(
        component=c,
        port1=bbdc1.ports["o1"],
        port2=bend.ports["o1"],
        cross_section="SM",
        bend="bend_euler",
        steps=[
            {"dx": 50},
            {
             "dy":-110 
            }
        ])
    gf.routing.route_single(
        component=c,
        port1=sbend.ports["o1"],
        port2=bbdc2.ports["i1"],
        cross_section="SM",
        bend="bend_euler",
        steps=[
            {"dx": -L-50},
            {
             "dy":+100 
            }
        ])

    

    # ==========================================================
    # EXTERNAL PORTS
    # ==========================================================

    c.add_port(
        name="o2",
        port=bbdc1.ports["i1"],
    )

    c.add_port(
        name="o1",
        port=bbdc1.ports["i2"],
    )

    c.add_port(
        name="o4",
        port=bbdc2.ports["o1"],
    )

    c.add_port(
        name="o3",
        port=bbdc2.ports["o2"],
    )

    return c

@gf.cell
def bbdc_amzi_block(spacingx=500,spacingy = 200):
    c = gf.Component()
    ec = c << exspot_array(num=6)
    mzi1 = c << bbdc_amzi(k=0.1)
    mzi2 = c << bbdc_amzi(k=0.3)
    mzi3 = c << bbdc_amzi(k=0.5)
    mzi4 = c << bbdc_amzi(k=0.7)
    mzi5 = c << bbdc_amzi(k=0.9)

    eco7 = c << exspot_packaging()
    eco8 = c << exspot_packaging()
    eco9 = c << exspot_packaging()
    eco10 = c << exspot_packaging()
    eco11 = c << exspot_packaging()
    eco12 = c << exspot_packaging()

    pitch = 127
    eco7.move(origin = eco7.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*1))
    eco8.move(origin = eco8.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*2))
    eco9.move(origin = eco9.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*3))
    eco10.move(origin = eco10.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*4))
    eco11.move(origin = eco11.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*5))
    eco12.move(origin = eco12.ports["o1"].center, destination = (ec.ports["o6"].x,ec.ports["o6"].y-pitch*6))

    mzi1.move(origin=mzi1.ports["o1"].center, destination=(ec.ports["i1"].x+spacingx,ec.ports["i2"].y))
    mzi2.move(origin=mzi2.ports["o1"].center, destination=(ec.ports["i1"].x+2*spacingx,ec.ports["i2"].y-spacingy))
    mzi3.move(origin=mzi3.ports["o1"].center, destination=(ec.ports["i1"].x+3*spacingx,ec.ports["i2"].y))
    mzi4.move(origin=mzi4.ports["o1"].center, destination=(ec.ports["i1"].x+4*spacingx,ec.ports["i2"].y-spacingy))
    mzi5.move(origin=mzi5.ports["o1"].center, destination=(ec.ports["i1"].x+5*spacingx,ec.ports["i2"].y))


   
    c.add_port(name="ref",port=ec.ports["i1"],cross_section="SM")
    return c


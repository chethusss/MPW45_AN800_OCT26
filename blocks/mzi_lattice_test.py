import gdsfactory as gf

from technology.layer_map import LAYER
from technology.cross_sections import x_strip_lig
from components.BB_import import exspot_packaging, PBS
from blocks.mzi_lattice_combiner import mzilattice

@gf.cell
def mzilatticetest(yref=0) -> gf.Component:

    mzilat = gf.Component("MZI Lattice test struct")

    # ==========================================================
    # INVERTED TAPER / EDGE COUPLERS
    # ==========================================================

    inv_taper = exspot_packaging()
    tapersize = inv_taper.xsize

    N_edge_couplers = 4
    pitch_edge_couplers = 127

    N0_y_pos = yref

    taper_block = gf.Component(
        "test_structures_inverted_taper_block"
    )

    incouplers = [None] * N_edge_couplers
    outcouplers = [None] * N_edge_couplers

    for i in range(N_edge_couplers):

        incouplers[i] = taper_block << inv_taper
        incouplers[i].mirror()

        incouplers[i].move(
            origin=incouplers[i].ports["o1"].center,
            destination=(
                tapersize,
                N0_y_pos - pitch_edge_couplers * i,
            ),
        )

    mzilat << taper_block

    # ==========================================================
    # MZI LATTICE
    # ==========================================================

    lattice = mzilattice()
    lat = mzilat << lattice

    # Same transformation as the old structure
    lat.rotate(-90)

    lat.mirror(
        p1=(0, 0),
        p2=(1, 0),
    )

    # Same placement relative to the fourth edge coupler
    lat.move(
        origin=lat.ports["o1"].center,
        destination=(
            incouplers[3].ports["o1"].center[0] - 190,
            incouplers[3].ports["o1"].center[1] - 180,
        ),
    )

    pbs1 = mzilat << PBS()
    pbs1.move(
        origin=pbs1.ports["o1"].center,
        destination=(
            incouplers[1].ports["o1"].center[0] + 10,
            incouplers[1].ports["o1"].center[1],
        ),
    )

    # ==========================================================
    # ROUTES 1
    #
    # lattice o2 -> edge coupler 0
    # ==========================================================

    gf.routing.route_single(
        component=mzilat,
        port1=lat.ports["o1"],
        port2=pbs1.ports["o3"],
        bend="bend_euler",
        cross_section=x_strip_lig,
        steps=[
            {"dy": 50},
            {
                "x": incouplers[3].ports["o1"].center[0] + 80
            },
            {
                "y": pbs1.ports["o3"].center[1] - 100
            },
            {
                "x": pbs1.ports["o3"].center[0] + 50
            },
            {
                "y": pbs1.ports["o3"].center[1]
            },
        ],
    )

    gf.routing.route_single(
        component=mzilat,
        port1=pbs1.ports["o2"],
        port2=incouplers[0].ports["o1"],
        bend="bend_euler",
        cross_section=x_strip_lig,
    )

    gf.routing.route_single(
        component=mzilat,
        port1=pbs1.ports["o1"],
        port2=incouplers[1].ports["o1"],
        bend="bend_euler",
        cross_section=x_strip_lig,
    )


    # ==========================================================
    # ROUTE 3
    #
    # lattice i1 -> edge coupler 2
    # ==========================================================
    gf.routing.route_single(
        component=mzilat,
        port1=lat.ports["i2"],
        port2=incouplers[2].ports["o1"],
        bend="bend_euler",
        cross_section=x_strip_lig,
        steps=[
            {"dy": -50},
            {
                "x": lat.center[0] - lat.xsize / 2 - 20
            },
            {
                "y": incouplers[3].ports["o1"].center[1] - 110
            },
            {
                "x": incouplers[3].ports["o1"].center[0] + 60
            },
            {
                "y": incouplers[2].ports["o1"].center[1]
            },
        ],
    )

    # ==========================================================
    # ROUTE 4
    #
    # lattice i2 -> edge coupler 3
    # ==========================================================

    gf.routing.route_single(
        component=mzilat,
        port1=lat.ports["i1"],
        port2=incouplers[3].ports["o1"],
        bend="bend_euler",
        cross_section=x_strip_lig,
        steps=[
            {"dy": -60},
            {
                "x": lat.center[0] - lat.xsize / 2 - 40
            },
            {
                "y": incouplers[3].ports["o1"].center[1] - 100
            },
            {
                "x": incouplers[3].ports["o1"].center[0] + 50
            },
            {
                "y": incouplers[3].ports["o1"].center[1]
            },
        ],
    )

    # ==========================================================
    # REFERENCE PORT
    # ==========================================================

    mzilat.add_port(
        name="ref",
        port=incouplers[1].ports["o2"]
    )

    return mzilat
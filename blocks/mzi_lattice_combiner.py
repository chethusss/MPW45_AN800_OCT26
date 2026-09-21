import numpy as np
import gdsfactory as gf

from technology.layer_map import LAYER
from components.bent_coupler import (
    broadband_dc_withbends,
    broadband_dc_withbendsR,
    broadband_dc_withbendsL,
)

x_h = gf.cross_section.cross_section(
    width=2.0,
    layer=LAYER.P1P,
    radius=50.0,
)

def heater_route_segment(
    component,
    start,
    end,
    start_orientation,
    end_orientation,
):

    p1 = gf.Port(
        name="h1",
        center=start,
        orientation=start_orientation,
        width=2.0,
        layer=LAYER.P1P,
    )

    p2 = gf.Port(
        name="h2",
        center=end,
        orientation=end_orientation,
        width=2.0,
        layer=LAYER.P1P,
    )

    return gf.routing.route_single(
        component=component,
        port1=p1,
        port2=p2,
        cross_section=x_h,
        bend="bend_euler",
    )

@gf.cell
def mzilattice(
    yref=0,
    L=181.1,
    armstop=None,
    armsbot=None,
    kaps=None,
) -> gf.Component:
    """
    MZI lattice filter.

    Parameters
    ----------
    yref : float
        Reference y-coordinate.

    L : float
        Base arm length.

    armstop : list
        Relative lengths of the top arms.

    armsbot : list
        Relative lengths of the bottom arms.

    kaps : list
        Coupling coefficients of the directional couplers.
    """

    # ------------------------------------------------------------
    # Defaults
    # ------------------------------------------------------------

    if armstop is None:
        armstop = [1, 0, 0, 3]

    if armsbot is None:
        armsbot = [0, 3, 2, 0]

    if kaps is None:
        kaps = [0.28, 0.32, 0.9, 0.35, 0.03]

    order = len(kaps) - 1

    spacing = 450
    exl = 60

    # ------------------------------------------------------------
    # Create parent component
    # ------------------------------------------------------------

    lattice = gf.Component()

    # ------------------------------------------------------------
    # Reverse the arm definitions.
    #
    # This preserves the behavior of the original code.
    # ------------------------------------------------------------

    kappas = np.flip(np.array(kaps))

    lt = np.flip(np.array(armstop)) * L / 2
    lb = np.flip(np.array(armsbot)) * L / 2

    # ------------------------------------------------------------
    # Create the couplers
    # ------------------------------------------------------------

    couplers = [None] * (order + 1)

    for i in range(order + 1):

        if i == 0:

            couplers[i] = lattice << broadband_dc_withbendsR(
                k=float(kappas[i])
            )

        elif i == order:

            couplers[i] = lattice << broadband_dc_withbendsL(
                k=float(kappas[i])
            )

        else:

            couplers[i] = lattice << broadband_dc_withbends(
                k=float(kappas[i])
            )

    # ------------------------------------------------------------
    # Place the couplers
    #
    # i2 of the next coupler is placed spacing away from
    # o2 of the previous coupler.
    # ------------------------------------------------------------

    for i in range(1, order + 1):

        current = couplers[i].ports["i2"].center
        previous = couplers[i - 1].ports["o2"].center

        target = (
            previous[0] + spacing,
            previous[1],
        )

        couplers[i].move(
            origin=current,
            destination=target,
        )

    # ------------------------------------------------------------
    # Utility function for obtaining a port center
    # ------------------------------------------------------------

    def pcenter(ref, port_name):
        return ref.ports[port_name].center

    # ------------------------------------------------------------
    # ROUTING
    # ------------------------------------------------------------

    top_routes = []
    bottom_routes = []

    # Minimum distance between consecutive bends.
    # bend_euler in this configuration requires at least 2*b90r.
    min_dy = 100.0

    # ------------------------------------------------------------
    # Top arm
    # ------------------------------------------------------------

    for i in range(order):

        p1 = couplers[i].ports["o1"]
        p2 = couplers[i + 1].ports["i1"]

        x1, y1 = p1.center
        x2, y2 = p2.center

        extra_length = float(lt[i])

        if abs(extra_length) < 1e-9:

            route = gf.routing.route_single(
                component=lattice,
                port1=p1,
                port2=p2,
                cross_section="SM",
                bend="bend_euler",
            )

        else:

            # Top arm goes upward.
            #
            # 50 um is the base vertical offset.
            # L/2 contribution is already contained in lt[i].
            #
            dely = 50.0 + extra_length

            steps = [
                {"dy": dely},
                {"dx": x2 - x1},
            ]

            route = gf.routing.route_single(
                component=lattice,
                port1=p1,
                port2=p2,
                steps=steps,
                cross_section="SM",
                bend="bend_euler",
            )

        top_routes.append(route)


    # ------------------------------------------------------------
    # Bottom arm
    # ------------------------------------------------------------

    for i in range(order):

        p1 = couplers[i].ports["o2"]
        p2 = couplers[i + 1].ports["i2"]

        x1, y1 = p1.center
        x2, y2 = p2.center

        extra_length = float(lb[i])

        if abs(extra_length) < 1e-9:

            route = gf.routing.route_single(
                component=lattice,
                port1=p1,
                port2=p2,
                cross_section="SM",
                bend="bend_euler",
            )

        else:

            # Bottom arm goes downward.
            dely = - 50.0 - extra_length

            steps = [
                {"dy": dely},
                {"dx": x2 - x1},
            ]

            route = gf.routing.route_single(
                component=lattice,
                port1=p1,
                port2=p2,
                steps=steps,
                cross_section="SM",
                bend="bend_euler",
            )

        bottom_routes.append(route)

    top_heaters = []
    bottom_heaters = []

    for i in range(order):

        # ======================================================
        # TOP HEATER
        # ======================================================

        p1 = couplers[i].ports["o1"]

        x1, y1 = p1.center

        dy = float(lt[i])
        y_heater = y1 + dy

        top_heater = heater_route_segment(
            component=lattice,
            start=(x1, y_heater),
            end=(x1 + spacing, y_heater),
            start_orientation=90,
            end_orientation=90,
        )

        top_heaters.append(top_heater)


        # ======================================================
        # BOTTOM HEATER
        # ======================================================

        p1 = couplers[i].ports["o2"]

        x1, y1 = p1.center

        dy = -float(lb[i])
        y_heater = y1 + dy

        bottom_heater = heater_route_segment(
            component=lattice,
            start=(x1, y_heater),
            end=(x1 + spacing, y_heater),
            start_orientation=270,
            end_orientation=270,
        )

        bottom_heaters.append(bottom_heater)
    # ------------------------------------------------------------
    # External input ports
    #
    # First coupler:
    #
    # i1
    # i2
    # ------------------------------------------------------------

    first = couplers[0]

    lattice.add_port(
        name="i1",
        port=first.ports["i1"],
    )

    lattice.add_port(
        name="i2",
        port=first.ports["i2"],
    )

    # ------------------------------------------------------------
    # External output ports
    #
    # Last coupler:
    #
    # o1
    # o2
    # ------------------------------------------------------------

    last = couplers[-1]

    lattice.add_port(
        name="o1",
        port=last.ports["o1"],
    )

    lattice.add_port(
        name="o2",
        port=last.ports["o2"],
    )

    # ------------------------------------------------------------
    # Reference y position
    # ------------------------------------------------------------

    lattice.move(
        origin=(0, 0),
        destination=(0, yref),
    )

    return lattice
import gdsfactory as gf
import numpy as np

from components.gds_import import spiral_import
from components.BB_import import exspot_packaging


def bezier(
    npoints=600,
    ang=20,
    height=20,
    thick=20,
    thick1=20,
    wid1=1,
    wid2=2,
    s=-1,
    pref=np.array([[0], [0]]),
    slp1=0.6,
    slp2=0.5,
):
    thet = (np.pi / 180) * ang
    t = np.linspace(0, 1, npoints)

    wdb = wid2 + t * (wid1 - wid2)

    p1 = np.array([[0], [0]]) + pref

    p2 = np.array(
        [[s * slp1 * thick],
         [-slp1 * thick * np.tan(thet)]]
    ) + pref

    p3 = np.array(
        [[s * slp2 * thick],
         [-height]]
    ) + pref

    p4 = np.array(
        [[s * thick],
         [-height]]
    ) + pref

    p5 = np.array(
        [[s * thick1],
         [-height]]
    ) + pref

    path = (
        p1 * (1 - t) ** 3
        + p2 * 3 * t * (1 - t) ** 2
        + p3 * 3 * (t ** 2) * (1 - t)
        + p5 * (t ** 3)
    )

    err = (
        -3 * p1 * (1 - t) ** 2
        + p2 * 3 * (1 - t) * (1 - 3 * t)
        + p3 * 3 * t * (2 - 3 * t)
        + 3 * p4 * (t ** 2)
    )

    dX1 = err[0]
    dY1 = err[1]

    erX1 = -(wdb / 2) * dY1 / np.sqrt(dX1**2 + dY1**2)
    erY1 = (wdb / 2) * dX1 / np.sqrt(dX1**2 + dY1**2)

    X = np.concatenate([
        path[0] - erX1,
        np.flip(path[0] + erX1),
    ])

    X[npoints - 1] = np.round(1000 * X[npoints - 1]) / 1000
    X[npoints] = np.round(1000 * X[npoints]) / 1000

    Y = np.concatenate([
        path[1] - erY1,
        np.flip(path[1] + erY1),
    ])

    Y[npoints - 1] = np.round(1000 * Y[npoints - 1]) / 1000
    Y[npoints] = np.round(1000 * Y[npoints]) / 1000

    return list(zip(X, Y))


@gf.cell
def spiral_block(
    xpush=2050,
    ypush=-50,
):
    c = gf.Component()

    N0_y_pos = 0
    pitch_edge_couplers = 3 * 127

    # ----------------------------------------------------------
    # Packaging tapers
    # ----------------------------------------------------------

    taper = exspot_packaging()

    inv_taper1 = c.add_ref(taper)
    inv_taper2 = c.add_ref(taper)

    inv_taper1.mirror_x()
    inv_taper2.mirror_x()

    # ----------------------------------------------------------
    # Imported spiral
    # ----------------------------------------------------------

    spiral1 = c.add_ref(
        spiral_import()
    )

    spany = spiral1.ysize

    # ----------------------------------------------------------
    # Position packaging tapers
    # ----------------------------------------------------------

    inv_taper1.move(
        [
            taper.xsize - 1,
            N0_y_pos,
        ]
    )

    inv_taper2.move(
        [
            taper.xsize - 1,
            N0_y_pos - pitch_edge_couplers,
        ]
    )

    # ----------------------------------------------------------
    # 180° bend
    # ----------------------------------------------------------

    bend_radius = spany / 2 + 3 / 2

    x_bend = gf.cross_section.cross_section(
        width=2.3,
        layer="X1P",
        radius=bend_radius,
    )

    arc = gf.components.bend_circular180(
        npoints=1000,
        cross_section=x_bend,
    )

    circbend = c.add_ref(arc)

    circbend.move(
        circbend.ports["o2"].center,
        np.array(inv_taper1.ports["o1"].center)
        + np.array((xpush, ypush + 3 + 2.3)),
    )

    # ----------------------------------------------------------
    # Connect spiral to circular bend
    # ----------------------------------------------------------

    spiral1.connect(
        "o2",
        circbend.ports["o1"],
    )

    # ----------------------------------------------------------
    # Bezier connection dimensions
    # ----------------------------------------------------------

    bendend1 = (
        np.array(circbend.ports["o2"].center)
        - np.array(inv_taper1.ports["o1"].center)
    )

    bendend2 = (
        np.array(spiral1.ports["o1"].center)
        - np.array(inv_taper2.ports["o1"].center)
    )

    # ----------------------------------------------------------
    # Bezier: circular bend -> taper 1
    # ----------------------------------------------------------

    c.add_polygon(
        points=bezier(
            npoints=2000,
            ang=0,
            height=bendend1[1],
            thick1=bendend1[0],
            thick=bendend1[0] / 1,
            wid1=1,
            wid2=2.3,
            pref=np.array([
                [circbend.ports["o2"].x],
                [circbend.ports["o2"].y],
            ]),
            slp1=0.68,
            slp2=0.7,
        ),
        layer="X1P",
    )

    # ----------------------------------------------------------
    # Bezier: spiral -> taper 2
    # ----------------------------------------------------------

    c.add_polygon(
        points=bezier(
            npoints=2000,
            ang=0,
            height=bendend2[1],
            thick1=bendend2[0],
            thick=bendend2[0] / 0.95,
            wid1=1,
            wid2=2.3,
            pref=np.array([
                [spiral1.ports["o1"].x],
                [spiral1.ports["o1"].y],
            ]),
            slp1=0.7,
            slp2=0.8,
        ),
        layer="X1P",
    )

    # ----------------------------------------------------------
    # External reference port
    # ----------------------------------------------------------

    c.add_port(
        name="ref1",
        center=(
            np.array(inv_taper1.ports["o1"].center)
            - np.array([inv_taper1.xsize, 0])
        ),
        orientation=0,
        cross_section="SM",
    )


    return c
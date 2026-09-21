import gdsfactory as gf
import numpy as np

from technology.layer_map import LAYER


def merge(list1, list2):
    return [(list1[i], list2[i]) for i in range(len(list1))]


def circ_arc(radius=80, ang1=+20, ang2=-20, npoints=300):
    thet1 = (ang1 / 180) * np.pi
    thet2 = (ang2 / 180) * np.pi
    angs = np.linspace(np.pi / 2 - thet1, np.pi / 2 - thet2, npoints)
    X = radius * np.cos(angs)
    Y = radius * np.sin(angs)
    return [X, Y]


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
    p2 = np.array([[s * slp1 * thick], [-slp1 * thick * np.tan(thet)]]) + pref
    p3 = np.array([[s * slp2 * thick], [-height]]) + pref
    p4 = np.array([[s * thick], [-height]]) + pref
    p5 = np.array([[s * thick1], [-height]]) + pref

    # Keep the original geometry definition from the old implementation.
    path = (
        p1 * (1 - t) ** 3
        + p2 * 3 * t * (1 - t) ** 2
        + p3 * 3 * (t**2) * (1 - t)
        + p5 * (t**3)
    )

    err = (
        -3 * p1 * (1 - t) ** 2
        + p2 * 3 * (1 - t) * (1 - 3 * t)
        + p3 * 3 * t * (2 - 3 * t)
        + 3 * p4 * (t**2)
    )

    dX1 = err[0]
    dY1 = err[1]

    erX1 = -(wdb / 2) * dY1 / np.sqrt(dX1**2 + dY1**2)
    erY1 = (wdb / 2) * dX1 / np.sqrt(dX1**2 + dY1**2)

    X = np.concatenate([path[0] - erX1, np.flip(path[0] + erX1)])
    Y = np.concatenate([path[1] - erY1, np.flip(path[1] + erY1)])

    X[npoints - 1] = np.round(1000 * X[npoints - 1]) / 1000
    X[npoints] = np.round(1000 * X[npoints]) / 1000
    Y[npoints - 1] = np.round(1000 * Y[npoints - 1]) / 1000
    Y[npoints] = np.round(1000 * Y[npoints]) / 1000

    return [X, Y]


def path_length_numpy(x, y):
    points = np.array([x, y]).T
    differences = np.diff(points, axis=0)
    squared_distances = np.sum(differences**2, axis=1)
    return np.sum(np.sqrt(squared_distances))


@gf.cell
def broadband_dc(npoints=300, k=0.01, angerr=0, flip=False) -> gf.Component:
    if k > 0.01:
        angs1 = np.array(
            [8.45, 9.32, 10.4, 11.5, 12.3, 13.3, 14.8, 16.3, 17.9, 19.92, 21.5, 22.3]
        )
        kaps1 = np.array(
            [0.081, 0.107, 0.145, 0.191, 0.24, 0.303, 0.4189, 0.549, 0.701, 0.87, 0.963, 0.99]
        )
        diffs1 = np.array(
            [0.62, 0.57, 0.52, 0.48, 0.45, 0.42, 0.381, 0.35, 0.32, 0.29, 0.27, 0.26]
        )

        a1 = np.polyfit(kaps1 - 0.8, angs1, 11)
        d1 = np.polyfit(kaps1 - 0.8, diffs1, 11)
        a1func = np.poly1d(a1)
        d1func = np.poly1d(d1)

        xsamps = np.array(
            [
                0.9, 0.7, 0.5, 0.3, 0.1,
                0.9, 0.7, 0.5, 0.3, 0.1,
                0.9, 0.7, 0.5, 0.3, 0.1,
                0.9, 0.7, 0.5, 0.3, 0.1,
                0.9, 0.7, 0.5, 0.3, 0.1,
            ]
        )
        xcor = np.array(
            [
                0.668, 0.377, 0.217, 0.113, 0.029,
                0.704, 0.392, 0.237, 0.12, 0.031,
                0.668, 0.376, 0.217, 0.117, 0.024,
                0.658, 0.358, 0.201, 0.105, 0.028,
                0.681, 0.383, 0.225, 0.12, 0.0308,
                0.988, 0.988, 0.988, 0.988, 0.988,
                0.83, 0.83, 0.83, 0.83, 0.83,
                0.9, 0.9, 0.9, 0.9, 0.9,
            ]
        )

        thetsamps = a1func(xsamps - 0.8)
        diffsamps = d1func(xsamps - 0.8)

        thetsamps = np.concatenate(
            (
                thetsamps,
                np.array(
                    [26.4, 26.4, 26.4, 26.4, 26.4,
                     24.2, 24.2, 24.2, 24.2, 24.2,
                     24.65, 24.65, 24.65, 24.65, 24.65]
                ),
            )
        )
        diffsamps = np.concatenate(
            (
                diffsamps,
                np.array(
                    [0.23, 0.23, 0.23, 0.23, 0.23,
                     0.264, 0.264, 0.264, 0.264, 0.264,
                     0.256, 0.256, 0.256, 0.256, 0.256]
                ),
            )
        )

        a2 = np.polyfit(xcor - 0.5, thetsamps, 7)
        d2 = np.polyfit(xcor - 0.5, diffsamps, 7)
        angfunc = np.poly1d(a2)
        diffunc = np.poly1d(d2)

        ang = (1 + angerr) * angfunc(k - 0.5)
        diff = diffunc(k - 0.5)
        gap = 0.4

    else:
        angs = np.array(
            [9.5, 9.566, 9.68, 9.9, 10.15, 10.44, 10.7, 11.2, 11.63,
             12.2, 12.69, 13.4, 14.43, 15.4, 16.62, 18.9, 24.7, 36.2]
        )
        kaps = np.array(
            [0.1, 0.098, 0.093, 0.086, 0.078, 0.0715, 0.0656, 0.0557,
             0.048, 0.04, 0.033, 0.0263, 0.02, 0.0156, 0.012, 0.0081,
             0.004, 0.0022]
        )
        gaps = np.array(
            [0.41, 0.413, 0.42, 0.4266, 0.437, 0.45, 0.465, 0.494, 0.522,
             0.55, 0.58, 0.62, 0.665, 0.71, 0.756, 0.83, 0.98, 1.15]
        )

        angfit = np.polyfit(kaps - 0.02, np.log(angs), 11)
        gapfit = np.polyfit(kaps - 0.02, np.log(gaps), 11)
        angfunc = np.poly1d(angfit)
        gapfunc = np.poly1d(gapfit)

        ang = (1 + angerr) * np.exp(angfunc(k - 0.02))
        gap = np.exp(gapfunc(k - 0.02))
        diff = 0.57

    wid0 = 1
    wid = 1
    wid1 = wid + diff
    r1 = 80
    r2 = r1 + gap + wid / 2 + wid1 / 2
    thet = ang * np.pi / 180
    thick = r1 * 0.5
    height = thick * np.tan(thet)
    outgap = 10

    coupler = gf.Component()

    l1 = circ_arc(
        radius=r1 - wid1 / 2, ang1=ang, ang2=-ang, npoints=npoints
    )
    l2 = bezier(
        npoints=2 * npoints,
        ang=ang,
        height=height + outgap,
        thick=thick,
        thick1=thick,
        wid1=wid0,
        wid2=wid1,
        s=-1,
        pref=np.array([[-r1 * np.sin(thet)], [r1 * np.cos(thet)]]),
    )
    l3 = circ_arc(
        radius=r1 + wid1 / 2, ang1=-ang, ang2=+ang, npoints=npoints
    )
    l4 = bezier(
        npoints=2 * npoints,
        ang=ang,
        height=height + outgap,
        thick=thick,
        thick1=thick,
        wid1=wid0,
        wid2=wid1,
        s=+1,
        pref=np.array([[+r1 * np.sin(thet)], [r1 * np.cos(thet)]]),
    )

    X = np.concatenate([l1[0], np.flip(l2[0]), l3[0], np.flip(l4[0])])
    Y = np.concatenate([l1[1], np.flip(l2[1]), l3[1], np.flip(l4[1])])
    len1 = path_length_numpy(l4[0], l4[1])

    u1 = circ_arc(
        radius=r2 - wid / 2, ang1=ang, ang2=-ang, npoints=npoints
    )
    u2 = bezier(
        npoints=2 * npoints,
        ang=ang,
        height=height + (r2 - r1) * np.cos(thet),
        thick=thick,
        thick1=thick - (r2 - r1) * np.sin(thet),
        wid1=wid0,
        wid2=wid,
        s=-1,
        pref=np.array([[-r2 * np.sin(thet)], [r2 * np.cos(thet)]]),
    )
    u3 = circ_arc(
        radius=r2 + wid / 2, ang1=-ang, ang2=+ang, npoints=npoints
    )
    u4 = bezier(
        npoints=2 * npoints,
        ang=ang,
        height=height + (r2 - r1) * np.cos(thet),
        thick=thick,
        thick1=thick - (r2 - r1) * np.sin(thet),
        wid1=wid0,
        wid2=wid,
        s=+1,
        pref=np.array([[+r2 * np.sin(thet)], [r2 * np.cos(thet)]]),
    )

    X1 = np.concatenate([u1[0], np.flip(u2[0]), u3[0], np.flip(u4[0])])
    Y1 = np.concatenate([u1[1], np.flip(u2[1]), u3[1], np.flip(u4[1])])
    len2 = path_length_numpy(u4[0], u4[1])

    print(f"length difference = {len2 - len1}")

    if flip is False:
        coupler.add_polygon(
            merge(X, Y),
            layer=LAYER.X1P,
        )
        coupler.add_polygon(
            merge(X1, Y1),
            layer=LAYER.X1P,
        )

        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                l2[0][2 * npoints],
                (l2[1][2 * npoints - 1] + l2[1][2 * npoints]) / 2,
            ],
            name="i1",
            width=wid0,
            orientation=180,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                u2[0][2 * npoints],
                (u2[1][2 * npoints - 1] + u2[1][2 * npoints]) / 2,
            ],
            name="i2",
            width=wid0,
            orientation=180,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                l4[0][2 * npoints],
                (l4[1][2 * npoints - 1] + l4[1][2 * npoints]) / 2,
            ],
            name="o1",
            width=wid0,
            orientation=0,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                u4[0][2 * npoints],
                (u4[1][2 * npoints - 1] + u4[1][2 * npoints]) / 2,
            ],
            name="o2",
            width=wid0,
            orientation=0,
        )
    else:
        coupler.add_polygon(merge(X, -Y), layer=LAYER.X1P)
        coupler.add_polygon(merge(X1, -Y1), layer=LAYER.X1P)

        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                l2[0][2 * npoints],
                (-l2[1][2 * npoints - 1] - l2[1][2 * npoints]) / 2,
            ],
            name="i2",
            width=wid0,
            orientation=180,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                u2[0][2 * npoints],
                (-u2[1][2 * npoints - 1] - u2[1][2 * npoints]) / 2,
            ],
            name="i1",
            width=wid0,
            orientation=180,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                l4[0][2 * npoints],
                (-l4[1][2 * npoints - 1] - l4[1][2 * npoints]) / 2,
            ],
            name="o2",
            width=wid0,
            orientation=0,
        )
        coupler.add_port(
            layer=LAYER.X1P,
            center=[
                u4[0][2 * npoints],
                (-u4[1][2 * npoints - 1] - u4[1][2 * npoints]) / 2,
            ],
            name="o1",
            width=wid0,
            orientation=0,
        )

    return coupler


@gf.cell
def broadband_dc_withbendsR(
    npoints=300,
    k=0.1,
    angerr=0,
) -> gf.Component:

    coupler = gf.Component()
    wid0 = 1

    bend = gf.components.bend_euler(
        angle=90,
        cross_section="SM",
    )

    c1 = coupler << broadband_dc(
        npoints=npoints,
        k=k,
        angerr=angerr,
    )

    b1 = coupler << bend
    b2 = coupler << bend

    b2.mirror(p1=(0, 0), p2=(1, 0))

    b1.connect("o1", c1.ports["o2"])
    b2.connect("o1", c1.ports["o1"])

    coupler.add_port(name="o1",port=b1.ports["o2"],width=wid0)

    coupler.add_port(name="o2",port=b2.ports["o2"],width=wid0)

    coupler.add_port(name="i1",port=c1.ports["i2"],width=wid0)

    coupler.add_port(name="i2",port=c1.ports["i1"],width=wid0)

    return coupler


@gf.cell
def broadband_dc_withbends(npoints=300, k=0.1, angerr=0) -> gf.Component:
    coupler = gf.Component()
    wid0 = 1

    bend = gf.components.bend_euler(
        angle=90,
        cross_section="SM",
    )

    c1 = coupler << broadband_dc(npoints=npoints, k=k, angerr=angerr)
    br1 = coupler << bend
    br2 = coupler << bend
    bl1 = coupler << bend
    bl2 = coupler << bend

    br2.mirror(p1=(0, 0), p2=(1, 0))
    bl1.mirror()
    bl2.rotate(180)

    br1.connect("o1", c1.ports["o2"])
    br2.connect("o1", c1.ports["o1"])
    bl1.connect("o1", c1.ports["i2"])
    bl2.connect("o1", c1.ports["i1"])

    coupler.add_port(name="o1", port=br1.ports["o2"], width=wid0)
    coupler.add_port(name="o2", port=br2.ports["o2"], width=wid0)
    coupler.add_port(name="i1", port=bl1.ports["o2"], width=wid0)
    coupler.add_port(name="i2", port=bl2.ports["o2"], width=wid0)

    return coupler


@gf.cell
def broadband_dc_withbendsL(
    npoints=300,
    k=0.1,
    angerr=0,
) -> gf.Component:

    coupler = gf.Component()
    wid0 = 1

    bend = gf.components.bend_euler(
        angle=90,
        cross_section="SM",
    )

    c1 = coupler << broadband_dc(
        npoints=npoints,
        k=k,
        angerr=angerr,
    )

    b1 = coupler << bend
    b2 = coupler << bend

    # Transform the bend references
    b1.mirror()
    b2.rotate(180)

    # Connect the bends to the two input ports
    b1.connect(
        "o1",
        c1.ports["i2"],
    )

    b2.connect(
        "o1",
        c1.ports["i1"],
    )

    # External ports
    coupler.add_port(
        name="i1",
        port=b1.ports["o2"],
        width=wid0,
    )

    coupler.add_port(
        name="i2",
        port=b2.ports["o2"],
        width=wid0,
    )

    coupler.add_port(
        name="o1",
        port=c1.ports["o2"],
        width=wid0,
    )

    coupler.add_port(
        name="o2",
        port=c1.ports["o1"],
        width=wid0,
    )

    return coupler


@gf.cell
def bezierbend(
    npoints=2000,
    ang=0,
    height=40,
    thick1=40,
    thick=40,
    wid1=1,
    wid2=2.3,
    slp1=0.68,
    slp2=0.7,
    layer=LAYER.X1P,
) -> gf.Component:
    bez = gf.Component("tapered_bezier")
    bez.add_polygon(
        points=bezier(
            npoints=npoints,
            ang=ang,
            height=height,
            thick1=thick1,
            thick=thick,
            wid1=wid1,
            wid2=wid2,
            slp1=slp1,
            slp2=slp2,
        ),
        layer=layer,
    )
    bez.add_port(
        name="i",
        center=[-thick1, -height],
        orientation=0,
        layer=layer,
        width=wid1,
    )
    bez.add_port(
        name="o",
        center=[0, 0],
        orientation=180,
        layer=layer,
        width=wid2,
    )
    return bez

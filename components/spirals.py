import gdsfactory as gf
import numpy as np

@gf.cell
def x_spiral(
    L=5000,
    n=5,
    radius=250,
    spacing=3,
):
    c = gf.Component()

    dr = 2.3 + spacing

    straight = gf.components.straight(
        length=L,
        cross_section="MM",
    )

    start_straight = c << straight
    start_straight.move((0, 0))

    bend1 = c << gf.components.bend_euler(
        angle=180,
        radius=radius,
        cross_section="MM",
    )

    bend1.connect("o1", start_straight, "o2")
    previous_bend = bend1

    for i in range(1, 2 * n):
        r = radius + i * dr

        bend = c << gf.components.bend_euler(
            angle=180,
            radius=r,
            cross_section="MM",
        )

        if i % 2 == 1:
            bend.rotate(180)

        s = c << straight

        s.connect("o1", previous_bend, "o2")
        bend.connect("o1", s, "o2")

        previous_bend = bend

    c.add_port(
        name="o1",
        port=start_straight.ports["o1"],
    )

    c.add_port(
        name="o2",
        port=previous_bend.ports["o2"],
    )

    return c

@gf.cell
def x_double_spiral(
    L=5000,
    n=5,
    radius=250,
    spacing=3,
):
    c = gf.Component()

    Rmin = radius
    gap = 2.3 + spacing
    bend_radius = Rmin - gap

    spiral = x_spiral(
        L=L,
        n=n,
        radius=radius,
        spacing=spacing,
    )

    # --------------------------------------------------
    # Two spirals
    # --------------------------------------------------

    spiral1 = c << spiral
    spiral1.move(
        spiral1.ports["o1"].center,
        (-L / 2, -(Rmin - gap / 2)),
    )

    spiral2 = c << spiral
    spiral2.rotate(180)
    spiral2.move(
        spiral2.ports["o1"].center,
        (L / 2, (Rmin - gap / 2)),
    )

    # --------------------------------------------------
    # 180-degree bends from the inner spiral ports
    # --------------------------------------------------

    bend1 = c << gf.components.bend_euler(
        angle=180,
        radius=bend_radius,
        cross_section="MM",
    )

    bend1.mirror(p1=(0, 0), p2=(1, 0))

    bend1.connect(
        "o1",
        spiral1.ports["o1"],
    )

    bend2 = c << gf.components.bend_euler(
        angle=180,
        radius=bend_radius,
        cross_section="MM",
    )

    bend2.mirror(p1=(0, 0), p2=(1, 0))

    bend2.connect(
        "o1",
        spiral2.ports["o1"],
    )

    # --------------------------------------------------
    # S-bend
    # --------------------------------------------------

    dy = (
        bend2.ports["o2"].center[1]
        - bend1.ports["o2"].center[1]
    )

    sbend = c << gf.components.bend_s(
        size=(2 * Rmin, dy),
        cross_section="MM",
    )

    sbend.connect(
        "o1",
        bend1.ports["o2"],
    )

    # --------------------------------------------------
    # Straight after S-bend
    # --------------------------------------------------
    straight_length = np.abs(bend2.ports["o2"].center[0] - sbend.ports["o2"].center[0])
    straight = c << gf.components.straight(
        length=straight_length,
        cross_section="MM",
    )

    straight.connect(
        "o1",
        sbend.ports["o2"],
    )
    # --------------------------------------------------
    # Straight + final 180-degree bend from spiral1 o2
    # --------------------------------------------------

    straight1 = c << gf.components.straight(
        length=L,
        cross_section="MM",
    )

    straight1.connect(
        "o1",
        spiral1.ports["o2"],
    )

    R_final = radius + (2 * n - 1) * (2.3 + spacing)
    final_radius = R_final + gap

    final_bend = c << gf.components.bend_euler(
        angle=180,
        radius=final_radius,
        cross_section="MM",
    )

    final_bend.connect(
        "o1",
        straight1.ports["o2"],
    )

    # --------------------------------------------------
    # Output ports
    # --------------------------------------------------

    c.add_port(
        name="o1",
        port=final_bend.ports["o2"],
    )

    c.add_port(
        name="o2",
        port=spiral2.ports["o2"],
    )
    return c
import gdsfactory as gf
import numpy as np
import math

from technology.layer_map import LAYER


@gf.cell
def heater_pad(orientation=1, overlap=0, optbox=0):

    c = gf.Component("Heater_Pad")

    # ==========================================================
    # PARAMETERS
    # ==========================================================

    p1r_size = 14.62
    via_size = 0.36
    p1p_size = 8.62
    via_pitch = 0.71

    # ==========================================================
    # P1R PAD
    # ==========================================================

    p1r_layer = c << gf.components.rectangle(
        size=(p1r_size, p1r_size),
        layer=LAYER.P1R,
    )

    # ==========================================================
    # P1P PAD
    # ==========================================================

    p1p_layer = c << gf.components.rectangle(
        size=(p1p_size, p1p_size),
        layer=LAYER.P1P,
    )

    p1p_layer.move(
        (
            (p1r_size - p1p_size) / 2,
            (p1r_size - p1p_size) / 2,
        )
    )

    # ==========================================================
    # VIAS
    # ==========================================================

    row = np.linspace(0, 6, 7)
    col = np.linspace(0, 6, 7)

    for j in row:
        for i in col:

            rect = c << gf.components.rectangle(
                size=(via_size, via_size),
                centered=(0, 0),
                layer=LAYER.VIA,
            )

            rect.move(
                (
                    5 + via_size / 2 + i * via_pitch,
                    5 + via_size / 2 + j * via_pitch,
                )
            )

    # ==========================================================
    # FIRST P1P TAPER
    # ==========================================================

    tap1 = c << gf.components.taper(
        width1=8.62,
        width2=3.2,
        length=5.4,
        cross_section="H",
    )

    # Mirror the reference, not the locked taper cell
    tap1.mirror()

    tap1.move(
        (
            (p1r_size - p1p_size) / 2,
            p1r_size / 2,
        )
    )

    # ==========================================================
    # P1P STRAIGHT
    # ==========================================================

    rect2 = c << gf.components.straight(
        length=4.2,
        width=3.2,
        cross_section="H",
    )

    rect2.connect(
        "o1",
        tap1.ports["o2"],
    )

    # ==========================================================
    # ORIENTATION 0
    # ==========================================================

    if orientation == 0:

        tap2 = c << gf.components.taper(
            width1=2,
            width2=3.2,
            length=1,
            cross_section="H",
        )

        c.add_port(
            name="o1",
            center=(-7.6, p1r_size / 2),
            orientation=-180,
            width=2,
            cross_section="H",
        )

        tap2.connect(
            "o2",
            rect2.ports["o2"],
        )

    # ==========================================================
    # ORIENTATION 1
    # ==========================================================

    elif orientation == 1:

        tap2 = c << gf.components.taper(
            width1=5.2,
            width2=3.2,
            length=1,
            cross_section="H",
        )

        c.add_port(
            name="o1",
            center=(-8.6 - overlap, 4.71),
            orientation=90,
            width=2,
            cross_section="H",
        )

        c.add_port(
            name="o2",
            center=(-8.6 - overlap, 4.71 + 5.2),
            orientation=270,
            width=2,
            cross_section="H",
        )

        tap2.connect(
            "o2",
            rect2.ports["o2"],
        )

        if optbox == 1:

            c.add_polygon(
                [
                    c.ports["o1"].center + (1, 0),
                    c.ports["o1"].center + (-1, 0),
                    c.ports["o2"].center + (-1, 0),
                    c.ports["o2"].center + (1, 0),
                ],
                layer=LAYER.P1P,
            )

    # ==========================================================
    # OTHER ORIENTATIONS
    # ==========================================================

    else:

        c.add_polygon(
            [
                (
                    rect2.ports["o2"].center[0],
                    rect2.ports["o2"].center[1]
                    + rect2.info["width"] / 2,
                ),
                (
                    rect2.ports["o2"].center[0]
                    + (1 / math.sqrt(2)) * rect2.info["width"],
                    rect2.ports["o2"].center[1]
                    + rect2.info["width"] / 2
                    - (1 / math.sqrt(2)) * rect2.info["width"],
                ),
                (
                    rect2.ports["o2"].center[0]
                    - 2 * rect2.info["width"]
                    + (1 / math.sqrt(2)) * rect2.info["width"],
                    rect2.ports["o2"].center[1]
                    - 1.5 * rect2.info["width"]
                    - (1 / math.sqrt(2)) * rect2.info["width"],
                ),
                (
                    rect2.ports["o2"].center[0]
                    - 2 * rect2.info["width"],
                    rect2.ports["o2"].center[1]
                    - 1.5 * rect2.info["width"],
                ),
            ],
            layer=LAYER.P1P,
        )

        c.add_port(
            name="o2",
            center=(
                rect2.ports["o2"].center[0]
                - 2 * rect2.info["width"],
                rect2.ports["o2"].center[1]
                - 1.5 * rect2.info["width"],
            ),
            width=2,
            orientation=315,
            cross_section="H",
        )

        c.add_port(
            name="o1",
            center=(
                rect2.ports["o2"].center[0]
                - 2 * rect2.info["width"]
                + (1 / math.sqrt(2)) * rect2.info["width"],
                rect2.ports["o2"].center[1]
                - 1.5 * rect2.info["width"]
                - (1 / math.sqrt(2)) * rect2.info["width"],
            ),
            width=2,
            orientation=135,
            cross_section="H",
        )

    # ==========================================================
    # ELECTRICAL P1R PORTS
    # ==========================================================

    c.add_port(
        name="e1",
        center=(p1r_size / 2, p1r_size / 2),
        orientation=-90,
        width=8.62,
        layer=LAYER.P1R,
    )

    c.add_port(
        name="e2",
        center=(p1r_size / 2, p1r_size / 2),
        orientation=0,
        width=8.62,
        layer=LAYER.P1R,
    )

    c.add_port(
        name="e3",
        center=(p1r_size / 2, p1r_size / 2),
        orientation=90,
        width=8.62,
        layer=LAYER.P1R,
    )

    c.add_port(
        name="e4",
        center=(p1r_size / 2, p1r_size / 2),
        orientation=-180,
        width=8.62,
        layer=LAYER.P1R,
    )

    return c
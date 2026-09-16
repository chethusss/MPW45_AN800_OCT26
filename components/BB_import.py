from pathlib import Path
import gdsfactory as gf


BB_GDS = Path(__file__).resolve().parent.parent / "AN800_LIGENTEC_BB_RELEASED.gds"

BB = gf.read.import_gds_multiple_top_cells(
    BB_GDS,
    rename_duplicated_cells=True,
)

@gf.cell
def exspot_packaging(
    wg_length=10,
    wg_width=1,
):
    c = gf.Component()

    # ----------------------------------------------------------
    # Input waveguide
    # ----------------------------------------------------------

    c.add_polygon(
        [
            (-wg_length, -wg_width / 2),
            (0, -wg_width / 2),
            (0, wg_width / 2),
            (-wg_length, wg_width / 2),
        ],
        layer="X1P",
    )

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    ref = c.add_ref(
        BB["AN800BB_ExSpot_packaging_SMF_C"]
    )

    # ----------------------------------------------------------
    # Ports
    # ----------------------------------------------------------

    c.add_port(
        name="o1",
        center=(-wg_length, 0),
        width=wg_width,
        orientation=180,
        layer="X1P",
    )

    # 10 um before the right edge of the BB
    c.add_port(
        name="o2",
        center=(674, 0),
        width=wg_width,
        orientation=0,
        layer="X1P",
    )

    return c

@gf.cell
def MMI1x2(
    wg_length=10,
):
    c = gf.Component()

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    mmi = c.add_ref(
        BB["AN800BB_MMI1x2_symmetric_C"]
    )

    # ----------------------------------------------------------
    # Input waveguide
    # Port location: (0, 0)
    # Extends to the left
    # ----------------------------------------------------------

    wg_in = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_in.move(
        origin=wg_in.ports["o2"].center,
        destination=(0, 0),
    )

    # ----------------------------------------------------------
    # Output waveguide 0
    # Port location: (133, -4.5)
    # Extends to the right
    # ----------------------------------------------------------

    wg_out0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out0.move(
        origin=wg_out0.ports["o1"].center,
        destination=(133, -4.5),
    )

    # ----------------------------------------------------------
    # Output waveguide 1
    # Port location: (133, +4.5)
    # Extends to the right
    # ----------------------------------------------------------

    wg_out1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out1.move(
        origin=wg_out1.ports["o1"].center,
        destination=(133, 4.5),
    )

    # ----------------------------------------------------------
    # External ports
    # ----------------------------------------------------------

    c.add_port(
        name="o1",
        port=wg_in.ports["o1"],
    )

    c.add_port(
        name="o3",
        port=wg_out0.ports["o2"],
    )

    c.add_port(
        name="o2",
        port=wg_out1.ports["o2"],
    )

    return c


@gf.cell
def MMI2x2(wg_length=10):
    c = gf.Component()

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    mmi = c.add_ref(
        BB["AN800BB_MMI2x2_symmetric_C"]
    )

    # ----------------------------------------------------------
    # Input waveguide 0
    # Port location: (0, 0)
    # ----------------------------------------------------------

    wg_in0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_in0.move(
        origin=wg_in0.ports["o2"].center,
        destination=(0, 0),
    )

    # ----------------------------------------------------------
    # Input waveguide 1
    # Port location: (0, 9)
    # ----------------------------------------------------------

    wg_in1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_in1.move(
        origin=wg_in1.ports["o2"].center,
        destination=(0, 9),
    )

    # ----------------------------------------------------------
    # Output waveguide 0
    # Port location: (218, 0)
    # ----------------------------------------------------------

    wg_out0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out0.move(
        origin=wg_out0.ports["o1"].center,
        destination=(218, 0),
    )

    # ----------------------------------------------------------
    # Output waveguide 1
    # Port location: (218, 9)
    # ----------------------------------------------------------

    wg_out1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out1.move(
        origin=wg_out1.ports["o1"].center,
        destination=(218, 9),
    )

    # ----------------------------------------------------------
    # External ports
    # ----------------------------------------------------------

    c.add_port(
        name="o2",
        port=wg_in0.ports["o1"],
    )

    c.add_port(
        name="o1",
        port=wg_in1.ports["o1"],
    )

    c.add_port(
        name="o4",
        port=wg_out0.ports["o2"],
    )

    c.add_port(
        name="o3",
        port=wg_out1.ports["o2"],
    )

    return c

@gf.cell
def MMI4x4(wg_length=10):
    c = gf.Component()

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    mmi = c.add_ref(
        BB["AN800BB_MMI4x4_symmetric_C"]
    )

    # ----------------------------------------------------------
    # Input waveguides
    # ----------------------------------------------------------

    wg_in0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_in0.move(
        origin=wg_in0.ports["o2"].center,
        destination=(0, 0),
    )

    wg_in1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_in1.move(
        origin=wg_in1.ports["o2"].center,
        destination=(0, 11.7),
    )

    wg_in2 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_in2.move(
        origin=wg_in2.ports["o2"].center,
        destination=(0, 23.46),
    )

    wg_in3 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_in3.move(
        origin=wg_in3.ports["o2"].center,
        destination=(0, 35.26),
    )

    # ----------------------------------------------------------
    # Output waveguides
    # ----------------------------------------------------------

    wg_out0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_out0.move(
        origin=wg_out0.ports["o1"].center,
        destination=(583, 0),
    )

    wg_out1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_out1.move(
        origin=wg_out1.ports["o1"].center,
        destination=(583, 11.7),
    )

    wg_out2 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_out2.move(
        origin=wg_out2.ports["o1"].center,
        destination=(583, 23.46),
    )

    wg_out3 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )
    wg_out3.move(
        origin=wg_out3.ports["o1"].center,
        destination=(583, 35.26),
    )

    # ----------------------------------------------------------
    # External ports
    # ----------------------------------------------------------

    c.add_port("o1", port=wg_in0.ports["o1"])
    c.add_port("o2", port=wg_in1.ports["o1"])
    c.add_port("o3", port=wg_in2.ports["o1"])
    c.add_port("o4", port=wg_in3.ports["o1"])

    c.add_port("o5", port=wg_out0.ports["o2"])
    c.add_port("o6", port=wg_out1.ports["o2"])
    c.add_port("o7", port=wg_out2.ports["o2"])
    c.add_port("o8", port=wg_out3.ports["o2"])

    return c

@gf.cell
def inv_taper(wg_length=10):
    c = gf.Component()

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    taper = c.add_ref(
        BB["AN800BB_EdgeCoupler_Lensed_C_w1.0"]
    )

    # ----------------------------------------------------------
    # Extend narrow input side
    # Port location: (0, 0)
    # ----------------------------------------------------------

    wg_in = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_in.move(
        origin=wg_in.ports["o2"].center,
        destination=(0, 0),
    )

    # ----------------------------------------------------------
    # External ports
    # ----------------------------------------------------------

    # Extended X1P waveguide port
    c.add_port(
        name="o1",
        port=wg_in.ports["o1"],
    )

    # Wide/lensed-fiber side: reference port only
    c.add_port(
        name="o2",
        center=(384, 0),
        width=1,
        orientation=0,
        layer="FPIN",
    )

    return c


@gf.cell
def PBS(wg_length=10):
    c = gf.Component()

    # ----------------------------------------------------------
    # Black-box
    # ----------------------------------------------------------

    pbs = c.add_ref(
        BB["AN800BB_PBS_C"]
    )

    # ----------------------------------------------------------
    # Input waveguide
    # Port location: (0, 0)
    # ----------------------------------------------------------

    wg_in = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_in.move(
        origin=wg_in.ports["o2"].center,
        destination=(0, 0),
    )

    # ----------------------------------------------------------
    # Output waveguide 0
    # Port location: (238, 0)
    # ----------------------------------------------------------

    wg_out0 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out0.move(
        origin=wg_out0.ports["o1"].center,
        destination=(238, 0),
    )

    # ----------------------------------------------------------
    # Output waveguide 1
    # Port location: (238, -28.56)
    # ----------------------------------------------------------

    wg_out1 = c.add_ref(
        gf.components.straight(
            length=wg_length,
            cross_section="SM",
        )
    )

    wg_out1.move(
        origin=wg_out1.ports["o1"].center,
        destination=(238, -28.56),
    )

    # ----------------------------------------------------------
    # External ports
    # ----------------------------------------------------------

    c.add_port(
        name="o1",
        port=wg_in.ports["o1"],
    )

    c.add_port(
        name="o2",
        port=wg_out0.ports["o2"],
    )

    c.add_port(
        name="o3",
        port=wg_out1.ports["o2"],
    )

    return c
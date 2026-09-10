from pathlib import Path

import gdsfactory as gf
from technology.pdk import AN800_PDK

AN800_PDK.activate()


SPIRAL_GDS = Path(__file__).resolve().parent.parent / "spiral.gds"


# Import the GDS once when this module is loaded
IMPORTED_SPIRAL = gf.import_gds(
    SPIRAL_GDS,
    rename_duplicated_cells=True,
)


@gf.cell
def spiral_import() -> gf.Component:
    spir = gf.Component()

    ref = spir.add_ref(IMPORTED_SPIRAL)

    ref.mirror()
    ref.center = (0, 0)

    spir.add_port(
        name="o1",
        center=[0, spir.ysize / 2 - 2.3 / 2],
        orientation=180,
        cross_section="MM",
    )

    spir.add_port(
        name="o2",
        center=[0, -spir.ysize / 2 + 2.3 / 2],
        orientation=0,
        cross_section="MM",
    )
    return spir
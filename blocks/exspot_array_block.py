import gdsfactory as gf
from components.BB_import import exspot_packaging

@gf.cell
def exspot_array(
    num=9,
    pitch=127,
    y0=0,
):
    c = gf.Component()

    num_right =num

    # Left edge couplers
    for i in range(num):

        ref = c << exspot_packaging()

        # Face toward the chip
        ref.mirror_x()

        ref.move(origin=ref.ports["o2"].center,
            destination=(0,- i * pitch))

        c.add_port(
            name=f"i{i + 1}",
            port=ref.ports["o1"],
        )
        if i==0:
            c.add_port("ref1",port=ref.ports["o2"])

    # Right edge couplers
    for i in range(num_right):
        ref = c << exspot_packaging()

        ref.move(origin=ref.ports["o2"].center,
            destination=(5190, y0 - i * pitch))

        c.add_port(
            name=f"o{i + 1}",
            port=ref.ports["o1"],
        )

    return c
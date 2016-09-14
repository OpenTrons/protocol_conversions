# Import Protocol Object from SDK - assuming user wont have to do this
from opentrons_sdk.protocol import Protocol

protocol = Protocol()

protocol.set_info(
    name="Dilution 10x",
    description="10X Full Plate",
    author="Opentrons",
    created="Wed Aug 24 10:10:00 2016"
}

p200_rack = containers.tiprack.p200('B1')
trash = containers.trough_12row('B2')

standards = containers.96_pcr_flat('D1')
trough = containers.trough.12('C2')

p200 = labware.Pipette(
    trash_container=trash,
    tip_racks=[p200_rack],
    min_vol=10,
    max_vol=1000,
    axis="b",
    channels=8
)

# spread the stuff to all of column A
for r in range(1,13):
	s_wells = trough.row(1)
	d_wells = standards.row(r)

	p200.take(s_well, volume=180, z=1)
	p200.to(d_well).blowout().touch_tip()

# dilute through the column
for r in range(1,12):

	s_wells = standards.row(r)
	d_wells = standards.row(r + 1)

	p200.replace_tip()

	# mix the well
	p200.take(s_wells, volume=100, z=1)
	p200.mix(3, {'tip-offset': 1}).blowout()

	# then transfer to next well
	p200.take(s_wells, volume=20, z=1)
	p200.to(d_wells, z=1).touch_tip()

p200.replace_tip()

p200.take(standards.row(12), volume=100, z=1)
p200.mix(3, z=1).blowout()
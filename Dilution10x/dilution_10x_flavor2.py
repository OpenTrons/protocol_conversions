# Import Protocol Object from SDK - assuming user wont have to do this
from opentrons_sdk.protocol import Protocol

protocol = Protocol()

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

	# it's an entire row of wells, because it's multi-channel
	s_wells = trough.row(1)
	d_wells = standards.row(r)

	p200.take(s_wells, volume=180, z=1.1) # z= is a percentage, in this case %110 of this well's height
	p200.to(d_wells).blowout().touch_tip()

# dilute through the column
for r in range(1,12):

	s_wells = standards.row(r)
	d_wells = standards.row(r + 1)

	p200.replace_tip()

	# mix the well
	p200.take(s_wells, volume=100, z=0.1) # z= is a percentage, in this case %10 of this well's height
	p200.mix(3, z=0.1).blowout(z=1.1).delay(3)

	# then transfer to next well
	p200.take(s_wells, volume=20, z=0.1)
	p200.to(d_wells).touch_tip()

p200.replace_tip()

p200.take(standards.row(12), volume=100, z=0.1)
p200.mix(3, z=0.1).blowout().delay(3)
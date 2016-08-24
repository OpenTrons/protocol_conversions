from opentrons_sdk.protocol import Protocol

protocol = Protocol()

protocol.add_container('C2','tiprack.p10','p10-rack')
protocol.add_container('A1','tiprack.p200','p200-rack')
protocol.add_container('C1','96-PCR-tall','PCR_plate')
protocol.add_container('E1',' tube-rack-2ml','Micro_Tube_Rack')
protocol.add_container('B2', 'point.trash','trash')

protocol.add_instrument(axis='b', 'p200.1c')
protocol.add_instrument(axis='b', 'p10.1c')

protocol.calibrate_instrument('a', top=2, bottom=12, blowout_pos=15, droptip=17)

protocol.config_instrument(
	axis='a',
	down_plunger_speed=300,
    up_plunger_speed=500,
    tip_plunge=6
)

start_config = {
	'liquid-tracking': False,
	'tip-offset': -3,
	'touch-tip': False,
	'delay': 1,
	'extra-pull-volume': 10,
	'extra-pull-delay': 0.5
}

end_config = {
	'liquid-tracking': True,
	'tip-offset': 0,
	'touch-tip': True,
	'delay': 0,
	'blowout': True
}

protocol.pickup_tip()

with protocol.new_tip() as tip:
	for row in 'ABCDEFGH':
		from_well = 'Micro_Tube_Rack:A1'
		to_well = 'PCR_plate:{row}1'.format(row=row)
		tip.transfer(from_well, to_well, tool='a', ul=23, start_config, end_config)

protocol.droptip()

start_config = {
	'liquid-tracking': True,
	'tip-offset': 0,
	'touch-tip': False,
	'delay': 0,
	'extra-pull-volume': 10,
	'extra-pull-delay': 0.5
}

end_config = {
	'liquid-tracking': False,
	'tip-offset': 0,
	'touch-tip': False,
	'delay': 0,
	'blowout': True
}

with protocol.new_tip() as tip:
	for row in 'ABCDEFGH':
		from_well = 'Micro_Tube_Rack:B1'
		to_well = 'PCR_plate:{row}1'.format(row=row)
		protocol.transfer(from_well, to_well, tool='b', ul=1, start_config, end_config)

		
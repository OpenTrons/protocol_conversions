from opentrons_sdk.protocol import Protocol

protocol = Protocol()

# not sure if we have run_notes yet, but it would be good for protocol lib
protocol.set_info(
    name = "8 Sample PCR",
    description ="8 PCRs from the same DNA sample",
    author ="OpenTrons",
    created ="Tue Aug 30 10:10:00 2016",
    run_notes = "Master Mix (tube rack A1), DNA (tube rack B1), Taq (tube rack C1), PCR samples (plate A1-H1)"
}

# Are we neglecting this? Set it once and pass to pipette object?
# Should we make this a PConfig object?
p10_config = {
	'max_vol' : 10,
	'ming_vol' : 1,
	'down-plunger-speed' : 300,
	'up-plunger-speed' : 500,
	'tip-plunge' : 7,
	'extra-pull-volume' : 0,
	'extra-pull-delay' : 200,
	'distribute-percentage' : 0.1
}
p10 = Pipette(channels=1, p10_config) 
# min and max vol should be baked in to Pipette object based on labware and optional here
# DC mentioned increments - does this affect us? increments only for manual?
p200 = Pipette(channels=1, min_vol=20, max_vol=200)

# writing this here without axis= and tool= as shorthand example 
protocol.add_tool('A',p10)
protocol.add_tool('B',p200)

p10_rack = Container(tiprack.p10)
p200_rack = Container(tiprack.p200)
plate = Container(microplate.96)
tube_rack = Container(tuberack.2)
trash = Container(point.trash)

# with slot and tool arguments specified
protocol.add_container(slot='C2',p10_rack )
# shorthand (after user gets the hang of it)
protocol.add_container('A1', p200_rack)
protocol.add_container('C1', plate)
# what if we reversed it, as in protocol.add_container(p200_rack, 'A1')
# it reads more like add the p200 rack to slot A1?
protocol.add_container('E1', tube_rack)
protocol.add_container('B2', trash)

# define default configs as a config object
# TO DO: get global defaults from DC so we dont need to write out settings that match defaults
# Q: new tip in start vs drop tip in end config? Thinking transfer groups here...
pcr = Config(start={'touchtip':false, 'delay':0, 'new_tip':false}, end={'touch_tip':false, 'blowout':true})

# protocol.activate(instrument, config) and .deactivate(instrument, config)
with protocol.activate(p200, pcr)
	# protocol.transfer(start, end, ul)
	protocol.transfer(tube_rack['A1'], plate['A1'], 23)
	protocol.transfer(tube_rack['A1'], plate['B1'], 23)
	protocol.transfer(tube_rack['A1'], plate['C1'], 23)
	protocol.transfer(tube_rack['A1'], plate['D1'], 23)
	protocol.transfer(tube_rack['A1'], plate['E1'], 23)
	protocol.transfer(tube_rack['A1'], plate['F1'], 23)


#transfer_group(self, *wells, ul=None, ml=None, **defaults)







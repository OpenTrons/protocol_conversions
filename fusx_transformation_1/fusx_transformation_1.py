protocol = Protocol()

# DECK section

tiprack_200ul 	= protocol.add_container('A2', 'tiprack.p200')
tiprack_10ul 	= protocol.add_container('B1', 'tiprack.p10')
LB 				= protocol.add_container('D1', 'tuberack.2000ul')
trash 			= protocol.add_container('A1', 'point.trash')
FusX_Output 	= protocol.add_container('C2', '96-pcr-flat')
Cool_Deck 		= protocol.add_container('D3', 'tuberack.2000ul')
Head_Deck 		= protocol.add_container('B3', 'tuberack.2000ul')

# HEAD section

p200 			= protocol.add_instrument(axis='b',channels=1)
p10 			= protocol.add_instrument(axis='a',channels=1)

""" pipette's are calibrated through the UI
p200.calibrate(volume=198, top=2, bottom=15, blowout=17, droptip=19)
p10.calibrate(volume=9.3, top=2, bottom=15, blowout=17, droptip=19)
"""

p200.config({
	'down-plunger-speed': 300,
    'up-plunger-speed': 500,
    'tip-plunge': 8
})

p10.config({
	'down-plunger-speed': 150,
    'up-plunger-speed': 300,
    'tip-plunge': 6
})

# INSTRUCTIONS section

start_config = {
}

end_config = {
	'touch-tip' : True,
	'blowout' : True,
	'delay' : 1.8
}

p10.transfer(FusX_Output['A1'], Cool_Deck['A1'], ul=2.5, start_config, end_config)



start_config = {
}

end_config = {
	'touch-tip' : True,
	'blowout' : True,
	'delay' : 0.035
}

p200.transfer(Cool_Deck['A1'], Heat_Deck['A1'], ul=27.5, start_config, end_config)



start_config = {
}

end_config = {
	'touch-tip' : True,
	'blowout' : True,
	'delay' : 0.3
}

p200.transfer(Head_Deck['A1'], Cool_Deck['A1'], ul=27.5, start_config, end_config)






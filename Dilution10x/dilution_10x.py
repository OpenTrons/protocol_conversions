# Import Protocol Object from SDK - assuming user wont have to do this
from opentrons_sdk.protocol import Protocol

protocol = Protocol()

# Add Info - replaces "info" section of JSON
protocol.set_info(
    name="Dilution 10x",
    description="10X Full Plate",
    author="Opentrons",
    created="Wed Aug 24 10:10:00 2016"
}

# Add Instruments (pipettes) - this replaces "head" section of JSON
# def add_instrument(self, axis, name)
# add p200 to axis a (center) 
# Q: Currently no ability to specify single or multi? See labware/pipettes.py
protocol.add_instrument('A', 'p200') 

# Add Containers  - replaces "deck" section of JSON
# def add_container(self, slot, name, label=None)
# Noticed a third parameter - label - this is the user freindly name - ie "standards" or "trash"
protocol.add_container('B1', 'tiprack.p200', label='p200-rack')
protocol.add_container('D1', 'microplate.96', label='standards')
protocol.add_container('C2', 'trough.12' label='trough')
protocol.add_container('B2', 'point.trash', label='trash')

### HYPOTHETICAL ###
# Andy had a great idea for creating transfer_config for things like plunger speed etc
# (See andy's example)
# I would add to that list - the tool definition, might save additional time?
# Something like:
tool_config = {
	tool = 'p200',
	touchtip = False,
	blowout = True
}
# I think transfer_group might fix all of these issues once fleshed out?


# Define transfers. 
# def transfer(self, start, end, ul=None, ml=None, blowout=True, touchtip=True, tool=None)
protocol.transfer('C2:A1', 'D1:A1', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A2', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A3', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A4', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A5', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A6', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A7', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A8', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A9', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A10', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A11', ul=180, touchtip=False, tool='p200')
protocol.transfer('C2:A1', 'D1:A12', ul=180, touchtip=False, tool='p200')

### OR with a loop ###
for r in range(1,13):
	to_row = 'D1:A' + str(r) #think this should be a row, col, or range function in transfer_group
	protocol.transfer('C2:A1', to_row, ul=180, touchtip=False, tool='p200')

# Mix is not complete - but syntax would be:
# def mix(self, start, volume=None, repetitions=None, blowout=True)
# NOTE: volume instead of ul/ml like in transfer above
protocol.mix('D1:A1', volume=100, repetitions=3)
# Work around for Mix using only transfer for now? start = end, do we need to specify axis or tool here as well?
for r in range(0,3):
	protocol.transfer('D1:A1', 'D1:A1', ul=100, touchtip=False, tool='p200')

# Transfer then Mix Combo
# Transfer 
protocol.transfer('D1:A1', 'D1:A2', ul=20, touchtip=True, tool='p200')
# Then Mix with a loop using future mix definition
protocol.mix('D1:A2', volume=100, repetitions=3)
### OR ###
# Recursive workaround
for r in range(0,3):
	protocol.transfer('D1:A2', 'D1:A2', ul=100, touchtip=False, tool='p200')

# Rest of Protocol here - using protocol.mix() for brevity sake - 
# this can also be a loop if the volumes stay consistent - will write that below
protocol.transfer('D1:A2', 'D1:A3', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A3', volume=100, repetitions=3)

protocol.transfer('D1:A3', 'D1:A4', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A4', volume=100, repetitions=3)

protocol.transfer('D1:A4', 'D1:A5', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A5', volume=100, repetitions=3)

protocol.transfer('D1:A5', 'D1:A6', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A6', volume=100, repetitions=3)

protocol.transfer('D1:A6', 'D1:A7', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A7', volume=100, repetitions=3)

protocol.transfer('D1:A7', 'D1:A8', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A8', volume=100, repetitions=3)

protocol.transfer('D1:A8', 'D1:A9', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A9', volume=100, repetitions=3)

protocol.transfer('D1:A9', 'D1:A10', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A10', volume=100, repetitions=3)

protocol.transfer('D1:A10', 'D1:A11', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A11', volume=100, repetitions=3)

protocol.transfer('D1:A11', 'D1:A12', ul=20, touchtip=True, tool='p200')
protocol.mix('D1:A12', volume=100, repetitions=3)

### LOOP EXAMPLE ###
for r in range(1,12):
	from_row = 'D1:A' + str(r)
	to_row = 'D1:A' + str(r+1)
	#print(from_row, to_row)
	protocol.transfer(from_row, to_row, ul=20, touchtip=True, tool='p200')
	protocol.mix(to_row, volume=100, repetitions=3)




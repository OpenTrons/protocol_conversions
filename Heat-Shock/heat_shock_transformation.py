# Import Protocol from SDK
from opentrons_sdk.protocol import Protocol

# The Protocol object represents your scientific experiment. The first step is to create an 
# instance of the Protocol object, only one instance is needed.
protocol = Protocol()

# set_info sets some meta data for user reference, and future descriptions for user
# uploads to the protocol library
protocol.set_info(
    name="E. coli Heat Shock Transformation",
    description="This protocol uses 50 uL competent cells, 2 uL plasmid DNA and 200 uL Luria Broth (LB). The DNA is first added to the cells, and then they are incubated for 30 minutes at 4 degrees Celsius. Then, the entire solution is transferred to a new tube on the heat block and ‘heat shocked’ for exactly 60 seconds. The solution is then returned to the cold block for 5 minutes, before adding the LB. The tube is then removed from the robot and incubated at 37 degrees Celsius on a shaker for two hours before being plated",
    author="OpenTrons",
    created="Mon Aug 29 10:10:00 2016"
}

# Pipette(channels, min_vol, max_vol)
# The Pipette object represents a given pipette used in a protocol.
# channels = how many tips it can hold (1 or 8)
# min_vol = the smallest volume this pipette can handle
# max_vol = the largest volume this pipette can handle

# Pipette Object should also have default increments based on the instrument,
# Need to discuss in meeting: 
# Do we guarantee volumes that the pipette does not give access to when used manually?
# min and max vols should have default values in pipette object with option to overwrite

p10 = Pipette(channels=1, min_vol=0.5, max_vol=10) 
p200 = Pipette(channels=1, min_vol=20, max_vol=200)
# p200 = Pipette(channels=8, min_vol=50, max_vol=300)
# Q: Can we reference preset min and max vols list somewhere in docs?

# protocol.add_instrument(axis, instrument)
# After we create our Pipette objects 
# these instances of Pipette can then be added to the protocol with .add_instrument()
# axis = either A or B
# tool = object representing your pipette (see Pipette above)
# These instances of Pipette can then be added to the protocol with .add_instrument()
protocol.add_tool(axis='B', instrument=p200) # p200 is a Pipette created above
protocol.add_tool(axis='A', instrument=p10)


# Container(type)
# The Container object represents a given container used in a protocol.
# Before we add them to a protocol, we need to declare and assign them a type from
# the supported labware type list. see: https://github.com/OpenTrons/opentrons_sdk/tree/master/opentrons_sdk/labware
p200_rack = Container(tiprack.p200)
p10_rack = Container(tiprack.p10)
# tube rack 2ml
# Q: not sure if this is fully fleshed out yet?
tube_rack = Container(tuberack.2)
trash = Container(point.trash)
# note- heat and cool deck are modules but the aluminum tube rack and pcr plate 
# are assigned just as any other rack or plate. 
cold_deck = Container(tuberack.2ml.4.6) # scientist suggestion: we need to define tube vol but accomodate various layouts
heat_deck = Container(tuberack.2ml.10.10) # 2ml tubrack 10x10

# protocol.add_container(slot, container)
# Adds a container to be used in the protocol, 
# container must be present on the deck where the protocol is being run. 
# These include well plates, tipracks, tube racks, etc.
# slot = deck location of this container, this will be useful when protocol sharing and dynamic deckmaps are implemented
# container object representing your container ^(see Container above)
protocol.add_container(slot='A2', container=p200_rack)
protocol.add_container(slot='B1', container=p10_rack)
protocol.add_container(slot='D1', container=tube_rack)
protocol.add_container(slot='B2', container=trash)
protocol.add_container(slot='D3', container=cold_deck)
protocol.add_container(slot='B3', container=heat_deck)

# protocol.transfer(start, end, ul)

# protocol.activate(instrument) and .deactivate(instrument)

# Takes a given pipette, and assigns all following commands to it. 
# This allows you to assign groups of commands to different pipettes. 
# The .deactivate() method is required before activating a different instrument.

# using start and end configs along with activate and deactivate for the p10 pipette:
# activate the pipette
protocol.activate(p10)
# assign start and end configurations, 
# this is more useful when using same settings for multiple transfers but it is more human readbale
s_config = {
    'new_tip' : true,
    'touchtip' : false
}
e_config = {
	'touchtip' : true,
    'blowout' : true,
    'delay' : 1800 # question - are we adding in delays to start or end config or will there be a protocol.add_delay(millis?)
}
# protocol.transfer(start, end, ul, start_config, end_config)
# Transfer commands can take two optional arguments for further setting up the robot's movements. 
# These ordered dictionaries are applied to the start and end wells independently, allowing the robot to behave differently for each.
# start_config an ordered dictionary of optional parameters
# new_tip option to use an unused clean tip for this transfer
# default is true
# blowout option to push the plunger an extra amount, dispensing any leftover liquids
# default is false
# touchtip option to touch the sides of a well after the command finishes, removing droplets left on the tip
# default is false
# tip-offset distance to halt the Z-axis above the well's bottom
# default is 0
# transfer 2ul from cold deck tube B1 to cold deck tube A1
protocol.transfer(start=cold_deck['B1'], end=cold_deck['A1'], ul=2, start_config=s_config, end_config=e_config)
protocol.deactivate(p10)

# If we are using the config settings, tips, etc for multiple similar transfers we can save time by
# using a python with statement and avoid the deactivate() method

with protocol.activate(p200):
    # suggestion - can this be a library like our supported containers
    # so that a user can access defaults for different commands/liquid types
    # start.viscous, end.water etc?
    # Can a user define thier own defaults at the beginning of the protocol much like
    # tools and containers start_config = hivebio.viscous
    s_config = {
        'new_tip' : false, 
        'touchtip' : true,
        'tip-offset' : 0
    }
    e_config = {
        'touch-tip': true,
        'tip-offset' : 0,
        'blowout' : true,
        'delay': 35
    }
    #Q: the only thing we need to change in the config each time in this transfer group is 
    #  the length of the delays. 
    # Can we pass in additional individual parameters like in the original docs?
    # OR
    # should this be separated as an optional argument? 
    # protocol.transfer(start,end,ul,start_config, end_config, delay)?
    protocol.transfer(start=cold_deck['A1'], end=heat_deck['A1'], ul=27,  start_config={'touchtip':true, 'delay':12})
    # the example below uses delay as a separate optional argument after the first transfer in group
    # this will create issues (are we delaying in the start config or end config) 
    # protocol.transfer(start=heat_deck['A1'], end=cold_deck['A1'], ul=27, start_config=s_config, end_config=e_config, delay=300)   
    # what about overwriting one property in e_config?
    e_config.delay = 300
    protocol.transfer(start=heat_deck['A1'], end=cold_deck['A1'], ul=27, start_config=s_config, end_config=e_config)
    # use a new tip, no delay?
    s_config.new_tip = true
    e_config.delay = 0
    protocol.transfer(start=cold_deck['A1'], end=heat_deck['A1'], ul=200, start_config=s_config, end_config=e_config)
    
    # default three arugments we shouldnt have to say start= end= and ul=
    protocol.transfer(cold_deck['A1'], heat_deck['A1'], 200)

# Example user defines config defaults based on discussion
viscous = Config(start={'tip_offset':0, 'delay': 0}, end={'blowout':true})
protocol.activate(p200,viscous)
protocol.transfer(cold_deck['A1'], heat_deck['A1'], 200)

protocol.transfer(cold_deck['A2'], heat_deck['A1'], 200, start_config={'delay':1200}) #overwrite visous.start default delay?
protocol.deactivate(p200)







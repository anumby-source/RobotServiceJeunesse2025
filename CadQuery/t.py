from cadquery import exporters
from cadquery import *
from cadquery.vis import show

# base of pin that goes through PCB

base_pin_diameter = 0.7
base_pin_fillet = 0.05
base_pin_length = 0.8

# body pin, that goes above washer
body_pin_diameter = 1.5

# body_pin_taper not specified on data sheet, guesstimated
body_pin_fillet = 0.2
body_pin_length = 3.5

# top pin
top_pin_diameter = 0.9
top_pin_fillet = 0.45
top_pin_length = 1.5

# washer shape that sits on PCB
washer_diameter = 2.0

# fractional fillet as a value of 0 causes the code to crash
washer_fillet = 0.001
washer_height = 0.5

def pin(diameter, length, fillet_radius):
    # Create a pin
    pin = Workplane("XY").circle(diameter/2).extrude(length).faces("+Z").fillet(fillet_radius)

    return pin

pogo_pin = Assembly()

# create the base pin that fits into the PCB
base_pin = pin(base_pin_diameter, base_pin_length, base_pin_fillet)

# mirror this pin so that the fillet is at the base
base_pin = base_pin.mirror(mirrorPlane="XY", basePointVector=(0, 0, base_pin_length/2))
pogo_pin.add(base_pin)

# keep track of high the assembly is
stack_height=base_pin_length

# add the washer that sits on the PCB
pogo_pin.add(pin(washer_diameter, washer_height, washer_fillet), loc=Location(Vector(0, 0, stack_height)))
stack_height += washer_height

# create the body pin that fits on top of the ‘washer’
pogo_pin.add(pin(body_pin_diameter, body_pin_length, body_pin_fillet), loc=Location(Vector(0, 0, stack_height)))
stack_height+=body_pin_length

# create the top pin
pogo_pin.add(pin(top_pin_diameter, top_pin_length, top_pin_fillet), loc=Location(Vector(0, 0, stack_height)))

# render object
show(pogo_pin)

# save step file
# pogo_pin.save("pogo_pin.step")


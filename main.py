# Do not modify these lines
__winc_id__ = '7b9401ad7f544be2a23321292dd61cb6'
__human_name__ = 'arguments'

# Add your code after this line

def greet(name, greeting_template = "Hello, <name>!"):
    print(greeting_template.replace("<name>", name))

#greet("Doc")
#greet('Bob', "What's up, <name>!")


# PLEASE READ
# the url https://www.smartconversion.com/otherInfo/gravity_of_planets_and_the_sun.aspx is not working, I am guessing I was getting a list of different forces per planet
# including an external link is very irritating by the way. imagine when it does not work

gravitational_forces = {"earth": 9.8, "venus": 0.9, "mercury":0.3, "moon":0.2}

def force(mass, body="earth"):
    gravitational_force_of_body = gravitational_forces[body]
    force_of_body = mass * gravitational_force_of_body
    return force_of_body

#print(force(1, "mercury"))

masses = {"earth": 10, "venus": 8, "mercury":2.8, "moon":7.5}
G = 9.8

def pull(body1, body2, distance):
    return G*(masses[body1]*masses[body2]/distance)

print(pull("earth", "moon", 5))
    




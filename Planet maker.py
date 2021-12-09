from vpython import *   # Import vpython so that we can visualise the programming
import random as rand
import numpy as np
import math
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#from matplotlib import cm
#from collections import namedtuple, OrderedDict
#import turtle



a = (rand.uniform(-10,10))
b = (rand.uniform(-5,5))# Defining 4 different random values to randomise velocity or location 
c = (rand.uniform(-10,10))
d = (rand.randint(7,15))

#planet spawn with set properties
Planet  = sphere(pos = vector(0,0,0), radius=6.371, texture= textures.stucco, opacity = 0.8, shininess = 0, color = vector(2,18,47), emissive=False)
#satellite spawned in as well with randomised spawn point
sat  = sphere(pos = vector(d,b,b), radius=0.5, color = vector(0.5,0.2,0.2), texture= textures.stucco, shininess = 0, make_trail=True, #trail_type="points",
              interval=2, retain=120000, trail_color = vector(1,1,1), trail_radius=0.1)
sitx  = sphere(pos = vector(d,b,b), radius=0.5, color = vector(1,1,1), make_trail=True, #trail_type="points",
              interval=2, retain=120000, trail_color = vector(1,1,1), trail_radius=0.1)
sitz  = sphere(pos = vector(d,b,b), radius=0.5, color = vector(1,1,1), make_trail=True, #trail_type="points",
              interval=2, retain=120000, trail_color = vector(0.3,1,1), trail_radius=0.1)
sitx.velocity = vector(5,0,0)
sitz.velocity = vector(0,0,5)
#M1 is planet mass
M1 = 5.9722*(10**24)
Masspervolume = M1/(108*(10**10))   #mass of planet divided by volume of planet
M2 = Masspervolume*((4/3)*pi*(0.5**3))    #Mass of satellite
#Gravitational constant
G = 6.674*(10**-11)


sat.velocity = vector(a,b,c)    # Establishing ball velocity

#dt set small so frequent reiterations
dt = 0.04
counter = 0 #set counter to 0

#Sat velocity established from vectors. Rounding set to 0 decimal points
actualsatvelocity = round((sqrt(a**2+b**2+c**2))*1000,0)
mach = round((actualsatvelocity/299792)*100,2)  #Not supposed to say mach but cba to change it. Percentage of the speed of light set to 2 dp

#Print velocities and respective speeds of satellite
print("The satellite is moving with a velocity of", str(actualsatvelocity),"km/s, along the vector of", str(sat.velocity),)
print("This is equivalent to", str(mach),"% of the speed of light")

   # Update the ball position a small time dt later
sat.pos = sat.pos + sat.velocity * dt

while True:   # This is so that it will loop indefinitely 
   rate(25)   # So it has a refesh loop rate of once every 1/25th of a second
   
   sitx.pos = sitx.pos + sitx.velocity * dt
   sitz.pos = sitz.pos + sitz.velocity * dt
   spradius = sat.pos - Planet.pos                          #Not effective in this but means if planet was moving then radius is still calculated properly. Just a constantly updating radius vector.

   #angle1 = math.atan((spradius.y)/(spradius.x))*180/pi     #angle between x and y
   #hypxy = sqrt(spradius.y**2+spradius.x**2)                #Hypotenuse between x and y to use for our z calculation
   #angle2 = math.atan((spradius.z)/hypxy)*180/pi            #angle between xy plane and z

   angle1 = math.atan((spradius.z)/(spradius.x))*180/pi     #angle between x and y
   hypxy = sqrt(spradius.z**2+spradius.x**2)                #Hypotenuse between x and y to use for our z calculation

   if spradius.z < 0:
      hypxy = -hypxy 
   if spradius.x < 0:
      hypxy = -hypxy
   
   angle2 = math.atan((spradius.y)/hypxy)*180/pi  

   sinanglecheck = math.sin(angle2*pi/180)                  #logic check

   Satelliteradius = sqrt(d**2+b**2+b**2)   #Turn sat spawn point into a scalar distance from (0,0,0)
   scalarspradius = (sqrt(spradius.x**2+spradius.y**2+spradius.z**2))*1000000

   F = (G*M1*M2)/(scalarspradius**2) #Newtonian Gravity
   Acc = F/M2     #F=ma. Turn Force into acceleration
   
   dv = Acc*dt    #Create change in velocity

   #dvz = dv*math.sin(angle2*pi/180)
   #dvx = dvz*math.cos(angle1*pi/180)
   #dvy = dvz*math.sin(angle1*pi/180)

   #dvy = math.sin(angle2*pi/180)
   #dvz = math.cos(angle2*pi/180)*math.sin(angle1*pi/180)
   #dvx = math.cos(angle2*pi/180)*math.sin(angle1*pi/180)

   hyp2 = sqrt(spradius.y**2+hypxy**2)

   dvy = -dv*math.sin(angle2*pi/180)
   dvz = -dv*math.cos(angle2*pi/180)*math.sin(angle1*pi/180)
   dvx = -dv*math.cos(angle2*pi/180)*math.cos(angle1*pi/180)
   
   
   
   dvv = vector(dvx,dvy,dvz)     #vector of change in velocity
   dvvs = sqrt((dvx)**2+(dvy)**2+(dvz)**2)      #change in velocity scalar

   sat.velocity = vector(sat.velocity.x+dvx,sat.velocity.y+dvy,sat.velocity.z+dvz)

   sat.pos = sat.pos + sat.velocity*dt + 1/2*dvv*dt
   
   satcheck = sqrt(sat.pos.x**2+sat.pos.y**2+sat.pos.z**2)     #Checking position of satellite relative to edge of circle

   actualsatvelocity1 = round((sqrt(sat.velocity.x**2+sat.velocity.y**2+sat.velocity.z**2))*1000,0)
   mach1 = round((actualsatvelocity1/299792)*100,2)
   Forceimpact = round((((Acc*M2)+((M2*(actualsatvelocity1*1000))/100))/(6.3*(10**13))/1000),1)

   if satcheck <= 6.881:
      print('The satellite collided at ', str(actualsatvelocity1),'km/s. This is ', str(mach1),'% the speed of light.')
      print('It impacted with the equivalent of ', str(Forceimpact),'thousand times the energy of the Hiroshima bomb.')  
   
   if satcheck <= 6.851:         #If at circle edge add a counter. Circle edge made bigger to account for touching at planet and sat edges.
      counter = counter + 1

   if counter == 1:        #Once touching circle. Stop the satellite.
      sat.velocity = 0

   if sat.velocity == 0:
      print('The satellite has collided with the planet')
      
   #print (str(angle2))
   #print (str(sinanglecheck))
   #print (str(spradius))
   #print (str(hypxy))
   #print (str(scalarspradius),'metres')
  # print(str(dvv))
   #print(str(dv))
  # print(str(sat.velocity))
   #print(str(sat.pos))
      



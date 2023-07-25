# Closed-Gravitational-Force-Simulation
Hi there, this is a Gravitational Force simulation, applying the Universal Newton's Law for Gravity in python using pygame and math libraries.
<img align="right" src="https://thumbs.gfycat.com/DimPowerlessBallpython-size_restricted.gif" width="180">
This project simply applies the equation F = G.m1.m2./d^2 
and works with collisions with the well-known quantity of
motion conservation. 
Other features:
> It uses a logic based on difference of masses between blocks in collision to deal with "absorbtion" features and pseudo black holes creation;
> The list of blocks created when the program is started can be modified (at least for now) just directly in the code, it is definied between lines 199-205, blocks' traits are, in this order: self position on the x axis, self position on the y axis, color, mass, radius, initial velocity at the x axis, initial velocity at the y axis:
``` python
class  Bloco:
	def  __init__(self,x,y,cor,massa,raio,x_vel,y_vel):
```
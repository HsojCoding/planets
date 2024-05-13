from tkinter import * 

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x+other.x, self.y+other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x+other, self.y+other)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x-other.x, self.y-other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x-other, self.y-other)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x*other.x, self.y*other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x*other, self.y*other)
        else:
            raise TypeError("Unsupported operand type for *")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def cross_product(self, other):
        return (self.x*other.y)-(self.y*other.x)

    def magnitude(self):
        return (self.x**2 + self.y**2) **0.5

class Planet:
    def __init__(self, mass: float, initial_speed: Vector2, initial_location: Vector2):
        self.mass = mass
        self.speed = initial_speed
        self.position = initial_location
        self.initial_speed = initial_speed
        self.initial_position = initial_location
        self.position_weight = self.position*mass

    def Precess(self, force: Vector2, time: float):
        acceleration = force*(1/self.mass)
        self.speed += acceleration * time
        self.position += self.speed * time


def drawPlanet(canvas, coords: Vector2, name):
    canvas.delete(f'{name}')
    x0, y0, x1, y1 = coords.x-4, coords.y-4, coords.x+4, coords.y+4
    canvas.create_oval(x0, y0, x1, y1, outline='black', fill='blue', tags=f'{name}')


def drawLine(canvas, old_coords, new_coords, line_no):
    canvas.create_line(old_coords.x, old_coords.y, new_coords.x, new_coords.y, fill='red', width=2, tags=f'line_no{line_no}')


def calculate_gravitational_force(planet1: Planet, planet2: Planet):
    G = 6.674e-11
    distance_vector = planet2.position - planet1.position
    distance = distance_vector.magnitude()

    force_magnitude = (G*planet1.mass*planet2.mass)/(distance**2)
    force_direction = distance_vector*(1/distance)
    return force_magnitude*force_direction


def calc_planet_positions(p1:Planet, p2:Planet, time_interval):
    force_p1_p2 = calculate_gravitational_force(p1, p2)
    force_p2_p1 = calculate_gravitational_force(p2, p1)

    p1.Precess(force_p1_p2, time_interval)
    p2.Precess(force_p2_p1, time_interval)


def planetCoordsToCOM(p1: Planet, p2: Planet):
    x_com = ((p1.mass*p1.position.x)+(p2.mass*p2.position.x))/(p1.mass+p2.mass)
    y_com = ((p1.mass*p1.position.y)+(p2.mass*p2.position.y))/(p1.mass+p2.mass)

    com = Vector2(x_com, y_com)

    rel_pos1 = p1.position-com
    rel_pos2 = p2.position-com

    return rel_pos1, rel_pos2


def planetsToCanvasCoords(p1: Planet, p2: Planet):
    p1_com, p2_com = planetCoordsToCOM(p1, p2)
    larger_val = max(abs(p1_com.magnitude()), abs(p2_com.magnitude()))
    max_val = larger_val*1.1
    
    p1_ratio = (p1.position*(1/max_val))
    p2_ratio = (p2.position*(1/max_val))
    
    p1_coords = (500*p1_ratio)
    p2_coords = (500*p2_ratio)

    return p1_coords, p2_coords


def planetsToCanvasCoords2(p1: Planet, p2: Planet, com: bool = 1):
    if com:
        p1_com, p2_com = planetCoordsToCOM(p1, p2)
    if not com:
        p1_com = p1.position
        p2_com = p2.position
    #larger_val = max(abs(p1_com.magnitude()), abs(p2_com.magnitude()))
    max_val = (151e6)*2

    
    p1_ratio = (p1_com*(1/max_val))
    p2_ratio = (p2_com*(1/max_val))
    
    p1_coords = (500*p1_ratio)+500
    p2_coords = (500*p2_ratio)+500
    
    return p1_coords, p2_coords

line_no = 0
def precessPlanets(canvas, planet1: Planet, planet2: Planet, remove_trail: bool = 0):
    # trail removing
    global line_no
    line_no+=1
    trail_length = 1000
    if remove_trail:
        trail_length = 1000
    if int(line_no) > int(trail_length):
        canvas.delete(f'line_no{line_no-(trail_length)}')
    
    p1_prev_pos, p2_prev_pos = planetsToCanvasCoords2(planet1, planet2)
    calc_planet_positions(planet1, planet2, 10)
    p1_coords, p2_coords = planetsToCanvasCoords2(planet1, planet2)
    drawPlanet(canvas, p1_coords, 'p1')
    drawLine(canvas, p1_prev_pos, p1_coords, line_no)
    drawPlanet(canvas, p2_coords, 'p2')
    drawLine(canvas, p2_prev_pos, p2_coords, line_no)
    canvas.after(1, precessPlanets, canvas, planet1, planet2)


root = Tk()
root.title("Simulation")

sun_pos = Vector2(0,0)
sun_vel = Vector2(-1e6,0)
sun = Planet(mass = 2e30, initial_speed = sun_vel, initial_location = sun_pos) 

earth_pos = Vector2(151e6, 0)

G = 6.674e-11
v0 = (G*sun.mass/earth_pos.x)**0.5 # Apprx orbital velocity based on 

earth_vel = Vector2(0,v0)
earth = Planet(mass = 2e30, initial_speed = earth_vel, initial_location = earth_pos)

#canvas
canvas = Canvas(root, width = 1000, height = 1000, bg='white')
canvas.pack()

precessPlanets(canvas, sun, earth, 1)

root.mainloop()
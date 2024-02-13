import numpy as np

class Body(object):
    def __init__(self, mass, radius, pos, velocity=(0, 0)):
        self.mass = mass
        self.r = radius
        self.pos = np.array(pos).astype(np.float64)
        self.vel = np.array(velocity)
        self.g = 6.674 * (10**-11)
        self.simspeed = 6000000

    def calc(self, body2, dt, size: tuple):
        dt = dt * self.simspeed
        direction = body2.pos - self.pos
        distance = np.linalg.norm(direction)
        magnitude = direction/distance

        # get the vector components of force
        f = (self.g * self.mass * body2.mass) / (distance**2)
        fvec = f*magnitude

        # calc acceleration
        acceleration = fvec/self.mass

        # calc vel
        self.vel = self.vel + acceleration * dt

        # collision reflection
        if distance <= self.r+body2.r:
            self.vel -= 2 * np.dot(self.vel, magnitude) * magnitude
            self.vel *= 0.9
            self.col += (self.r + body2.r - distance) * magnitude / 2

        # boundary reflection
        if 0+self.r > self.pos[0] or self.pos[0] >= size[0]-self.r:
            self.vel[0] *= -0.95
        if 0+self.r > self.pos[1] or self.pos[1] >= size[1]-self.r:
            self.vel[1] *= -0.95


    def update(self, dt):
        self.pos += self.vel * dt * self.simspeed
        self.col = 0



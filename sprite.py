import pygame
import vector as v
import math


class Sprite:
    """
    Class to define the general behaviour of sprites in the game
    Stores the sprite's image and has methods to handle movement and collisions
    """

    def __init__(self, game, image, scale, init_pos=(0, 0), init_velocity=(0, 0), init_angular_velocity=0, init_angle=0):
        """
        Constructor method for the sprite class.

        :param game:
        :param image:
        :param scale:
        :param init_pos:
        :param init_velocity:
        :param init_angular_velocity:
        """
        self.game = game
        self.screen_dims = pygame.display.get_window_size()
        self.scale = (scale[0], scale[1])

        # self.image = pygame.image.load(image_path)
        # self.image = self.image.convert_alpha(self.image)
        self.image = image
        # Scale image to correct size
        self.scaled_image = pygame.transform.scale(self.image, scale)

        # Initialise vectors for position, velocity and acceleration
        self.position = v.vector(init_pos[0], init_pos[1])
        self.velocity = v.vector(init_velocity[0], init_velocity[1])
        self.acceleration = v.vector()
        self.accelerating = False

        # Initialise the angle and direction of the sprite
        self.direction = v.vector()  # A unit vector to represent the sprite's direction
        self._angle = 0  # Angle in radians clockwise from the y-axis (0 is pointing straight up)
        self.angle = init_angle
        self.angular_velocity = init_angular_velocity  # Angular velocity in rad/s
        self.rotating = 0

    def update(self):
        """
        Method to update the sprite by calculating its position for the next frame
        Uses Euler integration to calculate the updated position, velocity and rotation
        """
        dt = self.game.dt*10   # Simulation timestep

        # Integrate to get the new position and velocity
        self.position = self.position + self.velocity * dt
        self.velocity = self.velocity + self.acceleration * dt

        self.angle = self.angle + self.angular_velocity * dt

        self.check_edges()

    def check_edges(self):
        """
        Method to check whether the sprite has reached the edge of the screen and wrap it around if so
        """
        if self.position.x < 0:
            self.position = v.vector(self.screen_dims[0], self.position.y)
        elif self.position.x > self.screen_dims[0]:
            self.position = v.vector(0, self.position.y)

        if self.position.y < 0:
            self.position = v.vector(self.position.x, self.screen_dims[1])
        elif self.position.y > self.screen_dims[1]:
            self.position = v.vector(self.position.x, 0)

    def check_collision(self, other):
        """
        Method to check if the sprite has collided with another passed in as other

        :param other:
        """
        collided = False

        if other.corners()[0][0] < self.position.x < other.corners()[2][0]:
            if other.corners()[0][1] < self.position.y < other.corners()[2][1]:
                collided = True

        return collided

    def corners(self):
        """
        Method to return a tuple of each of the sprite's corners.
        Starts from the top left, going clockwise
        :return corners:
        """
        c1 = (self.position.x - self.scale[0]/2, self.position.y - self.scale[1]/2)
        c2 = (self.position.x + self.scale[0]/2, self.position.y - self.scale[1]/2)
        c3 = (self.position.x + self.scale[0]/2, self.position.y + self.scale[1]/2)
        c4 = (self.position.x - self.scale[0]/2, self.position.y + self.scale[1]/2)
        corners = (c1, c2, c3, c4)
        return corners

    def draw(self):
        """
        Method to draw the sprite onto the screen
        """
        # Rotate image (angle is stored in radians clockwise from 0, has to be converted to degrees anticlockwise)
        rotated_image = pygame.transform.rotate(self.scaled_image, self.angle*(-180/math.pi))
        # Calculate a position to display the sprite, correcting for the error caused by
        #   rotation and scaling
        w, h = rotated_image.get_size()
        display_pos = (self.position[0] - (w / 2), self.position[1] - (h / 2))
        # Draw image to screen
        self.game.screen.blit(rotated_image, display_pos)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self.direction = v.vector(math.sin(new_angle), -math.cos(new_angle))

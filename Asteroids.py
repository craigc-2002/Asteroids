"""
Asteroids
Craig Cochrane, 2022

My version of Asteroids, written in python using pygame for graphics
"""
import math
import pygame
import random as r

import vector as v
import sprite
import image_loader

"""
TO DO:
- Implement UFO
- Add sounds
"""


class Rocket(sprite.Sprite):
    """
    Class to represent the rocket and give it some necessary methods
    Child class of Sprite
    """

    def __init__(self, game):
        screen_dims = pygame.display.get_window_size()
        self.start_pos = (screen_dims[0] / 2, screen_dims[1] / 2)

        image = game.sprite_images["rocket"]
        flames_image = game.sprite_images["rocket_flames"]
        self.flames_image = pygame.transform.scale(flames_image, (75, 116))
        self.normal_image = pygame.transform.scale(image, (75, 75))

        super().__init__(game, image, (75, 75), self.start_pos)

    def reset(self):
        """
        Method to reset the rocket's position on a new game
        """
        self.position = v.vector(self.start_pos[0], self.start_pos[1])
        self.velocity = v.vector()
        self.acceleration = v.vector()
        self.angle = 0

        self.accelerating = False
        self.rotating = 0

        self.draw()

    def update(self):
        """
        Overloaded update method for the Rocket class. Sets the acceleration and angular velocity
        of the rocket depending on keyboard inout and current speed
        """
        # Set acceleration depending on whether the A key has been pressed
        if self.accelerating:
            self.acceleration = self.direction * 5
        elif self.velocity.mag > 0:
            self.acceleration = self.velocity.unit * (-0.4)
        else:
            self.acceleration = v.vector()

        # Set angular velocity depending on whether the a or d keys have been pressed
        if self.rotating == 1:
            self.angular_velocity = -0.9
        elif self.rotating == 2:
            self.angular_velocity = 0.9
        else:
            self.angular_velocity = 0

        for asteroid in self.game.asteroids:
            if self.check_collision(asteroid):
                asteroid.destroy()
                self.game.new_life()
        for beam in self.game.laser_beams:
            if self.check_collision(beam) and beam.elapsed > 50:
                self.game.new_life()

        self.rotating = 0
        super().update()

    def draw(self):
        """
        Method to change the image used by the rocket if it's accelerating
        """
        if self.accelerating:
            self.scaled_image = self.flames_image
        else:
            self.scaled_image = self.normal_image

        self.accelerating = False
        super().draw()

    def move_forward(self):
        self.accelerating = True

    def turn_left(self):
        self.rotating = 1

    def turn_right(self):
        self.rotating = 2

    def fire(self):
        """
        Method to fire a laser beam
        """
        speed = self.direction * 100
        new_beam = Laser(self.game, (self.position[0], self.position[1]), speed, start_angle=self.angle)
        self.game.laser_beams.append(new_beam)
        self.game.display_objects.append(new_beam)


class Asteroid(sprite.Sprite):
    """
    Class to represent the asteroids and give them the necessary methods
    Child class of Sprite
    """

    def __init__(self, game, size, init_pos=(0, 0), image=None):
        img_scale = (0, 0)
        match size:
            case 1:
                img_scale = (100, 100)
            case 2:
                img_scale = (150, 150)
            case 3:
                img_scale = (200, 200)

        self.size = size
        self.screen_dims = pygame.display.get_window_size()
        init_conditions = self.initial_conditions()
        if size != 3:
            init_conditions[0] = init_pos

        if image is None:
            image_options = (
                game.sprite_images["asteroid1"], game.sprite_images["asteroid2"], game.sprite_images["asteroid3"])
            image = r.choice(image_options)

        # Call the sprite class constructor
        super().__init__(game, image, img_scale, init_conditions[0], init_conditions[1], init_conditions[2])

    def initial_conditions(self):
        """
        Method to calculate initial values for position, velocity and angular velocity

        All values are calculated to be within sensible values and the position is checked
        so that it isn't too near the player
        :return initial_conditions:
        """
        init_conditions = []
        # Assign the asteroid a random position
        # Starts by assigning the position in the centre, then repeatedly calculates new values until it is away
        # from the centre
        position = (self.screen_dims[0] / 2, self.screen_dims[1] / 2)
        while ((self.screen_dims[0] / 2) + 150 > position[0] > (self.screen_dims[0] / 2) - 150) and (
                (self.screen_dims[0] / 2) + 150 > position[0] > (self.screen_dims[0] / 2) - 150):
            position = (r.randint(0, self.screen_dims[0]), r.randint(0, self.screen_dims[1]))
        init_conditions.append(position)

        # Assign the asteroid a speed in the x and y axes
        rand_speed = lambda min_speed, max_speed: r.choice((-1, 1)) * (
                r.randint(min_speed, max_speed) + ((1 / r.randint(1, 10)) * r.randint(0, 1)))
        speed_range = ()
        match self.size:
            case 3:
                speed_range = (5, 8)
            case 2:
                speed_range = (7, 10)
            case 1:
                speed_range = (10, 13)

        velocity = (rand_speed(speed_range[0], speed_range[1]), rand_speed(speed_range[0], speed_range[1]))
        init_conditions.append(velocity)

        # Assign the asteroid a random angular velocity
        angular_velocity = r.choice((-1, 1)) * (1 / r.randint(1, 10))
        init_conditions.append(angular_velocity)

        return init_conditions

    def reset(self):
        """
        Method to reset the asteroid to a new position and velocity
        :return:
        """
        reset_conditions = self.initial_conditions()

        self.position = v.vector(reset_conditions[0][0], reset_conditions[0][1])
        self.velocity = v.vector(reset_conditions[1][0], reset_conditions[1][1])
        self.angle = reset_conditions[2]

        self.draw()

    def destroy(self, laser=False):
        """
        Method to destroy the asteroid if it hits the player or a laser
        If hit by a laser, laser is passed in as True and the player will not get any points
        :param laser:
        """
        if self.size > 1:
            for i in range(2):
                new_asteroid = Asteroid(self.game, self.size - 1, (self.position[0], self.position[1]), self.image)
                self.game.asteroids.append(new_asteroid)
                self.game.display_objects.append(new_asteroid)

        new_score = 0
        match self.size:
            case 3:
                new_score = 20
            case 2:
                new_score = 50
            case 1:
                new_score = 100

        if laser:
            self.game.score += new_score
        self.game.asteroids.remove(self)
        self.game.display_objects.remove(self)
        del self


class Laser(sprite.Sprite):
    """
    Class to represent the laser beam fired from the rocket
    """

    def __init__(self, game, start_pos, start_velocity, start_angle):
        image = game.sprite_images["laser"]
        self.start_time = pygame.time.get_ticks()
        self.elapsed = 0
        super().__init__(game, image, (5, 20), start_pos, start_velocity, init_angle=start_angle)

    def update(self):
        destroyed = False
        for asteroid in self.game.asteroids:
            if self.check_collision(asteroid):
                asteroid.destroy(True)
                destroyed = True

        self.elapsed = pygame.time.get_ticks() - self.start_time
        if self.elapsed > 1000:
            destroyed = True

        if destroyed:
            self.destroy()
        else:
            super().update()

    def destroy(self):
        self.game.laser_beams.remove(self)
        self.game.display_objects.remove(self)
        del self


class Asteroids:
    """
    Main Asteroids game class
    """

    def __init__(self):
        # ---Initialise pygame and screen---
        pygame.init()
        window_width = 1280
        window_height = 720

        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Helvetica", 30)
        self.title_font = pygame.font.SysFont("Helvetica", 100)

        self.background_image = pygame.image.load("assets/background.png")
        self.background_image = self.background_image.convert_alpha()

        # ---Initialise game objects and variables---
        self.lives = 3
        self.score = 0
        self.dt = 0.01

        image_index = {"rocket": ((1, 17), (10, 27)),
                       "rocket_flames": ((11, 17), (20, 32)),
                       "asteroid1": ((1, 1), (16, 16)),
                       "asteroid2": ((17, 1), (32, 16)),
                       "asteroid3": ((33, 1), (48, 16)),
                       "laser": ((40, 18), (41, 19))}
        self.sprite_images = image_loader.get_textures("assets/textures.png", image_index)

        self.rocket = Rocket(self)
        self.asteroids = []  # Empty list to contain the asteroids on screen
        self.laser_beams = []
        self.display_objects = []

        # ---Enter the title page---
        self.title_screen()

    def title_screen(self):
        """
        Method to make and loop the title screen.
        Calls the main game loop when the mouse is pressed
        """
        bg_asteroids = []

        title_text = "ASTEROIDS"
        init_title_text_img = self.title_font.render(title_text, True, (255, 255, 255))

        subtitle_text = "CLICK TO START GAME"
        subtitle_text_img = self.font.render(subtitle_text, True, (255, 255, 255))

        dt = 0.01
        t = 0

        for i in range(2):
            new_asteroid = Asteroid(self, 3)
            bg_asteroids.append(new_asteroid)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_game()

            self.screen.blit(self.background_image, (0, 0))
            for asteroid in bg_asteroids:
                asteroid.update()
                asteroid.draw()

            # Scale the title text to make it pulse slowly
            scale_size = (init_title_text_img.get_size()[0] + 40 * math.sin(0.5 * math.pi * t),
                          init_title_text_img.get_size()[1] + 10 * math.sin(0.5 * math.pi * t))
            title_text_img = pygame.transform.scale(init_title_text_img, scale_size)
            t += dt

            # Display the title and subtitle text
            self.screen.blit(title_text_img, img_display_pos(title_text_img, (640, 275)))
            self.screen.blit(subtitle_text_img, img_display_pos(subtitle_text_img, (640, 350)))

            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))

            pygame.display.flip()  # display the screen updates
            self.clock.tick(60)  # run at 60 FPS

    def start_game(self):
        """
        Method to start the game
        Calls the main game loop once the objects and variables are set up
        """
        self.lives = 3
        self.score = 0
        self.dt = 0.01

        self.asteroids = []  # Empty list to contain the asteroids on screen
        self.laser_beams = []
        self.rocket.reset()

        self.display_objects = [self.rocket]
        for i in range(3):
            self.add_asteroid()

        self.game_loop()

    def game_loop(self):
        # ---Main game loop---
        while True:
            # Handle the event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.rocket.fire()

            # Get a list of keys currently being pressed
            key_input = pygame.key.get_pressed()
            # If the w key is being pressed
            if key_input[pygame.K_w]:
                self.rocket.move_forward()
            if key_input[pygame.K_a]:
                self.rocket.turn_left()
            if key_input[pygame.K_d]:
                self.rocket.turn_right()

            # Update the objects on screen
            self.screen.blit(self.background_image, (0, 0))

            for i in self.display_objects:
                i.update()
                i.draw()

            if len(self.asteroids) < 3:
                for i in range(r.randint(1,4)):
                    self.add_asteroid()

            top_text = "Score: " + str(self.score) + "     " + "Lives: " + str(self.lives)
            top_text_img = self.font.render(top_text, True, (255, 255, 255))
            self.screen.blit(top_text_img, (20, 20))

            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))

            pygame.display.flip()  # display the screen updates
            frame_time = self.clock.tick(60)
            self.dt = frame_time / 1000  # set time step to time taken by previous frame (in s)

    def new_life(self):
        """
        Method to reset the game for a new point
        """
        self.lives -= 1
        if self.lives < 0:
            self.game_over()

        for beam in self.laser_beams:
            beam.destroy()
        self.rocket.reset()
        self.game_loop()

    def game_over(self):
        """
        Method to handle the end of the game
        """
        bg_asteroids = []

        title_text = "GAME OVER"
        init_title_text_img = self.title_font.render(title_text, True, (255, 255, 255))

        subtitle_text = "CLICK TO RESTART"
        subtitle_text_img = self.font.render(subtitle_text, True, (255, 255, 255))

        dt = 0.01
        t = 0

        for i in range(2):
            new_asteroid = Asteroid(self, 3)
            bg_asteroids.append(new_asteroid)

        new_highscore = False
        highscore_text_img = None
        f = open("assets/highscore.txt", "r")
        lines = f.read()
        print(type(lines))
        if int(lines) < self.score:
            f.close()
            f = open("assets/highscore.txt", "w")
            f.write(str(self.score))
            new_highscore = True
        f.close()

        if new_highscore:
            highscore_txt_img = self.title_font.render("NEW HIGH SCORE", True, (255, 255, 255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_game()

            self.screen.blit(self.background_image, (0, 0))
            for asteroid in bg_asteroids:
                asteroid.update()
                asteroid.draw()

            # Scale the title text to make it pulse slowly
            scale_size = (init_title_text_img.get_size()[0] + 40 * math.sin(0.5 * math.pi * t),
                          init_title_text_img.get_size()[1] + 10 * math.sin(0.5 * math.pi * t))
            title_text_img = pygame.transform.scale(init_title_text_img, scale_size)
            t += dt

            # Display the title and subtitle text
            self.screen.blit(title_text_img, img_display_pos(title_text_img, (640, 225)))
            self.screen.blit(subtitle_text_img, img_display_pos(subtitle_text_img, (640, 325)))

            # Render and display the final score
            score_text = "SCORE: {}".format(self.score)
            score_text_img = self.title_font.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_text_img, img_display_pos(score_text_img, (640, 480)))

            # Render display new high score text if applicable
            if new_highscore:
                self.screen.blit(highscore_txt_img, img_display_pos(highscore_txt_img, (640, 600)))

            # Render and display FPS
            fps_text = str(round(self.clock.get_fps()))
            fps_text_img = self.font.render(fps_text, True, (255, 255, 255))
            self.screen.blit(fps_text_img, (1220, 20))

            pygame.display.flip()  # display the screen updates
            self.clock.tick(60)  # run at 60 FPS

    def add_asteroid(self):
        new_asteroid = Asteroid(self, 3)
        self.asteroids.append(new_asteroid)
        self.display_objects.append(new_asteroid)


def img_display_pos(img, pos: tuple) -> tuple:
    """
    Function to take in an image and the desired centre coordinates and return the top-left corner coordinates
    :param img:
    :param pos:
    :return display_pos:
    """
    size = img.get_size()
    display_pos = (
        pos[0]-size[0]/2,
        pos[1]-size[1]/2
    )
    return display_pos


if __name__ == "__main__":
    Asteroids()

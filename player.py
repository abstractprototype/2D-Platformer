import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.10
        # start with the idle animation folder and start at frame 0
        self.image = self.animations['idle'][self.frame_index]
        # this rectangle will be the sword and follows the self.collision_rect rectangle
        self.rect = self.image.get_rect(topleft=pos)

        # dust particles
        # dust particles are going to be apart of the screen not the player
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        # pushes player down 0.8 but the vertical collision pushes player back up to 0 constantly
        self.gravity = 0.8
        self.jump_speed = -16
        self.double_jump = 0
        # create a new rectangle to seperate the sword from the player # make a rectangle starting from top left for the player from self.rect
        self.collision_rect = pygame.Rect(
            self.rect.topleft, (50, self.rect.height))  # dont include the sword in collision with environment only enemies # 50 width because of measured size on pirate in photoshop(so a different sprite will have to change this number)

        # player status
        self.status = 'idle'
        self.facing_right = True  # false if facing_left
        # check all the player collisions
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500  # invincible for 500 milliseconds
        self.hurt_time = 0  # timer for when the player collided with enemy

        # audio
        self.jump_sound = pygame.mixer.Sound('./audio/effects/jump.wav')
        self.jump_sound.set_volume(0.2)
        self.hit_sound = pygame.mixer.Sound('./audio/effects/hit.wav')

    # gets the file path to the folder containing all the png frames of one action
    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder(
            './graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # drawing the player if hes facing right or left
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image  # if facing right then default right image
            # makes the sword rectangle follow the player rectangle
            # attaches the sword rectangle from the bottom left
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(
                image, True, False)  # flip the image to the left
            self.image = flipped_image
            # makes the sword rectangle follow the player rectangle
            # attaches the sword rectangle from the bottom right
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:  # sets transparency of player if hurt
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:  # if not hurt then set full transparency
            self.image.set_alpha(255)

        # fixes the animation where player jumps in midair
        # problem is: pygame always tries to put self.image on topleft of self.rect
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # commented out code because we don't need a static rectangle anymore
        #     # set the rectangle for collisions for every direction
        # if self.on_ground and self.on_right:  # if player is touching ground AND touching something on the right side
        #     # set bottomright of player to bottomright
        #     self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        # elif self.on_ground:
        #     self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # elif self.on_ceiling and self.on_right:  # if player touching ceiling and touching something on right side
        #     self.rect = self.image.get_rect(
        #         topright=self.rect.topright)  # set player to topright
        # elif self.on_ceiling and self.on_left:
        #     self.rect = self.image.get_rect(topleft=self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:  # greater than 1 because of our gravity at 0.8
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        # changed from rect to collision_rect to fix sword collision bug
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):  # more info on video at 59:51
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:  # timer to turn off invicibility
                self.invincible = False

    def wave_value(self):  # called wave value because not exactly a sin value
        # value returns between 1 and -1, but we need 255 and 0 for transparency
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255  # full image
        else:
            return 0  # invisible image

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()

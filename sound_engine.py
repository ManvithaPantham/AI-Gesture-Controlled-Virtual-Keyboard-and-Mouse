import pygame


class SoundEngine:

    def __init__(self):

        pygame.mixer.init()

        self.key_sound = pygame.mixer.Sound("sounds/type.wav.mp3")

    def play(self):

        self.key_sound.stop()      # Prevent overlapping sounds
        self.key_sound.play()
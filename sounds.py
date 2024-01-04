import pygame


class All_Sounds:
    def __init__(self):
        self.sounds = {}
        self.sounds_volume = 1
        self.channels_num = 2

    def change_sounds_volume(self):
        self.sounds_volume = 1 - self.sounds_volume
        for val in self.sounds.values():
            val[0].set_volume(self.sounds_volume)

    def add_sound(self, name):
        channel = pygame.mixer.Channel(self.channels_num)
        self.channels_num += 1
        sound = pygame.mixer.Sound(name)
        sound.set_volume(self.sounds_volume)
        self.sounds[name] = [sound, channel]

    def play_sound(self, name):
        sound, channel = self.sounds[name]
        channel.play(sound, loops=0)


class Background_music:
    def __init__(self):
        self.music = {}
        self.music_volume = 0.5
        self.channels_num = 0

    def change_music_volume(self, num):
        self.music_volume = num
        for val in self.music.values():
            val[0].set_volume(self.music_volume)

    def add_music(self, name):
        channel = pygame.mixer.Channel(self.channels_num)
        self.channels_num += 1
        music = pygame.mixer.Sound(name)
        music.set_volume(self.music_volume)
        self.music[name] = [music, channel]

    def play_music(self, name):
        music, channel = self.music[name]
        if channel.get_busy():
            channel.unpause()
        else:
            channel.play(music, loops=-1)

    def stop_music(self, name):
        music, channel = self.music[name]
        channel.pause()


all_sounds = All_Sounds()
background_music = Background_music()
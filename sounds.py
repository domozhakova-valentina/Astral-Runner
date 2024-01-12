import pygame


class All_Sounds:
    def __init__(self):
        self.sounds = {}
        self.sounds_volume = 1
        self.channels_num = 2

    def change_sounds_volume(self, num):
        self.sounds_volume = 1 - num
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
        self.state = 1

    def change_music_volume(self, num):
        self.music_volume = num
        if self.state:
            for val in self.music.values():
                val[0].set_volume(self.music_volume)

    def change_music_state(self, state):
        self.state = state
        if self.state == 0:
            for val in self.music.values():
                val[0].set_volume(0)
        else:
            self.change_music_volume(self.music_volume)

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
        if name == 'sound/game_music.mp3':
            channel.stop()
        else:
            channel.pause()


sounds_list = ['sound/damage.mp3', 'sound/explosion.mp3', 'sound/get_coin.wav', 'sound/jump.ogg', 'sound/shot.wav',
               'sound/step.wav', 'sound/game over.mp3', 'sound/win.wav']
music_list = ['sound/menu_music.mp3', 'sound/game_music.mp3']

all_sounds = All_Sounds()
background_music = Background_music()

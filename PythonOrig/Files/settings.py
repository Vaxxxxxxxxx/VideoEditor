class Settings:
    def __init__(self, params):

        # music_folder, background_path, effect_style,
        # audio_bar_style, background_style, number_of_tracks,screen_width, screen_height, mode):
        # Assign to self object
        self.__music_folder = params[0]
        self.__background_path = params[1]
        self.__effect_style = params[2]
        self.__audio_bar_style = params[3]
        self.__background_style = params[4]
        self.__number_of_tracks = params[5]
        self.__screen_width = params[6]
        self.__screen_height = params[7]
        self.__mode = params[8]

    # Getters
    @property
    def get_music_folder(self):
        return self.__music_folder

    @property
    def get_background_path(self):
        return self.__background_path

    @property
    def get_effect_style(self):
        return self.__effect_style

    @property
    def get_audio_bar_style(self):
        return self.__audio_bar_style

    @property
    def get_background_style(self):
        return self.__background_style

    @property
    def get_number_of_tracks(self):
        return self.__number_of_tracks

    @property
    def get_screen_width(self):
        return self.__screen_width

    @property
    def get_screen_height(self):
        return self.__screen_height

    @property
    def get_mode(self):
        return self.__mode

"""
--------------------------
  Clarifications
--------------------------

4 different modes:
mode = 0 (<number> of random tracks from the folder + image)
-----
mode = 1 (<number> of random tracks from the folder + image + effect)
-----
mode = 2 (<number> of random tracks from the folder + image + effect + responsive bars)
mode = 2 (<number> of random tracks from the folder + image          + responsive bars)
-----
mode = 3 (<number> of random tracks from the folder + image + effect + responsive bars + responsive background)
mode = 3 (<number> of random tracks from the folder + image          + responsive bars + responsive background)
mode = 3 (<number> of random tracks from the folder + image + effect                   + responsive background)
mode = 3 (<number> of random tracks from the folder + image                            + responsive background)

2 different audio bar styles:
audio_bar_style = 0 (disabled)
audio_bar_style = <bar style> (enabled)

2 different background styles:
background_style = 0 (disabled)
background_style = <background style> (enabled)

2 different effect styles:
effect_style = 0 (disabled)
effect_style = <effect> (enabled)
"""




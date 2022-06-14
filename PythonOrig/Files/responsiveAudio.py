import math
import numpy as np
from audioBar import AudioBar


class ResponsiveAudio:
    def __init__(self, style, mode, screen_w, screen_h, without_responsive_bg=False):
        super().__init__()
        self.__style = style
        self.__mode = mode
        self.__screen_w = screen_w
        self.__screen_h = screen_h
        self.__width = None
        self.__height = None
        self.__trigger = without_responsive_bg
        self.__bars = []
        self.load_style()


    # getters
    @property
    def get_width(self):
        return self.__width

    @property
    def get_height(self):
        return self.__height

    @property
    def get_screen_w(self):
        return self.__screen_w

    @property
    def get_screen_h(self):
        return self.__screen_h

    @property
    def get_style(self):
        return self.__style

    # load style
    def load_style(self):
        match self.__style:
            case 0:
                pass
            case 1:
                # Height must be divisible by 2
                self.__width = int(self.__screen_w / 2) * 2
                # Audio bar height

                # Value = 20% of the height and must be divisible by 2
                self.__height = int((self.__screen_h * 0.2) / 2) * 2
                # Setup
                frequencies = np.arange(500, 8500, 500)
                quantity_of_bars = len(frequencies)
                # bar = 1/320 of the screen width
                bar_width = int(math.ceil(self.__screen_w / 320))

                # bar width = screen width - 1/19 of the screen divided by number of bars
                width = (self.__screen_w - self.__screen_w / 19) / quantity_of_bars
                # current anchor
                x = (self.__screen_w - width * quantity_of_bars) / 2 + width / 2

                # create bars

                if not self.__trigger:
                    for frequency in frequencies:
                        self.__bars.append(AudioBar(int(x), self.__screen_h - self.__height, frequency, (255, 255, 255), max_height=int(self.__height), width=bar_width))
                        x += width
                else:
                    for frequency in frequencies:
                        self.__bars.append(AudioBar(int(x), 0, frequency, (255, 255, 255), max_height=int(self.__height), width=bar_width))
                        x += width
            case 2:
                 # Height must be divisible by 2
                self.__width = int(self.__screen_w / 2) * 2
                # Audio bar height

                # Value = 20% of the height and must be divisible by 2
                self.__height = int((self.__screen_h * 0.2) / 2) * 2
                # Setup
                frequencies = np.arange(500, 8500, 500)
                quantity_of_bars = len(frequencies)
                # bar = 1/320 of the screen width
                bar_width = int(math.ceil(self.__screen_w / 320))

                # bar width = screen width - 1/19 of the screen divided by number of bars
                width = (self.__screen_w - self.__screen_w / 19) / quantity_of_bars
                # current anchor
                x = (self.__screen_w - width * quantity_of_bars) / 2 + width / 2

                # create bars
                if not self.__trigger:
                    for frequency in frequencies:
                        self.__bars.append(AudioBar(int(x), self.__screen_h - self.__height, frequency, (0, 0, 0), max_height=int(self.__height), width=bar_width))
                        x += width
                else:
                    for frequency in frequencies:
                        self.__bars.append(AudioBar(int(x), 0, frequency, (0, 0, 0), max_height=int(self.__height), width=bar_width))
                        x += width

            case _:
                print('Error')

    # draw
    def run(self, screen, fps, frame, audio_info):
        if self.__mode == 2:  # responsive image -> disabled
            # erase buffer content
            if self.__style == 1:
                screen.fill((0, 0, 0))
            else:
                screen.fill((255, 255, 255))

        # update and draw audio bar
        for bar in self.__bars:
            bar.update(fps, audio_info.get_decibel(frame / fps, bar.get_freq))
            bar.render(screen)

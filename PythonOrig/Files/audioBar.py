# Adapted https://medium.com/analytics-vidhya/how-to-create-a-music-visualizer-7fad401f5a69 Avi Rzayev

import pygame


# this function checks if value in between the min value and max value
def limit(min_value, max_value, value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value


# This class keeps the information about bar and update the height based on the audio decibel
class AudioBar:
    def __init__(self, x, y, frequency, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.__x = x
        self.__y = y
        self.__frequency = frequency
        self.__color = color
        self.__width = width
        self.__min_height = min_height
        self.__max_height = max_height
        self.__height = min_height
        self.__min_decibel = min_decibel
        self.__max_decibel = max_decibel
        self.__decibel_height_ratio = (self.__max_height - self.__min_height) / (
                    self.__max_decibel - self.__min_decibel)

    # getters
    @property
    def get_freq(self):
        return self.__frequency

    # update the height
    def update(self, fps, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.__max_height
        speed = (desired_height - self.__height) / 0.1
        # updated height
        self.__height += speed * (1 / fps)
        self.__height = limit(self.__min_height, self.__max_height, self.__height)

    # draw the bar
    def render(self, screen):
        pygame.draw.rect(screen, self.__color, (self.__x, self.__y + self.__max_height/2 - self.__height/2, self.__width, self.__height), border_radius=10)

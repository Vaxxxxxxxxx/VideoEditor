import numpy as np
import pygame

# this function checks if value in between the min value and max value
def limit(min_value, max_value, value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value

# Scale image each frame
class ResponsiveImage:
    def __init__(self, style, image_path, screen_w, screen_h, min_decibel=-20, max_decibel=0):

        # Variables
        self.__style = style
        self.__image_path = image_path
        self.__screen_w = screen_w
        self.__screen_h = screen_h
        self.__width = screen_w
        self.__height = screen_h

        # Jump constraints
        self.__min_decibel = min_decibel
        self.__max_decibel = max_decibel

        # max scale of the image
        self.__jump_scale = 1.05

        # min possible height of the image
        self.__min_height = self.__screen_h
        # max possible height of the image
        self.__max_height = self.__screen_h * self.__jump_scale

        # min possible width of the image
        self.__min_width = self.__screen_w - 1
        # max possible width of the image
        self.__max_width = self.__screen_w * self.__jump_scale

        # decibel width ratio (how strongly scale with the decibel change)
        self.__decibel_width_ratio = (self.__max_width - self.__min_width) / (self.__max_decibel - self.__min_decibel)
        self.__decibel_height_ratio = (self.__max_height - self.__min_height) / (self.__max_decibel - self.__min_decibel)

        if self.__style != 0:
            self.__image = pygame.image.load(r'' + self.__image_path)
        else:
            self.__image = None


    # getters
    @property
    def get_screen_w(self):
        return self.__screen_w

    @property
    def get_screen_h(self):
        return self.__screen_h

    # Scale and draw image each frame
    def run(self, screen, fps, frame, audio_info):

        #frequencies
        frequencies = np.arange(0, 50, 1)

        max_decibel = self.__min_decibel

        # if decibel is high enough to trigger this function then remember decibel
        for f in frequencies:
            temp = audio_info.get_decibel(frame / fps, f)
            if temp > max_decibel and temp >= self.__min_decibel:
                max_decibel = temp

        # how much to move
        desired_height = max_decibel * self.__decibel_height_ratio + self.__max_height
        desired_width = max_decibel * self.__decibel_width_ratio + self.__max_width
        # how fast to move
        speed_h = (desired_height - self.__height) / 0.2
        speed_w = (desired_width - self.__width) / 0.2
        # calculate the new width and height
        self.__height += speed_h * (1 / fps)
        self.__width += speed_w * (1 / fps)
        # make sure that it is in the borders
        self.__height = limit(self.__min_height, self.__max_height, self.__height)
        self.__width = limit(self.__min_width, self.__max_width, self.__width)
        # scale
        temp_image = pygame.transform.smoothscale(self.__image, (self.__width, self.__height))
        # align center
        temp_image_rect = temp_image.get_rect(center=(self.__screen_w / 2, self.__screen_h / 2))
        # draw
        screen.blit(temp_image, temp_image_rect)


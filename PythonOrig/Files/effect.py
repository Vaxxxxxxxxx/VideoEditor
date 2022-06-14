# Path to effect styles
class Effect:
    def __init__(self, style):
        self.__effect_style = style

    # Return selected effect style
    @property
    def get_effect_path(self):
        match self.__effect_style:
            case 0:
                # effect_style = 0 (disabled)
                return None
            case 1:
                # effect_style = <1> (enabled)
                effect_path = '..\Effects\Snow.mp4'
                return effect_path
            case 2:
                # effect_style = <2> (enabled)
                effect_path = '..\Effects\Sparks.mp4'
                return effect_path
            case _:
                print('error')

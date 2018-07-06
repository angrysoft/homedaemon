class RGB:
    def __init__(self):
        self._red = 0
        self._green = 0
        self._blue = 0
        self._dimmer = 255

    def setRgb(self, arg):
        col = arg.split('.')
        if len(col) >= 3:
            self.red = col[0]
            self.green = col[1]
            self.blue = col[2]
        if len(col) == 4:
            self.dimmer = col[3]

    @property
    def red(self):
        ret = self._red * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @red.setter
    def red(self, val):
        self._red = self.toInt(val)

    @property
    def green(self):
        ret = self._green * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @green.setter
    def green(self, val):
        self._green = self.toInt(val)

    @property
    def blue(self):
        ret = self._blue * (self._dimmer / 255)
        if ret < 0:
            return 0
        else:
            return int(ret)

    @blue.setter
    def blue(self, val):
        self._blue = self.toInt(val)

    @property
    def dimmer(self):
        return self._dimmer

    @red.setter
    def dimmer(self, val):
        self._dimmer = self.toInt(val)

    def toSend(self):
        return 'F.{}.{}.{}'.format(self.red, self.green, self.blue)

    @staticmethod
    def toInt(v):
        if not type(v) == int:
            v = int(v)
        if v < 0 or v > 255:
            v = 0
        return v

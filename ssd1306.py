import font
import spidev
import RPi.GPIO as GPIO

RST = 23
D_C = 24

SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF

SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA

SSD1306_SETVCOMDETECT = 0xDB

SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9

SSD1306_SETMULTIPLEX = 0xA8

SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10

SSD1306_SETSTARTLINE = 0x40

SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22

SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8

SSD1306_SEGREMAP = 0xA0

SSD1306_CHARGEPUMP = 0x8D

SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

class SSD1306():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RST, GPIO.OUT)
        GPIO.setup(D_C, GPIO.OUT)

        GPIO.output(RST, 1)
        GPIO.output(RST, 0)
        GPIO.output(RST, 1)

        self.spi = spidev.SpiDev()
        #ls /dev/spi*
        #  /dev/spidev0.0 /dev/spidev0.1
        self.spi.open(0, 0)

        self.sendCmd(SSD1306_DISPLAYOFF)                    # 0xAE
        self.sendCmd(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        self.sendCmd(0x80)                                  # the suggested ratio 0x80
        self.sendCmd(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.sendCmd(0x3F)
        self.sendCmd(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.sendCmd(0x0)                                   # no offset
        self.sendCmd(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.sendCmd(SSD1306_CHARGEPUMP)                    # 0x8D
        self.sendCmd(0x14)
        self.sendCmd(SSD1306_MEMORYMODE)                    # 0x20
        self.sendCmd(0x00)                                  # 0x0 act like ks0108
        self.sendCmd(SSD1306_SEGREMAP | 0x1)
        self.sendCmd(SSD1306_COMSCANDEC)
        self.sendCmd(SSD1306_SETCOMPINS)                    # 0xDA
        self.sendCmd(0x12)
        self.sendCmd(SSD1306_SETCONTRAST)                   # 0x81
        self.sendCmd(0xCF)
        self.sendCmd(SSD1306_SETPRECHARGE)                  # 0xd9
        self.sendCmd(0xF1)
        self.sendCmd(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.sendCmd(0x40)
        self.sendCmd(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.sendCmd(SSD1306_NORMALDISPLAY)                 # 0xA6

    def init(self):
        pass

    def display(self, on):
        if on:
            self.sendCmd(SSD1306_DISPLAYON)
        else:
            self.sendCmd(SSD1306_DISPLAYOFF)

    def invert(self, inv):
        if inv:
            self.sendCmd(SSD1306_INVERTDISPLAY)
        else:
            self.sendCmd(SSD1306_NORMALDISPLAY)

    def sendCmd(self, cmd):
        GPIO.output(D_C, 0)
        self.spi.xfer2([cmd])
        
    def clear(self):
        self.sendCmd(SSD1306_COLUMNADDR)
        self.sendCmd(0)
        self.sendCmd(127)
        self.sendCmd(SSD1306_PAGEADDR)
        self.sendCmd(0)
        self.sendCmd(7)

        GPIO.output(D_C, 1)
        for c in range(0, 128):
            for r in range(0, 8):
                self.spi.xfer2([0])

    def printat(self, row, col, msg):
        self.sendCmd(SSD1306_COLUMNADDR)
        self.sendCmd(1 + 6*col)
        self.sendCmd(126)
        self.sendCmd(SSD1306_PAGEADDR)
        self.sendCmd(row)
        self.sendCmd(row)

        GPIO.output(D_C, 1)
        dat = []
        for c in msg:
            f = 5*(ord(c)-32)
            dat = dat + font.font[f:f+5] + [0]
        self.spi.xfer2(dat)

    def print2at(self, row, col, msg):
        self.sendCmd(SSD1306_COLUMNADDR)
        self.sendCmd(1 + 6*col)
        self.sendCmd(6*col + 12*len(msg))
        self.sendCmd(SSD1306_PAGEADDR)
        self.sendCmd(row)
        self.sendCmd(row+1)

        GPIO.output(D_C, 1)
        dat = []
        for c in msg:
            f = 20*(ord(c)-32)
            dat = dat + font.font2[f:f+10] + [0, 0]
        for c in msg:
            f = 20*(ord(c)-32)
            dat = dat + font.font2[f+10:f+20] + [0, 0]
        self.spi.xfer2(dat)

    def close(self):
        self.spi.close()
        GPIO.cleanup()
import ssd1306
import time

lcd = ssd1306.SSD1306()

lcd.clear()
lcd.display(True)
lcd.invert(False)

#lcd.printat(1, 3, "EDM 2015")
#lcd.printat(2, 1, "Project: LCD")
#lcd.printat(3, 3, time.strftime("%H:%M:%S"))
#lcd.printat(4, 2, time.strftime("%d/%m/%Y"))

lcd.printat(0, 0, 'IP: 192.168.102.123')

lcd.print2at(2, 2, 'X: 123')
lcd.print2at(4, 2, 'Y:  34')
lcd.print2at(6, 2, 'Z: 240')

lcd.close()

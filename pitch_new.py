from microbit import *
import math

compass.calibrate()
uart.init(11520, bits=8, parity=None, stop=1)

elev_set = 0
azi_set = 0

while True:
    x = accelerometer.get_x()/1030
    y = accelerometer.get_y()/1030
    if math.sqrt(x*x+y*y) < 1:
        z = math.sqrt(1-(x*x + y*y))
        roll = math.degrees(math.pi-(math.atan2(x, z)/(math.pi*2)))
        tilt = int(math.degrees(math.atan2(y, math.sqrt(x*x + z*z))))

    needle_ist = ((15 - compass.heading()) // 30) % 12
    needle_i_im = Image.ALL_CLOCKS[needle_ist]
    height_i_im = Image("00000:00000:00000:00000:00000")
    if tilt > 9:
        height_i_im = Image("00000:00000:00000:00000:00003")
    if tilt > 18:
        height_i_im = Image("00000:00000:00000:00000:00006")
    if tilt > 27:
        height_i_im = Image("00000:00000:00000:00003:00006")
    if tilt > 36:
        height_i_im = Image("00000:00000:00000:00006:00006")
    if tilt > 45:
        height_i_im = Image("00000:00000:00003:00006:00006")
    if tilt > 54:
        height_i_im = Image("00000:00000:00006:00006:00006")
    if tilt > 63:
        height_i_im = Image("00000:00003:00006:00006:00006")
    if tilt > 72:
        height_i_im = Image("00000:00006:00006:00006:00006")
    if tilt > 81:
        height_i_im = Image("00003:00006:00006:00006:00006")
    if tilt > 88:
        height_i_im = Image("00006:00006:00006:00006:00006")
    # print(compass.heading(), tilt)
    if uart.any():
        read_com = uart.read()
        read_com = str(read_com, 'utf-8')
        if read_com[0] == 'W':
            print(compass.heading(), tilt)
        if read_com[0] == 'R':
            azi_set = int(float(read_com.split(' ')[1]))
            elev_set = int(float(read_com.split(' ')[2]))
            print(azi_set, elev_set)

    height_s_im = Image("00000:00000:00000:00000:00000")
    if elev_set > 9:
        height_s_im = Image("00000:00000:00000:00000:00009")
    if elev_set > 36:
        height_s_im = Image("00000:00000:00000:00009:00000")
    if elev_set > 54:
        height_s_im = Image("00000:00000:00009:00000:00000")
    if elev_set > 72:
        height_s_im = Image("00000:00009:00000:00000:00000")
    if elev_set > 88:
        height_s_im = Image("00009:00000:00000:00000:00000")
    needle_soll = ((15 - compass.heading() + azi_set) // 30) % 12
    needle_s_im = Image.ALL_CLOCKS[needle_soll]

    display.show(needle_i_im + height_i_im)
    sleep(200)
    display.show(needle_i_im + height_i_im + needle_s_im + height_s_im)
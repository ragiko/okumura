# coding: UTF-8

import sys
import time
import RPi.GPIO as GPIO
import pygame.mixer

alarm_on_volt = 2.0
alarm_music = "m.mp3"
play_time = 5 
play_volume = 100


# GPIOの番号の定義。
# 上記回路図では、Raspberry Pi上の特定のピンに接続するかのように説明しましたが、
# たぶんここで定義する番号と接続するGPIOの番号が合っていれば動く気がする。
spi_clk  = 11
spi_mosi = 10
spi_miso = 9
spi_ss   = 8

# RPiモジュールの設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# GPIOデバイスの設定
GPIO.setup(spi_mosi, GPIO.OUT)
GPIO.setup(spi_miso, GPIO.IN)
GPIO.setup(spi_clk,  GPIO.OUT)
GPIO.setup(spi_ss,   GPIO.OUT)


pygame.mixer.init()
pygame.mixer.music.load( alarm_music )
pygame.mixer.music.set_volume( play_volume/100 )

# pygame.mixer.music.play( -1 )

# init channels
chs = 2
mem = []
for i in range(chs):
    mem.append(-1)

reset_flag = 1
ii = 0

# 0.1秒インターバルの永久ループ
while True:
    time.sleep(0.01)

    # 8チャンネル分のループ
    for ch in range(chs):
        GPIO.output(spi_ss,   False)
        GPIO.output(spi_clk,  False)
        GPIO.output(spi_mosi, False)
        GPIO.output(spi_clk,  True)
        GPIO.output(spi_clk,  False)

        # 測定するチャンネルの指定をADコンバータに送信
        cmd = (ch | 0x18) << 3
        for i in range(5):
            if (cmd & 0x80):
                GPIO.output(spi_mosi, True)
            else:
                GPIO.output(spi_mosi, False)
            cmd <<= 1
            GPIO.output(spi_clk, True)
            GPIO.output(spi_clk, False)
        GPIO.output(spi_clk, True)
        GPIO.output(spi_clk, False)
        GPIO.output(spi_clk, True)
        GPIO.output(spi_clk, False)

        # 12ビットの測定結果をADコンバータから受信
        value = 0

        for i in range(12):
            value <<= 1
            GPIO.output(spi_clk, True)
            if (GPIO.input(spi_miso)):
                value |= 0x1
            GPIO.output(spi_clk, False)

        GPIO.output(spi_ss, True)
	print " "
	
	if mem[ch] == -1:
	    mem[ch] = value
	    continue

        # 測定結果を標準出力
       	# sys.stdout.write(str(value))

       	sys.stdout.write(str(mem[ch] - value))
        if ch > 0:
	    # pass
            sys.stdout.write(" ")
       	    # sys.stdout.write(str(mem[ch] - value))


        if (mem[ch] - value > 500):
	    sys.stdout.write(str(ii)+"\n")
	    ii += 1

            pygame.mixer.music.play( -1 )
            st = time.time()
            while st + play_time > time.time():
                time.sleep( 1 )

	    pygame.mixer.music.stop()

	    for i in range(chs):
	        mem[i] = -1

	    break	

	mem[ch] = value

    sys.stdout.write("\n")

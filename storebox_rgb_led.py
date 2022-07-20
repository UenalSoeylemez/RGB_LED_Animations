#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse
from filelock import Timeout, FileLock

from config import *
from StoreboxAnimationEnum import *
    
def startAnimation(animationType, monthlyDebitNetto=40, insuranceSum=2000):
    lock = FileLock("led_animation.lock", timeout=600)
    try:
        with lock.acquire(timeout=600):
            # Create NeoPixel object with appropriate configuration.
            print("Initialize leds")
            strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
            # Intialize the library (must be called once before other functions).
            strip.begin()

            if animationType == StoreboxAnimation.Connected:
                rainbow(strip)
            elif animationType == StoreboxAnimation.Booking:
                storeboxBookingEffect(strip, monthlyDebitNetto, insuranceSum)
            elif animationType == StoreboxAnimation.KeyResultFranchise:
                storeboxFranchiseEffect(strip)
            elif animationType == StoreboxAnimation.KeyResultTech:
                storeboxTechEffect(strip, Color(255, 0, 0))
            elif animationType == StoreboxAnimation.KeyResultMarketing:
                storeboxMarketingEffect(strip, Color(0,0,255))
            elif animationType == StoreboxAnimation.KeyResultHR:
                storeboxHREffect(strip)
            elif animationType == StoreboxAnimation.KeyResultOperation:
                storeboxOperationsEffect(strip)
            elif animationType == StoreboxAnimation.KeyResultFinance:
                storeboxFinanceEffect(strip, Color(165,255,0))
            elif animationType == StoreboxAnimation.TempratureTooHot:
                storeboxTemperatureEffectTooHot(strip)
            elif animationType == StoreboxAnimation.TempratureTooCold:
                storeboxTemperatureEffectTooCold(strip)
            elif animationType == StoreboxAnimation.Fire:
                storeboxFireEffect(strip)
            elif animationType == StoreboxAnimation.Birthday:
                storeboxBirthdayEffect(strip)
            elif animationType == StoreboxAnimation.Rapid:
                rapidEffect(strip)
            elif animationType == StoreboxAnimation.abwischen:
                abwischen(strip, Color(255,0,0))
                abwischen(strip, Color(0,255,0))
                abwischen(strip, Color(0,0,255))
                abwischen(strip, Color(255,0,255))
            elif animationType == StoreboxAnimation.anim3:
                anim3(strip)
            elif animationType == StoreboxAnimation.anim2:
                anim2(strip, Color(255, 153, 255))
                anim2(strip, Color(255, 128, 0))
                anim2(strip, Color(153, 204, 255))
            elif animationType == StoreboxAnimation.Regenbogen:
                regenbogen(strip)
                verteilung(strip)
                theaterChaseRainbow(strip)
            else:
                print('Unknwon animation type {}'.str(animationType))
            colorWipe(strip, Color(0,0,0), 10)
            print("Animation ended")

    except Timeout:
        print("Another instance of this application currently holds the lock.")
  
    
# Define functions which animate LEDs in various ways.
def storeboxTemperatureEffectTooHot(strip):
    print("Start storeboxTemperatureEffectTooHot")
    colorWipe(strip, Color(0,255,0), 50)
    for x in range(10):
        for i in range(255, 0, -1):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(0,i,0))
            strip.show()
            time.sleep(0.001)
        for i in range(255):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(0,i,0))
            strip.show()
            time.sleep(0.001)

def storeboxTemperatureEffectTooCold(strip):
    print("Start storeboxTemperatureEffectTooCold")
    colorWipe(strip, Color(0,0,255), 50)
    for x in range(10):
        for i in range(255, 0, -1):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(0,0,i))
            strip.show()
            time.sleep(0.001)
        for i in range(255):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(0,0,i))
            strip.show()
            time.sleep(0.001)

def storeboxBookingEffect(strip, monthlyDebitNetto, insuranceSum=2000):
    print("Start storeboxBookingEffect")
    insurance_leds = int(insuranceSum / 1000)
    if monthlyDebitNetto + insurance_leds > LED_COUNT:
        monthlyDebitNetto = LED_COUNT
    for i in range(int(monthlyDebitNetto)):
        strip.setPixelColor(i, Color(255,0,0))
        strip.show()
        time.sleep(1)
    for i in range(int(insurance_leds)):
        strip.setPixelColor(i + monthlyDebitNetto, Color(255,255,0))
        strip.show()
        time.sleep(3)        
    time.sleep(monthlyDebitNetto * 2)

def storeboxFranchiseEffect(strip):
    print("Start storeboxFranchiseEffect")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255,255,0))
        strip.show()
        time.sleep(0.01)
    for x in range(25):
        for i in range(255, 0, -1):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(i,i,0))
            strip.show()
            time.sleep(0.001)
        for i in range(255):
            for j in range(strip.numPixels()):
                strip.setPixelColor(j, Color(i,i,0))
            strip.show()
            time.sleep(0.001)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    print("Start colorWipe")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def storeboxMarketingEffect(strip, color, wait_ms=10):
    print("Start storeboxMarketingEffect")
    for j in range(7):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(1/10)

def storeboxHREffect(strip):
    print("Start storeboxHREffect")
    for i in range(strip.numPixels(), 1, -1):
        strip.setPixelColor(i, Color(0,255,127))
        strip.show()
        time.sleep(0.4)
    for i in range(strip.numPixels(), 1, -1):
        strip.setPixelColor(i, Color(0,0,0))
        strip.setPixelColor(i + 1, Color(0,255,127))
        strip.show()
        time.sleep(0.001)

def storeboxFinanceEffect(strip, color):
    print("Start storeboxFinanceEffect")
    for i in range(strip.numPixels(), 1, -1):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.05)
    for j in range(3):
        for i in range(strip.numPixels(), 1, -1):
            strip.setPixelColor(i, Color(0,0,0))
            strip.setPixelColor(i + 1, color)
            strip.show()
            time.sleep(0.03)

def storeboxOperationsEffect(strip):
    print("Start storeboxOperationsEffect")
    for j in range(3):
        for i in range(1, strip.numPixels(), 5):
            strip.setPixelColor(i, Color(190,190,190))
            strip.setPixelColor(i + 1, Color(190,190,190))
            strip.setPixelColor(i + 2, Color(190,190,190))
            strip.setPixelColor(i + 3, Color(190,190,190))
            strip.setPixelColor(i + 4, Color(190,190,190))
            strip.show()
            time.sleep(1)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0,0,0))
        strip.show()
        time.sleep(2)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    print("Start theaterChase")
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def storeboxTechEffect(strip, color, wait_ms=50, iterations=200):
    print("Start storeboxTechEffect")
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def storeboxFireEffect(strip, wait_ms=60, iterations=200):
    print("Start storeboxFireEffect")
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, Color(0,255,0))
                strip.setPixelColor(i+q+1, Color(35,240,0))
                strip.setPixelColor(i+q+2, Color(100,255,0))
            strip.show()
            time.sleep(wait_ms/1000.0)

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    print("Start rainbow")
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    print("Start rainbowCycle")
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    print("Start theaterChaseRainbow")
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def storeboxBirthdayEffect(strip, wait_ms=50):
    print("Start storeboxBirthdayEffect")
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def rapidEffect(strip):
    print("Start rapidEffect")
    for i in range(0, strip.numPixels()):
        if i <= strip.numPixels() / 2:
            strip.setPixelColor(i, Color(230,0,8))
        else:
            strip.setPixelColor(i, Color(255,255,255))
    strip.show()
    time.sleep(30)


    'Ünals Animationen:'

#animation1
def abwischen(strip, color, wait_ms=5.1):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

#animation2 
def anim2(strip, color, wait_ms=0.1, iterations=10):
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)

#animation3
def anim3(strip, wait_ms=1, iterations=10):
    position = 0 
    for i in range(strip.numPixels()*2):
        position = position + 1
        for j in range(strip.numPixels()):
            strip.setPixelColor(j, Color(round(((math.sin(j+position)*127+128)/255)*255), round(((math.sin(j+position)*127+128)/255)*100), round(((math.sin(j+position)*127 + 128)/255)*100)))
        strip.show()
        time.sleep(wait_ms/500.0)

def wechseln(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else: 
        pos -= 170
        return Color(0, pos*3, 255 - pos * 3)

def regenbogen(strip, wait_ms=1, iterations=1):
    for j in range(256*iterations):
        for i in range(strip.numPixels()): 
            strip.setPixelColor(i, wechsln((i+j)& 255))
        strip.show()
    
def verteilung(strip, wait_ms=1, iterations=5):
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wechseln((int(i*256 / strip.numPixels()) + j ) & 255))
        strip.show()
        time.sleep(wait_ms/500.0)

def theaterChaseRainbow(strip, wait_ms=0.5):
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wechseln((i+j) % 2255))
            strip.show()
            time.sleep(wait_ms/10.0)
            for i in range(0, strip.numPixels(), 3): 
                strip.setPixelColor(i+q, 0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:

            anim3(strip)
            print('anim2')
            anim2(strip, Color(255, 153, 255))
            anim2(strip, Color(255, 128, 0))
            anim2(strip, Color(153, 204, 255))
            print('Abwischen.')
            abwischen(strip, Color(255, 0, 0))
            abwischen(strip, Color(0, 255, 0))
            abwischen(strip, Color(0, 0, 255))
            abwischen(strip, Color(255,0, 255))
            print('Regenbogen')
            regenbogen(strip)
            verteilung(strip)
            theaterChaseRainbow(strip)
            #print ('Storebox booking effect')
            #storeboxBookingEffect(strip, 42, 5000)
            #print ('Storebox franchise effect')
            #storeboxFranchiseEffect(strip)
            #print ('Storebox temprature (tooHot) effect')
            #storeboxTemperatureEffectTooHot(strip)
            #print ('Storebox temprature (tooCold) effect')
            #storeboxTemperatureEffectTooCold(strip)
            #print ('Storebox fire effect')
            #storeboxFireEffect(strip)  
            print ('Storebox tech effect')
            storeboxTechEffect(strip, Color(255, 0, 0))
            #print ('Storebox birthday effect')
            #storeboxBirthdayEffect(strip)
            #print ('Storebox marketing effect')
            #storeboxMarketingEffect(strip, Color(0,0,255))
            #print ('Storebox HR effect')
            #storeboxHREffect(strip)
            #print ('Storebox operations effect')
            #storeboxOperationsEffect(strip)
            #print ('Storebox finance effect')
            #storeboxFinanceEffect(strip, Color(165,255,0))
            
            #print ('Rapid vienna effect')
            #rapidEffect(strip)  

            #theaterChase(strip, Color(255, 0, 0))  # White theater chase
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(255, 0, 0), 100)  # Green wipe
#           print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase

            #print ('Rainbow animations.')
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

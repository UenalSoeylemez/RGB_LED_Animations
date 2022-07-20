#!/usr/bin/python3

RGB_STRIP_AVAILABLE = True
CLIENT_ID = 'LOCAL_RASPBERRY_RGB'  # Thing name in AWS IoT

ENDPOINT = 'a2i7ywvwltxze1-ats.iot.eu-central-1.amazonaws.com'
CERT_FILEPATH = '/usr/local/lib/storebox-rgb-led/certificates/certificate.pem.crt'
PRIVATE_KEY_FILEPATH = '/usr/local/lib/storebox-rgb-led/certificates/private.pem.key'
CA_FILEPATH = '/usr/local/lib/storebox-rgb-led/certificates/AmazonRootCA1.pem'

# CA_FILEPATH = 'certificates/AmazonRootCA1.pem'
AWS_REGION = 'eu-central-1'

# LED strip configuration:
LED_COUNT      = 239      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

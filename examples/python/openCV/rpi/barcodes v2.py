#!/usr/bin/python3

import cv2
from pyzbar.pyzbar import decode
from gpiozero import LED
from time import sleep

red = LED(4)
green = LED(17)

red.off()
green.off()

from picamera2 import MappedArray, Picamera2, Preview

color_valid = (0, 255, 0)
color_error = (255, 0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

barcodes = []

barcode_string_list = []

# array für alle barcodes
valid_bottle_list = {
    "4019424051983": "apfelschorle",
    "4019424051822": "wasser",
}


def draw_info(barcode, m):
    barcode_string = barcode.data.decode("utf-8")
    bottle_type = valid_bottle_list.get(barcode_string)

    if barcode_string not in barcode_string_list:
        barcode_string_list.append(barcode_string)
        print(bottle_type)

    # calculate positions of label
    x = min([p.x for p in barcode.polygon])
    y = min([p.y for p in barcode.polygon]) - 10

    show_text = f"'{barcode_string}' -> {bottle_type}"
    if bottle_type:
        text_color = color_valid
        red.off()
        green.on()
    else:
        text_color = color_error
        red.on()
        green.off()
    cv2.putText(m.array, show_text, (x, y), font, scale, text_color, thickness)
    
        


def draw_barcodes(request):
    with MappedArray(request, "main") as m:
        if len(barcodes) == 0:
            global barcode_string_list
            barcode_string_list = []
            red.off()
            green.off()
        else:
            for b in barcodes:
                if b.polygon:
                    draw_info(b, m)
        


# setup camera
picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)
config = picam2.create_preview_configuration(main={"size": (1280, 960)})
picam2.configure(config)

picam2.post_callback = draw_barcodes
picam2.start()

while True:
    rgb = picam2.capture_array("main")
    barcodes = decode(rgb)

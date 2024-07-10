#!/usr/bin/python3

import cv2
from pyzbar.pyzbar import decode

from picamera2 import MappedArray, Picamera2, Preview

color_valid = (0, 255, 0)
color_error = (255, 0, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

barcodes = []

# array für alle barcodes
valid_bottle_list = {
    "4019424051983": "apfelschorle",
    "4019424051822": "wasser",
}


def handle_status_pins(bottle_type):
    print(bottle_type)

def draw_info(barcode, m):
    barcode_string = barcode.data.decode("utf-8")
    bottle_type = valid_bottle_list.get(barcode_string)

    # calculate positions of label
    x = min([p.x for p in barcode.polygon])
    y = min([p.y for p in barcode.polygon]) - 10

    show_text = "'{}' -> {}".format(barcode_string, bottle_type)
    text_color = color_error
    if bottle_type:
        text_color = color_valid
    cv2.putText(m.array, show_text, (x, y), font, scale, text_color, thickness)
    handle_status_pins(bottle_type)


def draw_barcodes(request):
    with MappedArray(request, "main") as m:
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

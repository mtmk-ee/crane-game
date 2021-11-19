"""Contains some values used all over the place.

P = value in terms of pixels
M = value in terms of meters
"""
PIXELS_PER_METER = 20
SCREEN_SIZE_P = (480, 640)
SCREEN_SIZE_M = SCREEN_SIZE_P[0] / PIXELS_PER_METER, SCREEN_SIZE_P[1] / PIXELS_PER_METER
SCREEN_CENTER_M = SCREEN_SIZE_M[0] / 2, SCREEN_SIZE_M[1] / 2

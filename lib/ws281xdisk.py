import time
from rpi_ws281x import PixelStrip, Color

import diskmapping


class PixelDisk(PixelStrip):

    def __init__(self, pin):
        print("Loading mapping config")
        disk_map = diskmapping.DiskMapping('241led9ringRGB')
        print("Initializing Strip")
        super().__init__(disk_map.pixel_count,  pin, 800000, 10, False, 255, 0)
        self.disk_map = disk_map
        self.begin()

    def set_pixel(self, n, color):
        r = self.disk_map.map_pos(n)
        self.setPixelColor(r, Color(*color))

    def set_pixels(self, pixels, color):
        for pix in pixels:
            self.set_pixel(pix, color)


    def fill(self, color):
        for i in range(self.numPixels()):
            self.setPixelColor(i, Color(*color))
        self.show()

    def fill_ring(self, ring, color):
        for i in self.disk_map.get_ring(ring):
            self.set_pixel(i, color)
        self.show()

    def get_line(self, angle, full = False):
        pixels = []
        for r in self.disk_map.get_ring_list():
            if full: #Line extends across the disk.
                pixels.append(self.disk_map.get_pixel_at_angle(r, self.adjust_angle(angle, 180)))
            pixels.append(self.disk_map.get_pixel_at_angle(r, angle))
        return pixels


    # def fade(self, color, os=.2):
    #     c1 = int(color[0] * os)
    #     c2 = int(color[1] * os)
    #     c3 = int(color[2] * os)
    #
    #     c = (c1,c2,c3)
    #
    #     return c


    def adjust_angle(self, angle, n):
        adj = angle + n
        if adj < 0:
            adj += 360
        return adj % 360


    def get_chain(self, ring, angle, size, adj=0): #Select 1 or more pixels in a row along a single ring

        if size % 2 == 0:
            l_tails = (size/2)
            r_tails = (size/2) - 1
        else:
            l_tails = (size - 1)/2
            r_tails = (size - 1)/2
        if adj:  #For Gyro adjustment
            angle = self.adjust_angle(angle, adj)

        center = self.disk_map.get_pixel_at_angle(ring,  angle)

        l = [self.disk_map.traverse_ring(ring, center, (0-i)) for i in range (int(l_tails) + 1)]
        r = [self.disk_map.traverse_ring(ring, center, i) for i in range (int(r_tails) + 1)]

        pix = l + [center] + r
        return pix

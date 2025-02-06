import time
import os
import json
from rpi_ws281x import PixelStrip, Color

class PixelDisk(PixelStrip):

    def __init__(self, pin, brightness, invert, channel):
        print("Loading mapping config")
        disk_map = DiskMapping('241led9ringRGB')
        print("Initializing Strip")
        super().__init__(disk_map.pixel_count, pin, disk_map.freq_hz, disk_map.dma, invert, brightness, channel)
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



class DiskMapping:
    def __init__(self, device='241led9ringRGB'):

        script_dir = os.path.dirname(__file__)
        config_file_path = os.path.join(script_dir, 'devicemaps/{}.json'.format(device))


        with open(config_file_path) as config_file:
            device_conf = json.load(config_file)

        self.device = device

        self.pixel_count = device_conf['pixel_count']
        self.freq_hz = device_conf['freq_hz']
        self.dma = device_conf['dma']

        self.ring_count = device_conf['ring_count']
        self.ring_map = self.map_rings(device_conf['ring_sizes'])
        self.direction = device_conf['pixel_direction']

    def get_ring(self, ring_id):
        return self.ring_map[ring_id]

    def get_ring_list(self):
        return self.ring_map.keys()

    def map_rings(self, ring_sizes):
        ring_map = {}
        ring_start = 0

        for ring_id in ring_sizes.keys():
            ring_end = ring_start + ring_sizes[ring_id]
            ring_map[ring_id] = list(range(ring_start, ring_end))
            ring_start = ring_end

        if self.pixel_count != ring_start:
            print(f"pixel_count in config did not match total mapped pixels, pixel_count: {self.pixel_count}, mapped: {ring_start}")
            raise ValueError("pixel_count in config did not match total mapped pixels")
        return ring_map


    def map_pos(self, pix):
        if str(self.direction) == "1":
            return (self.pixel_count - 1) - pix
        else:
            return pix

    def get_pixel_at_angle(self, ring, angle):
        angle = 360 - angle
        ratio = angle/360
        pixels = self.get_ring(ring)
        pix_index = int((len(pixels) - 1) * ratio)  #Which pixel on the ring has this angle?
        return pixels[pix_index]

    def traverse_ring(self, ring, start, n):
        pixels = self.get_ring(ring)
        ring_size = len(pixels)
        n = n % ring_size
        pos = pixels.index(start)
        new_pos = pos + n
        if new_pos < 0:
            new_pos = ring_size + new_pos
        elif new_pos >= ring_size:
            new_pos = new_pos - ring_size
        return pixels[new_pos]


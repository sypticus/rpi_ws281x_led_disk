import json
import os

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './output03.txt')


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

    def show(self):
        self.show()


    def map_pos(self, pix):
        if str(self.direction) == "1":
            return (self.pixel_count - 1) - pix
        else:
            return pix

    @property
    def __class__(self):
        return super().__class__

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


#
# def get_rings_map():
#     ring_map = {}
#     for x in ring_sizes.keys():
#         ring_map[x] = get_ring_pixels(x)
#     return ring_map
#
# def get_flat_map():
#     flat_map = list(range(0, get_wheel_size()))
#     return flat_map
#
# def get_angle(ring, angle):
#     rad = angle/360
#     rings = get_ring_pixels(ring)
#     pix_index = int((len(rings) - 1) * rad)  #Which pixel on the ring has this angle?
#     pc = rings[pix_index]
#     return pc
#

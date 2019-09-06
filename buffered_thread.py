import threading
import numpy as np
import time
import os
from PIL import Image

class Data(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.data = []
        self.lock = threading.Lock()

    def run(self):
        while len(self.data) < 100:
            self.data.append(np.random.randint(0, 100))
            time.sleep(0.1)

    def sample(self):
        while len(self.data) < 10:
            time.sleep(1)

        self.lock.acquire()
        print('length of data before sample: {}'.format(len(self.data)))
        r = self.data[:10]
        self.data = self.data[10:]
        print('length of data after sample: {}'.format(len(self.data)))
        self.lock.release()

        time.sleep(1)
        print('length of data after releases: {}'.format(len(self.data)))
        return r


d = Data()
d.start()
print(d.sample())
print(d.sample())


# A real world application
class Data(threading.Thread):

    def __init__(self, data_paths, max_buff_len=3000, batch_size=300):
        threading.Thread.__init__(self)
        self.data = []
        self.lock = threading.Lock()
        self.paths = data_paths
        self.N = 0
        self.max_buff_len = max_buff_len
        self.batch_size = batch_size

    def run(self):
        for p in self.paths:
            while len(self.data) > self.max_buff_len:
                time.sleep(1)
            imgs = [os.path.join(p, _) for _ in os.listdir(p)]
            imgs = [np.array(Image.open(_)) for _ in imgs]
            self.data += imgs
            print('current data size is {}'.format(len(self.data)))
            self.N += 1

    def sample(self):
        while len(self.data) < self.batch_size:
            if self.N == len(self.paths):
                break
            time.sleep(0.1)

        self.lock.acquire()
        r = self.data[:self.batch_size]
        self.data = self.data[self.batch_size:]
        self.lock.release()

        return np.array(r).astype(np.uint8)

import random
from time import sleep
import math

class randomnumbers():
    def __init__(self, snref):
        self.sn = snref
        self.run()

    def run(self):
        ct = 0
        while True:
            ct = ct + 0.1
            for key in self.sn.names_dict.keys():
                if key == "sin":
                    self.sn.set_name(key,round((math.sin(ct)),3))
                elif key == "cos":
                    self.sn.set_name(key,round((math.cos(ct)),3))
                elif key == "beans":
                    self.sn.set_name(key,round(random.random(),3))
                elif key == "cats":
                    self.sn.set_name(key,round(random.random(),3))
                elif key == "hello":
                    self.sn.set_name(key,round(random.random(),3))

            sleep(0.1)



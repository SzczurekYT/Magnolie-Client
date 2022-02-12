from threading import Thread
from time import sleep
import os

class LoadAnim(Thread):

    def run(self):
        self.anim = True
        i = 0
        anim = [".", "..", "..."]
        while self.anim:
            print(anim[i], end="\r")
            i += 1
            if i == 3:
                i = 0
            sleep(0.5)

    def stopAnim(self):
        self.anim = False

    


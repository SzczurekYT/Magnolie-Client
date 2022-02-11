from threading import Thread
from time import sleep

class LoadAnim(Thread):
    def __init__(self) -> None:
        self.anim = True

    def run(self) -> None:

        i = 0
        anim = [".", "..", "..."]
        while self.anim:
            print(anim[i], end="\r")
            i += 1
            if i == 3:
                i = 0
            sleep(0.1)

    def stopAnim(self):
        self.anim = False
    


from cbpi.craftbeerpi import CraftBeerPi
import os

if __name__ == '__main__':
    if os.path.exists(os.path.join(".", "config", "config.yaml")) is False:
        print("***************************************************")
        print("CraftBeerPi Config File not found: %s" % os.path.join(".", "config", "config.yaml"))
        print("Please run 'cbpi setup' before starting the server ")
        print("***************************************************")
    else:
        with open("test.txt", 'w') as f:
            f.write("I ran and the curDir is: " + os.path.realpath(os.curdir))
        print("START")
        cbpi = CraftBeerPi()
        cbpi.start()

import driver.portController as portController
import game.game as gameCtrl

portCtrl = portController.PortsController()
gameInstance = gameCtrl.Instance()

def setup():
    portCtrl.addControllers("cfg/master.json")
    gameInstance.
    print(1)


if __name__ == "__main__":
    setup()
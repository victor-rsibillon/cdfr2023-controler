import pygame
import pygame_gui
import ui.infoPane

FRAME_TITLE = 'CDFR 2023 - Grenoble INP Phelma Robotronik'
FRAME_RATE = 60
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080

TABLE_WIDTH = 1463
TABLE_HEIGHT = 1080

PANE_X_OFFSET = FRAME_WIDTH - TABLE_WIDTH


class Instance:

    def __init__(self):
        self.manager = pygame_gui.UIManager((TABLE_WIDTH, TABLE_HEIGHT))
        self.window_surface = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.UIListenerClass = {}
        self.infoPane = None
        self.isRunning = True
        self.window_surface = None

    def runModel(self):
        self.infoPane =
        while self.isRunning:
            self.frameHandler()

    def setupPyGame(self):
        pygame.init()
        pygame.display.set_caption(FRAME_TITLE)
        self.addGraphicalElement()


    def addGraphicalElement(self):
        self.UIListenerClass["start"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, PANE_X_OFFSET), (100, 50)), text='Start', manager=self.manager)
        self.UIListenerClass["pause"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, PANE_X_OFFSET + 100), (100, 50)), text='Pause', manager=self.manager)
        self.UIListenerClass["stop"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, PANE_X_OFFSET + 200), (100, 50)), text='Stop', manager=self.manager)
        self.UIListenerClass["reset"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, PANE_X_OFFSET + 300), (100, 50)), text='Reset', manager=self.manager)


    def frameHandler(self):
        time_delta = self.clock.tick(FRAME_RATE) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.UIListenerClass["start"]:
                        print("start pressed")

                    if event.ui_element == self.UIListenerClass["pause"]:
                        print("pause pressed")

                    if event.ui_element == self.UIListenerClass["stop"]:
                        print("stop pressed")

                    if event.ui_element == self.UIListenerClass["reset"]:
                        print("reset pressed")

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                print(f"Mouse@({mouse_pos[0]}, {mouse_pos[1]})")

            if event.type == pygame.QUIT:
                self.isRunning = False

            self.manager.process_events(event)

        self.manager.update(time_delta)
        self.window_surface.blit(pygame.image.load("assets/img/table_2023.png"), (0, 0))
        self.manager.draw_ui(self.window_surface)

        pygame.display.update()


    def setInfoPane(self, pane):
        self.infoPane = pane


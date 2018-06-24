import pygame
import numpy as np
# import time
pygame.init()


class Radar(object):
    def __init__(self):
        self.angle = 0
        self.distances = [0]*360
        self.color_GREEN = (0, 255, 0)
        self.color_RED = (255, 0, 0)
        self.display_width = 800
        self.display_height = 800
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("PiRadar")
        self.clock = pygame.time.Clock()

    def draw_radar(self):
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width/2), int(self.display_height/2)), 400, 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), 300, 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), 200, 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), 100, 1)
        pygame.draw.line(self.gameDisplay, self.color_GREEN, (0, int(self.display_height/2)), (int(self.display_width), int(self.display_height/2)))
        pygame.draw.line(self.gameDisplay, self.color_GREEN, (int(self.display_width/2), 0), (int(self.display_width/2), int(self.display_height)))

    def needle(self, angle, distance):
        x = (self.display_width/2)+2*distance*np.cos(np.deg2rad(angle))
        y = (self.display_height/2) - 2 * distance * np.sin(np.deg2rad(angle))
        pygame.draw.line(self.gameDisplay, self.color_RED, (int(self.display_width / 2), int(self.display_height / 2)), (x, y))

    def draw_points(self, pts):
        for pnt in range(len(pts)):
            x = (self.display_width / 2) + 2 * pts[pnt] * np.cos(np.deg2rad(pnt))
            y = (self.display_height / 2) - 2 * pts[pnt] * np.sin(np.deg2rad(pnt))
            pygame.draw.circle(self.gameDisplay, (255, 0, 0), (int(x), int(y)), 2)

    def loop(self):
        # for i in range(0, 360):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                try:
                    GPIO.cleanup()
                except NameError:
                    pass
                pygame.quit()
                exit()
        # self.clock.tick(60)
        # self.distances[i] = 200 * np.sin(a*np.deg2rad(i)/2)
        self.gameDisplay.fill((0, 0, 0))
        self.draw_radar()
        self.draw_points(self.distances)
        self.needle(self.angle, distance=self.distances[self.angle])

        pygame.display.update()

    def update(self, angle, dist):
        self.angle = angle
        self.distances[angle] = dist


d = 0

if __name__ == '__main__':
    radar = Radar()
    while True:
        d += 1
        for i in range(360):
            radar.update(i, 200*np.sin(d*np.deg2rad(i)))
            print(radar.angle, radar.distances[i])
            radar.loop()

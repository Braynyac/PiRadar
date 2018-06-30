import pygame
import numpy as np
# import time
pygame.init()


class Radar(object):
    def __init__(self, stSz):
        self.angle = 0
        self.deg_step = stSz
        self.distances = [0]*360
        self.points = [0] * 360
        self.color_GREEN = (0, 255, 0)
        self.color_RED = (255, 0, 0)
        self.display_width = 800
        self.display_height = 800
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("PiRadar")
        self.draw_radar()
        #self.clock = pygame.time.Clock()

    def draw_radar(self):
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width/2), int(self.display_height/2)), int(self.display_height/2), 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), int(self.display_height*0.375), 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), int(self.display_height/4), 1)
        pygame.draw.circle(self.gameDisplay, self.color_GREEN, (int(self.display_width / 2), int(self.display_height / 2)), int(self.display_height/8), 1)
        pygame.draw.line(self.gameDisplay, self.color_GREEN, (0, int(self.display_height/2)), (int(self.display_width), int(self.display_height/2)))
        pygame.draw.line(self.gameDisplay, self.color_GREEN, (int(self.display_width/2), 0), (int(self.display_width/2), int(self.display_height)))

        font = pygame.font.SysFont("comicsansms", 18)
        measurements = [font.render("0 cm", True, (0, 255, 0)),
                        font.render("50 cm", True, (0, 255, 0)),
                        font.render("100 cm", True, (0, 255, 0)),
                        font.render("150 cm", True, (0, 255, 0)),
                        font.render("200 cm", True, (0, 255, 0))]
        for i in range(len(measurements)):
            self.gameDisplay.blit(measurements[i], (self.display_width/2 - measurements[i].get_width() + i*self.display_height/8, self.display_height/2))

    def needle(self, angle, distance):
        x = (self.display_width/2)+2*distance*np.cos(np.deg2rad(angle))
        y = (self.display_height/2) - 2 * distance * np.sin(np.deg2rad(angle))
        pygame.draw.line(self.gameDisplay, self.color_RED, (int(self.display_width / 2), int(self.display_height / 2)), (x, y))

    def draw_points(self, pts):
        for pnt in range(len(pts)):
            x = (self.display_width / 2) + 2 * pts[pnt] * np.cos(np.deg2rad(pnt))
            y = (self.display_height / 2) - 2 * pts[pnt] * np.sin(np.deg2rad(pnt))
            self.points[pnt] = [x, y]
            pygame.draw.circle(self.gameDisplay, (255, 0, 0), (int(x), int(y)), 2)

    def connect_pts(self, pts):
        for pnt in range(int(len(pts)/self.deg_step-self.deg_step)):
            pygame.draw.line(self.gameDisplay, (255, 0, 0), (pts[pnt*self.deg_step][0], pts[pnt*self.deg_step][1]), (pts[pnt*self.deg_step+self.deg_step][0], pts[pnt*self.deg_step+self.deg_step][1]))

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

        self.gameDisplay.fill((0, 0, 0))
        self.draw_radar()
        self.draw_points(self.distances)
        self.connect_pts(self.points)
        self.needle(self.angle, distance=self.distances[self.angle])

        pygame.display.update()

    def update(self, angle, dist):
        self.angle = angle
        self.distances[angle] = dist


d = 0

if __name__ == '__main__':
    radar = Radar(7)
    while True:
        d += 1
        for i in range(int(360/radar.deg_step)):
            radar.update(i*radar.deg_step, 200*np.sin(d*np.deg2rad(i*radar.deg_step)))
            radar.loop()

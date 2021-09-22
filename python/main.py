import pyglet
import random


class Window(pyglet.window.Window):
    def __init__(self, width, height, box_width, box_height, dt, particle_num):
        super().__init__(width, height)
        self.particle_num = particle_num
        self.box_height = box_height
        self.box_width = box_width
        self.height = height
        self.width = width
        self.time_step = dt
        self.particles = []
        self.generate_particles(self.particle_num)
        pyglet.clock.schedule_interval(self.update, self.time_step)
        self.start = False

    def on_draw(self):
        self.clear()
        for i in self.particles:
            i.part_draw()

    def update(self, time_step):
        for idx, i in enumerate(self.particles):
            flag = False
            for jdx, j in enumerate(self.particles[idx+1:self.particle_num]):
                if not flag:
                    overlap, direction = self.doOverlap(i, j)
                    if overlap:
                        if direction == 0:
                            i.velx *= -1
                            j.velx *= -1
                        elif direction == 1:
                            i.vely *= -1
                            j.vely *= -1
                        elif direction == 2:
                            i.velx *= -1
                            i.vely *= -1
                            j.velx *= -1
                            j.vely *= -1

            if i.posx + i.velx <= 0 or i.posx + i.width + i.velx >= i.window_w:
                i.velx *= -1
            if i.posy + i.vely <= 0 or i.posy + i.height + i.vely >= i.window_h:
                i.vely *= -1

            #         if not (i.posx == self.posx and i.posy == self.posy):
            #             if self.doOverlap()
            #                 self.velx *= -1
            # flag = False
            # for i in particles:
            #     if not flag:
            #         if not (i.posx == self.posx and i.posy == self.posy):
            #             if self.doOverlap()
            #                 self.velx *= -1
            # if self.posx + self.velx <= 0 or self.posx + self.width + self.velx >= self.window_w:
            #     self.velx *= -1
            # if self.posy + self.vely <= 0 or self.posy + self.height + self.vely >= self.window_h:
            #     self.vely *= -1
            i.part_update(self.particles)

    def generate_particles(self, num):
        for i in range(num):
            size = random.randint(10, 20)
            posx = random.randint(0, self.width - size)
            posy = random.randint(0, self.width - size)
            vx = random.randint(-5, 5)
            vy = random.randint(-5, 5)
            self.particles.append(Particle(posx, posy, vx, vy, size, size, self.width, self.height))

    def doOverlap(self, part1, part2):
        overlap = True
        direction = -1
        if part1.posx >= part2.posx + part2.width or part2.posx >= part1.posx + part1.width:
            overlap = False
        else:
            direction += 1
        if part1.posy >= part2.posy + part2.height or part2.posy >= part1.posy + part1.height:
            overlap = False
        else:
            direction += 2

        return overlap, direction


    # def on_draw(self):
    #     self.clear()
    #     for i in range(self.width // self.box_width):
    #         for j in range(self.height // self.box_height):
    #             if random.random() < 0.4:
    #                 print((i,j))
    #                 print((i * self.box_width, j * self.box_height, i * self.box_width + self.box_width, j * self.box_height + self.box_height))
    #                 self.draw_square(i * self.box_width, j * self.box_height, i * self.box_width + self.box_width, j * self.box_height + self.box_height)
    #
    # def draw_square(self, x1, y1, x2, y2):
    #     pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 1, 2, 3],
    #                                  ('v2i', (x1, y1,
    #                                           x1, y2,
    #                                           x2, y1,
    #                                           x2, y2)))


class Particle:

    def __init__(self, posx, posy, velx, vely, width, height, window_w, window_h):
        self.height = height
        self.width = width
        self.window_h = window_h
        self.window_w = window_w
        self.posx = posx
        self.posy = posy
        self.velx = velx
        self.vely = vely

    def part_update(self, particles):
        self.posx += self.velx
        self.posy += self.vely

    def part_draw(self):
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES, [0, 1, 2, 1, 2, 3],
                                     ('v2i', (self.posx, self.posy,
                                              self.posx, self.posy + self.height,
                                              self.posx + self.width, self.posy,
                                              self.posx + self.width, self.posy + self.height)))



def main_func():
    window = Window(600, 600, 10, 10, 1.0 / 60.0, 25)
    pyglet.app.run()


if __name__ == '__main__':
    main_func()

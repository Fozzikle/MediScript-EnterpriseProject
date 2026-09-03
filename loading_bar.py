from manim import *
import os

config.media_dir = os.path.expanduser(r"C:\Users\mathi\OneDrive\Desktop\temp test")

# Setting video quality
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30

config.background_color = BLACK


class Loading_Intro(Scene):
    def construct(self):
        # making objects
        c1 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)
        c2 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)
        c3 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)

        # starting position
        c1.move_to(UP * 3)
        c2.move_to(DOWN * 2 + LEFT * 4)
        c3.move_to(DOWN * 2 + RIGHT * 4)

        # adding them to environment
        self.add(c1, c2, c3)

        # first position 
        c1_p1 = LEFT * 1.5 + DOWN * 1
        c2_p1 = RIGHT * 1.5 + UP * 2
        c3_p1 = RIGHT * 1.5 + DOWN * 1

        # p1 animation
        self.play(
            c1.animate.move_to(c1_p1),
            c2.animate.move_to(c2_p1),
            c3.animate.move_to(c3_p1)
        )


class Loading_Loop(Scene):
    def construct(self):
        # making objects
        c1 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)
        c2 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)
        c3 = Circle(radius=1, color=PINK, fill_opacity=1, sheen_factor=0.5, stroke_width=2, stroke_color=LIGHT_PINK)

        # first position
        c1_p1 = LEFT * 1.5 + DOWN * 1
        c2_p1 = RIGHT * 1.5 + UP * 2
        c3_p1 = RIGHT * 1.5 + DOWN * 1

        # second position
        c1_p2 = RIGHT * 1.5 + DOWN * 1
        c2_p2 = LEFT * 1.5 + DOWN * 1
        c3_p2 = LEFT * 1.5 + UP * 2

        # third position
        c1_p3 = LEFT * 1.5 + UP * 2
        c2_p3 = RIGHT * 1.5 + UP * 2
        c3_p3 = LEFT * 1.5 + DOWN * 1

        # fourth position
        c1_p4 = RIGHT * 1.5 + DOWN * 1
        c2_p4 = LEFT * 1.5 + UP * 2
        c3_p4 = RIGHT * 1.5 + UP * 2

        # fifth position
        c1_p5 = RIGHT * 1.5 + UP * 2
        c2_p5 = RIGHT * 1.5 + DOWN * 1
        c3_p5 = LEFT * 1.5 + DOWN * 1

        # starting position
        c1.move_to(c1_p1)
        c2.move_to(c2_p1)
        c3.move_to(c3_p1)

        # adding them to environment
        self.add(c1, c2, c3)

        # p1 animation
        self.play(
            c1.animate.move_to(c1_p2),
            c2.animate.move_to(c2_p2),
            c3.animate.move_to(c3_p2),
        )
        self.wait(0.25)

        steps = [
            (c1_p3, c2_p3, c3_p3),
            (c1_p4, c2_p4, c3_p4),
            (c1_p5, c2_p5, c3_p5),
            (c1_p1, c2_p1, c3_p1)
        ]

        for _ in range(2):
            for c1_pos, c2_pos, c3_pos in steps:
                self.play(
                    c1.animate.move_to(c1_pos),
                    c2.animate.move_to(c2_pos),
                    c3.animate.move_to(c3_pos)
                )
                self.wait(0.25)

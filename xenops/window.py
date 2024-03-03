from typing import cast
import random

from xenops.event import ClickEvent, PointerMotionEvent, ScrollEvent
from .widget import Widget, Root
import pygame

class Window:
    def __init__(self, title: str) -> None:
        self.title = title
        self.root: Root = Root()
        self.running = True

        self.init_pygame()

    def init_pygame(self):
        pygame.init()

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((500, 500), pygame.RESIZABLE | pygame.SRCALPHA)

        pygame.display.set_caption(self.title)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                self.handle_raw_event(event)

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        self.cleanup_pygame()

    def cleanup_pygame(self):
        pygame.quit()

    def draw(self):
        self.screen.fill((0, 0, 0, 1))

        def draw_widget(widget: Widget):
            gp = widget.global_position

            color = (
                id(widget)       & 0xFF,
                id(widget) >> 8  & 0xFF,
                id(widget) >> 16 & 0xFF
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect=(gp.x, gp.y, gp.w, gp.h),
                width=1            
            )

            for child in widget.children:
                draw_widget(child)

        draw_widget(self.root)

    def handle_raw_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.dict["button"] in [4, 5]:
                return

            self.root.dispatch_event(
                ClickEvent(
                    pos=event.dict["pos"],
                    button=event.dict["button"]
                )
            )
        
        elif event.type == pygame.MOUSEMOTION:
            self.root.dispatch_event(
                PointerMotionEvent(
                    pos=event.dict["pos"],
                    rel_pos=event.dict["rel"]
                )
            )
        
        elif event.type == pygame.MOUSEWHEEL:
            direction: int = -1 if event.dict["flipped"] else 1

            self.root.dispatch_event(
                ScrollEvent(
                    pos=pygame.mouse.get_pos(),
                    x=event.dict["x"] * direction,
                    y=event.dict["y"] * direction,
                    dx=event.dict["precise_x"] * direction,
                    dy=event.dict["precise_y"] * direction
                )
            )

        else:
            pass #print(event.dict)
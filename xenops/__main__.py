# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

"""Main module of xenops."""

import pygame

def main() -> None:
    pygame.init()

    running = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE | pygame.SRCALPHA)
    pygame.display.set_caption("Xenops")

    pygame.draw.rect(screen, (0, 0, 0, 0), screen.get_rect())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                print(event.dict)

        pygame.draw.rect(screen, (255, 0, 255), (20, 20, 20, 20))
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()

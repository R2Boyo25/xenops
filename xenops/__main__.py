# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

"""Main module of xenops."""


from xenops.event import Event
from xenops.window import Window


def main() -> None:
    window = Window("Xenops")

    window.root.on(Event, lambda event: print(event))

    window.run()


if __name__ == '__main__':
    main()

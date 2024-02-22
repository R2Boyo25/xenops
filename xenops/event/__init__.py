# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field


class Event:
    def __init__(self) -> None:
        self.consumed = False

    def cancel(self) -> None:
        self.consumed = True

@dataclass
class PointerEvent(Event):
    pos: tuple[int, int]

@dataclass
class PointerMotionEvent(PointerEvent):
    rel_pos: tuple[int, int]

@dataclass
class ClickEvent(PointerEvent):
    button: int

@dataclass
class KeyboardEvent(Event):
    modifiers: int
    key: int
from dataclasses import dataclass, field


@dataclass
class Event:
    consumed = field(default=False)

    def cancel(self):
        self.consumed = True

@dataclass
class PointerEvent(Event):
    pos: tuple[int, int]
    left: bool = field(default=False)
    middle: bool = field(default=False)
    right: bool = field(default=False)

@dataclass
class PointerMotionEvent(PointerEvent):
    rel_pos: tuple[int, int]

@dataclass
class KeyboardEvent(Event):
    modifiers: int
    key: int
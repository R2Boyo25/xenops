# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

from typing import Callable, cast

from .rect import Point, Rect
from ..event import Event, KeyboardEvent, PointerEvent


class Widget:
    def __init__(self) -> None:
        self.parent: "Widget | None" = None
        self.children: list["Widget"] = []
        self.event_handlers: dict[type[Event], list[Callable[[Event], None]]] = {}
        self._global_pos = Rect(25, 25, 25, 25)

    def on(self, event_type: type[Event], handler: Callable[[Event], None]) -> None:
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        self.event_handlers[event_type].append(handler)

    def remove_handler(self, handler: Callable[[Event], None]) -> None:
        for event_type in self.event_handlers.values():
            if handler in event_type:
                event_type.remove(handler)

    def add_child(self, child: "Widget") -> None:
        self.children.append(child)

        if child.parent is not None:
            child.parent.remove_child(child)

        child.parent = self

    @property
    def global_position(self) -> Rect:
        return self._global_pos

    def remove_child(self, child: "Widget") -> None:
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_root(self) -> "Root":
        target = self

        while target.parent is not None:
            target = target.parent

        return cast(Root, target)

    def _dispatch_event(self, event: Event) -> None:
        if type(event) in self.event_handlers:
            for handler in self.event_handlers[type(event)]:
                handler(event)

# Events dispatched:
#  Pointer:   trickle down to target      -> bubble up
#  Key:       trickle down to target      -> bubble up; target is self.focused
#  Otherwise: directly dispatch to target -> bubble up

class Root(Widget):
    def __init__(self) -> None:
        super().__init__()

        self.focused: Widget | None = None

    def dispatch_event(self, event: Event) -> None:
        if isinstance(event, PointerEvent):
            def handle_widget(widget: Widget) -> None:
                print(widget, widget.global_position, event.pos)
                if widget.global_position.contains_point(event.pos):
                    widget._dispatch_event(event)
                    
                    for child in widget.children:
                        handle_widget(child)

            handle_widget(self)

        elif isinstance(event, KeyboardEvent):
            self._dispatch_event(event)

            if self.focused is not None:
                path = []
                target = self.focused

                while target.parent is not None:
                    target = target.parent
                    path.append(target)

                for widget in reversed(path):
                    widget._dispatch_event(event)

                    if event.consumed:
                        return

                self.focused._dispatch_event(event)

                if event.consumed:
                    return

                for widget in path:
                    widget._dispatch_event(event)

                    if event.consumed:
                        return

        else:
            self._dispatch_event(event)
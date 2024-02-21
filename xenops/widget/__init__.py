from typing import Callable, cast

from .rect import Point, Rect
from ..event import Event, KeyboardEvent, PointerEvent


class Widget:
    def __init__(self):
        self.parent: "Widget | None" = None
        self.children: list["Widget"] = []
        self.event_handlers: dict[type[Event], list[Callable[[Event], None]]] = {}

    def on(self, event_type: type[Event], handler: Callable[[Event], None]):
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []

        self.event_handlers[event_type].append(handler)

    def remove_handler(self, handler: Callable[[Event], None]):
        for event_type in self.event_handlers.values():
            if handler in event_type:
                event_type.remove(handler)

    def add_child(self, child: "Widget"):
        self.children.append(child)

        if child.parent is not None:
            child.parent.remove_child(child)

        child.parent = self

    @property
    def global_position(self) -> Rect:
        return Rect(25, 25, 25, 25)

    def remove_child(self, child: "Widget"):
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def get_root(self) -> "Root":
        target = self

        while target.parent is not None:
            target = target.parent

        return cast(Root, target)

    def _dispatch_event(self, event: Event):
        if type(event) in self.event_handlers:
            for handler in self.event_handlers[type(event)]:
                handler(event)

    def _propagate_event(self, event: Event):
        self.on_event_down(event)

        if event.consumed:
            return

        for child in self.children:
            # if inside bounds
            if True:
                child._propagate_event(event)

            if event.consumed:
                return

        self.on_event_up(event)

    def on_event_down(self, event: Event):
        pass

    def on_event_up(self, event: Event):
        pass

# Events dispatched:
#  Pointer: trickle down to target, then bubbled up
#  Key: also trickle down to target, then bubbled up; target is self.focused
#  Otherwise: direct then bubble up

class Root(Widget):
    def __init__(self):
        super().__init__()

        self.focused: Widget | None = None

    def dispatch_event(self, event: Event):
        if event is PointerEvent:
            def handle_widget(widget: Widget):
                if widget.global_position.contains_point(cast(PointerEvent, event).pos):
                    for child in widget.children:
                        handle_widget(child)

            handle_widget(self)

        elif event is KeyboardEvent:
            self._dispatch_event(event)

            if self.focused is not None:
                path = []
                target = self.focused

                while target.parent is not None:
                    target = target.parent
                    path.append(target)

                for widget in reversed(path):
                    widget._dispatch_event(event)

                    if event.handled:
                        return

                self.focused._dispatch_event(event)

                if event.handled:
                    return

                for widget in path:
                    widget._dispatch_event(event)

                    if event.handled:
                        return

        else:
            self._dispatch_event(event)
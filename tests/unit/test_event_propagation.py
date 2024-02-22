# SPDX-FileCopyrightText: 2024 Ohin "Kazani" Taylor <kazani@kazani.dev>
# SPDX-License-Identifier: MIT

"""Test main module of xenops."""

import _pytest.capture
from xenops.event import ClickEvent, Event, PointerEvent

from xenops.widget import Root, Widget
from xenops.widget.rect import Rect


def test_pointer_click() -> None:
    """Test that a mouse click propagates properly."""

    received = False

    root = Root()

    child = Widget()
    child._global_pos = Rect(50, 50, 50, 50)

    def handle_click(event: Event) -> None:
        nonlocal received
        received = True

    root.on(PointerEvent, handle_click)

    root.add_child(child)

    root.dispatch_event(PointerEvent(
        pos=(25, 25),
        left=True,
        middle=False,
        right=False
    ))

    assert received

def test_key_press() -> None:
    """Test that a mouse click propagates properly."""

    received = False

    root = Root()

    child = Widget()
    child._global_pos = Rect(50, 50, 50, 50)

    def handle_click(event: Event) -> None:
        nonlocal received
        received = True

    root.on(ClickEvent, handle_click)

    root.add_child(child)

    root.dispatch_event(ClickEvent(
        pos=(25, 25),
        button=1
    ))

    assert received
# src/blindwindow/core/console_multiplex.py

from __future__ import annotations
from enum import Enum
import sys
from typing import Any, Tuple, Optional, Set, List

class ConsoleMultiplex(str, Enum):
    RICH = "rich"
    BW = "blindwindow"
    NONE = "none"

class DummyConsole:
    """Fallback console when neither Rich nor BlindWindow is present."""
    def print(self, *args: Any, **kwargs: Any) -> None:
        file = sys.stderr if kwargs.get("stderr") else sys.stdout
        print(*args, file=file)

    def log(self, *args: Any, **kwargs: Any) -> None:
        self.print(*args, **kwargs)

def detect_available_consoles() -> List[ConsoleMultiplex]:
    available = []
    try:
        import blindwindow.core  # noqa: F401
        available.append(ConsoleMultiplex.BW)
    except ImportError:
        pass

    try:
        import rich.console  # noqa: F401
        available.append(ConsoleMultiplex.RICH)
    except ImportError:
        pass

    available.append(ConsoleMultiplex.NONE)
    return available

def resolve_multiplex_selection(
    force: Optional[ConsoleMultiplex] = None,
    avoid: Optional[Set[ConsoleMultiplex]] = None,
    order: Optional[List[ConsoleMultiplex]] = None,
) -> ConsoleMultiplex:
    avoid_set = avoid or set()
    order_list = order or []

    # 1. Direct force override
    if force is not None:
        return force

    available_backends = set(detect_available_consoles()) - avoid_set

    # 2. Check explicit order preference first
    for candidate in order_list:
        if candidate in available_backends:
            return candidate

    # 3. Check remaining backends not mentioned in `order`, using default precedence
    DEFAULT_FALLBACK_PRECEDENCE = [ConsoleMultiplex.BW, ConsoleMultiplex.RICH]
    for candidate in DEFAULT_FALLBACK_PRECEDENCE:
        if candidate in available_backends and candidate not in order_list:
            return candidate

    # 4. Safe fallback
    return ConsoleMultiplex.NONE

def get_consoles(
    force: Optional[ConsoleMultiplex] = None,
    avoid: Optional[Set[ConsoleMultiplex]] = None,
    order: Optional[List[ConsoleMultiplex]] = None,
) -> Tuple[Any, Any]:
    """
    Returns (console_stderr, console_stdout) based on installed packages
    and user preference flags.
    """
    selected = resolve_multiplex_selection(force=force, avoid=avoid, order=order)

    if selected == ConsoleMultiplex.BW:
        from blindwindow.core import Console
        return Console(stderr=True, tee_sys=True), Console(stderr=False, tee_sys=True)

    elif selected == ConsoleMultiplex.RICH:
        from rich.console import Console
        return Console(stderr=True), Console(stderr=False)

    else:
        dummy = DummyConsole()
        return dummy, dummy

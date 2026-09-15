#!/usr/bin/env python3
# src/blindwindow/core/blindwindow.py
from __future__ import annotations

import logging
import sys
import pyhabitat
import threading
import queue

from maxson_gui_utils.textpane import TextPane
from .ansi import strip_ansi
from .registration import (
    register_listener,
    unregister_listener,
)
from .streams import GuiStream, TeeStream

logger = logging.getLogger(__name__)


class BlindWindow(TextPane):
    """
    Passive output display window.
    Intercepts sys.stdout/sys.stderr and handles rendering.
    """

    def __init__(
        self,
        master=None,
        autoscroll: bool = True,
        **kwargs,
    ):
        self.autoscroll = autoscroll
        logger.debug("[BlindWindow.__init__] Initializing BlindWindow widget (autoscroll=%s)", autoscroll)
        super().__init__(master, **kwargs)

        self._append_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self._append_poll_id = self.after(10, self._drain_append_queue)

        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        # 1. Intercept raw stdout/stderr writes in current process
        logger.debug("[BlindWindow.__init__] Setting up GuiStream and TeeStream stdout/stderr interceptors...")
        self._sys_gui_stream = GuiStream(lambda text: self._safe_append(text, "stdout"))
        sys.stdout = TeeStream(self._orig_stdout, self._sys_gui_stream)
        sys.stderr = TeeStream(self._orig_stderr, self._sys_gui_stream)

        # 2. Register listener for in-process Console() dispatches
        logger.debug("[BlindWindow.__init__] Registering self._safe_append in-process listener...")
        register_listener(self._safe_append)

    def _safe_append(self, text: str, tag: str = "stdout") -> None:
        clean_text = strip_ansi(text)
        if not clean_text:
            return
        logger.debug(
            "[BlindWindow._safe_append] Thread=%s (%s) | text=%r",
            threading.current_thread().name,
            threading.get_ident(),
            clean_text[:30],
        )
        #self.after_idle(self._logged_append, clean_text, tag)
        self._append_queue.put((clean_text, tag))

    def _logged_append(self, text: str, tag: str = "stdout") -> None:
        """Wrapper around TextPane.append to verify Tkinter mainloop thread execution."""
        logger.debug("[BlindWindow._logged_append] Executing append in Tkinter mainloop | tag=%s | text_len=%d", tag, len(text))
        try:
            self.append(text, tag=tag)
            if hasattr(self, "see") and self.autoscroll:
                self.see("end")
            logger.debug("[BlindWindow._logged_append] Successfully inserted text into TextPane widget.")
        except Exception as err:
            logger.exception("[BlindWindow._logged_append] Exception occurred while inserting into TextPane: %s", err)

    def _drain_append_queue(self) -> None:
        """Drain pending output on the Tkinter mainloop thread."""
        try:
            while True:
                text, tag = self._append_queue.get_nowait()

                logger.debug(
                    "[BlindWindow._drain_append_queue] Main thread appending "
                    "| tag=%s | text_len=%d",
                    tag,
                    len(text),
                )

                self._logged_append(text, tag)

        except queue.Empty:
            pass

        try:
            self._append_poll_id = self.after(10, self._drain_append_queue)
        except Exception:
            logger.exception(
                "[BlindWindow._drain_append_queue] Failed to reschedule queue drain."
            )
            
    def destroy(self) -> None:
        """Clean up process I/O streams and unregister dispatch listeners."""
        logger.info(
            "[BlindWindow.destroy] Cleaning up streams and unregistering listeners..."
        )

        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr

        unregister_listener(self._safe_append)

        if getattr(self, "_append_poll_id", None) is not None:
            try:
                self.after_cancel(self._append_poll_id)
            except Exception:
                logger.debug(
                    "[BlindWindow.destroy] Failed to cancel append queue poll.",
                    exc_info=True,
                )
            self._append_poll_id = None

        super().destroy()


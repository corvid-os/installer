"""Main installer window -- a wizard walking through ALL_STEPS. Holds
InstallState centrally, renders the current step, handles Back/Next."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk  # noqa: E402

from corvid_installer.state import InstallState
from corvid_installer.steps import ALL_STEPS
from corvid_installer.steps.base import ValidationResult


class CorvidInstallerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(760, 620)
        self.set_title("Install Corvid OS")

        self.state = InstallState()
        self.steps = ALL_STEPS
        self.current_index = 0

        self.back_button = Gtk.Button(label="Back")
        self.back_button.connect("clicked", self._on_back)

        self.next_button = Gtk.Button(label="Next")
        self.next_button.add_css_class("suggested-action")
        self.next_button.connect("clicked", self._on_next)

        self.progress_label = Gtk.Label()
        self.progress_label.add_css_class("dim-label")

        header = Adw.HeaderBar()
        header.pack_start(self.back_button)
        header.pack_end(self.next_button)
        header.set_title_widget(self.progress_label)

        self.content_stack = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
            transition_duration=200,
        )
        self._current_step_widget: Gtk.Widget | None = None
        clamp = Adw.Clamp(maximum_size=640, tightening_threshold=480)
        clamp.set_child(self.content_stack)

        scroller = Gtk.ScrolledWindow(vexpand=True)
        scroller.set_child(clamp)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header)
        toolbar_view.set_content(scroller)

        self.set_content(toolbar_view)
        self._render_current_step()

    def _render_current_step(self) -> None:
        step = self.steps[self.current_index]
        widget = step.build_widget(self.state)

        # Only one step lives in the stack at a time -- drop the previous
        # one so we don't accumulate old widgets.
        if self._current_step_widget is not None:
            self.content_stack.remove(self._current_step_widget)
        self._current_step_widget = widget

        self.content_stack.add_named(widget, step.id)
        self.content_stack.set_visible_child_name(step.id)

        self.back_button.set_sensitive(self.current_index > 0)
        is_last = self.current_index == len(self.steps) - 1
        self.next_button.set_label("Finish" if is_last else "Next")
        self.progress_label.set_label(f"Step {self.current_index + 1} of {len(self.steps)} — {step.title}")

    def _on_next(self, _button) -> None:
        step = self.steps[self.current_index]
        validation = step.validate(self.state)
        if validation.result != ValidationResult.OK:
            toast = Adw.Toast.new(validation.message or "Fix the highlighted fields before continuing")
            # This skeleton's ToolbarView has no ToastOverlay wired in yet --
            # a full version should wrap the content in Adw.ToastOverlay.
            print(f"[validation] {toast.get_title()}")
            return

        step.apply(self.state)

        if self.current_index == len(self.steps) - 1:
            self.close()
            return

        self.current_index += 1
        self._render_current_step()

    def _on_back(self, _button) -> None:
        if self.current_index == 0:
            return
        self.current_index -= 1
        self._render_current_step()

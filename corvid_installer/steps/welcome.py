import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

from corvid_installer.i18n import tr
from corvid_installer.state import InstallState
from corvid_installer.steps.base import InstallStep
from corvid_installer.ui.page import build_step_page

LANGUAGES = ["English", "Polski"]

# Purely decorative -- cycles on the welcome screen while the real language
# picker below is what actually drives the (translated) rest of the UI.
HELLOS = [
    "Hello", "Cześć", "Hola", "Bonjour", "Hallo",
    "Ciao", "Olá", "Привет", "こんにちは", "你好", "안녕하세요",
]


class WelcomeStep(InstallStep):
    id = "welcome"
    title = "Welcome"

    _hello_timeout_id = None
    _hello_index = 0
    _hello_stack: Gtk.Stack | None = None

    def build_widget(self, state: InstallState) -> Gtk.Widget:
        if self._hello_timeout_id is not None:
            GLib.source_remove(self._hello_timeout_id)
            self._hello_timeout_id = None

        group = Adw.PreferencesGroup(title=tr(state, "welcome.language_group"))

        model = Gtk.StringList.new(LANGUAGES)
        row = Adw.ComboRow(title=tr(state, "welcome.language_row"), model=model)
        row.set_selected(LANGUAGES.index(state.language))

        def on_selected(combo_row, _pspec):
            new_language = LANGUAGES[combo_row.get_selected()]
            if new_language == state.language:
                return
            state.language = new_language
            if self.request_language_refresh:
                self.request_language_refresh()

        row.connect("notify::selected", on_selected)
        group.add(row)

        # Rotating greeting in a Stack so switching words crossfades instead
        # of just snapping to new text.
        hello_stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE, transition_duration=350)
        hello_stack.add_css_class("title-1")
        hello_stack.add_css_class("accent")
        first_label = self._make_hello_label(HELLOS[0])
        hello_stack.add_named(first_label, "hello-0")
        self._hello_stack = hello_stack
        self._hello_index = 0

        def cycle_hello():
            self._hello_index = (self._hello_index + 1) % len(HELLOS)
            name = f"hello-{self._hello_index}"
            label = self._make_hello_label(HELLOS[self._hello_index])
            hello_stack.add_named(label, name)
            hello_stack.set_visible_child_name(name)
            # Drop stale children once the crossfade to the new one finishes,
            # so the stack doesn't accumulate every greeting we've shown.
            GLib.timeout_add(hello_stack.get_transition_duration() + 50, self._prune_hello_stack, name)
            return GLib.SOURCE_CONTINUE

        self._hello_timeout_id = GLib.timeout_add(1100, cycle_hello)
        hello_stack.connect("unrealize", lambda *_: self._stop_hello())

        return build_step_page(
            icon_name="preferences-desktop-locale-symbolic",
            title=tr(state, "welcome.title"),
            subtitle=tr(state, "welcome.subtitle"),
            groups=[group],
            hero_widget=hello_stack,
        )

    @staticmethod
    def _make_hello_label(text: str) -> Gtk.Label:
        label = Gtk.Label(label=text)
        return label

    def _prune_hello_stack(self, keep_name: str) -> bool:
        stack = self._hello_stack
        if stack is None:
            return GLib.SOURCE_REMOVE
        pages = stack.get_pages()
        stale = []
        for i in range(pages.get_n_items()):
            page = pages.get_item(i)
            if page.get_name() != keep_name:
                stale.append(page.get_child())
        for child in stale:
            stack.remove(child)
        return GLib.SOURCE_REMOVE

    def _stop_hello(self) -> None:
        if self._hello_timeout_id is not None:
            GLib.source_remove(self._hello_timeout_id)
            self._hello_timeout_id = None

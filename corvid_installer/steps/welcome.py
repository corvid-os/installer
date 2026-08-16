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

    def build_widget(self, state: InstallState) -> Gtk.Widget:
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

        hero = self._build_hello_animation()

        return build_step_page(
            icon_name="preferences-desktop-locale-symbolic",
            title=tr(state, "welcome.title"),
            subtitle=tr(state, "welcome.subtitle"),
            groups=[group],
            hero_widget=hero,
        )

    @staticmethod
    def _build_hello_animation() -> Gtk.Widget:
        """Every call builds a fully self-contained rotating greeting --
        no state lives on `self`, so a rebuild (step re-navigation or a
        language-change re-render) can never cancel a *different* build's
        timeout. That cross-instance clobbering was the earlier bug where
        switching languages killed the animation for good."""
        stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.CROSSFADE, transition_duration=350)
        stack.add_css_class("title-1")
        stack.add_css_class("accent")
        stack.add_named(Gtk.Label(label=HELLOS[0]), "hello-0")

        anim = {"index": 0, "timeout_id": None}

        def prune_stale(keep_name: str) -> bool:
            pages = stack.get_pages()
            stale = [
                pages.get_item(i).get_child()
                for i in range(pages.get_n_items())
                if pages.get_item(i).get_name() != keep_name
            ]
            for child in stale:
                stack.remove(child)
            return GLib.SOURCE_REMOVE

        def cycle_hello() -> bool:
            anim["index"] = (anim["index"] + 1) % len(HELLOS)
            name = f"hello-{anim['index']}"
            stack.add_named(Gtk.Label(label=HELLOS[anim["index"]]), name)
            stack.set_visible_child_name(name)
            GLib.timeout_add(stack.get_transition_duration() + 50, prune_stale, name)
            return GLib.SOURCE_CONTINUE

        anim["timeout_id"] = GLib.timeout_add(1100, cycle_hello)

        def stop_hello(*_args) -> None:
            if anim["timeout_id"] is not None:
                GLib.source_remove(anim["timeout_id"])
                anim["timeout_id"] = None

        stack.connect("unrealize", stop_hello)

        return stack

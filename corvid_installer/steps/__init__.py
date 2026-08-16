"""Ordered list of install steps. Adding a step means one new file in this
package plus an entry here -- no changes needed in window.py."""

from corvid_installer.steps.bootloader import BootloaderStep
from corvid_installer.steps.desktop_choice import DesktopChoiceStep
from corvid_installer.steps.disk import DiskStep
from corvid_installer.steps.encryption import EncryptionStep
from corvid_installer.steps.finish import FinishStep
from corvid_installer.steps.keyboard import KeyboardStep
from corvid_installer.steps.locale import LocaleStep
from corvid_installer.steps.network import NetworkStep
from corvid_installer.steps.profile_choice import ProfileChoiceStep
from corvid_installer.steps.progress import ProgressStep
from corvid_installer.steps.snapshots import SnapshotsStep
from corvid_installer.steps.summary import SummaryStep
from corvid_installer.steps.user_account import UserAccountStep
from corvid_installer.steps.welcome import WelcomeStep

ALL_STEPS = [
    WelcomeStep(),
    KeyboardStep(),
    NetworkStep(),
    DiskStep(),
    EncryptionStep(),
    LocaleStep(),
    DesktopChoiceStep(),
    ProfileChoiceStep(),
    UserAccountStep(),
    BootloaderStep(),
    SnapshotsStep(),
    SummaryStep(),
    ProgressStep(),
    FinishStep(),
]

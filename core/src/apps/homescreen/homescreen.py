from . import TaskBase
from apps.base import lock_device
import storage.device
async def homescreen() -> None:
    await Homescreen()
    lock_device()


class Homescreen(TaskBase):
    def __init__(self) -> None:
        if not storage.device.is_initialized():
            from trezor.lvgls.scrs.initscreen import InitScreen
            InitScreen()
        else:
            from trezor.lvgls.scrs.homescreen import MainScreen
            MainScreen("My Trezor")


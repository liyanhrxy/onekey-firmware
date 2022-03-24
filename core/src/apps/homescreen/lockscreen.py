from . import TaskBase
from trezor import wire
async def lockscreen() -> None:
    from apps.common.request_pin import can_lock_device
    from apps.base import unlock_device

    # Only show the lockscreen UI if the device can in fact be locked.
    if can_lock_device():
        await Lockscreen()
    # Otherwise proceed directly to unlock() call. If the device is already unlocked,
    # it should be a no-op storage-wise, but it resets the internal configuration
    # to an unlocked state.
    try:
        await unlock_device()
    except wire.PinCancelled:
        pass

class Lockscreen(TaskBase):

    def __init__(self, bootscreen=False) -> None:
        if bootscreen:
            from trezor.lvgls.scrs.bootscreen import BootScreen
            BootScreen()
        from trezor.lvgls.scrs.lockscreen import LockScreen
        LockScreen()

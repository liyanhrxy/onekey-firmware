import storage
import storage.device
from trezor import config, log, loop, utils, wire

from apps.common.request_pin import can_lock_device, verify_user_pin
from apps.homescreen.lockscreen import Lockscreen



async def bootscreen() -> None:
    # bootscreen
    lockscreen = Lockscreen(bootscreen=True)
    while True:
        try:
            if can_lock_device():
                await lockscreen

            await verify_user_pin()
            storage.init_unlocked()
            return
        except wire.PinCancelled:
            # verify_user_pin will convert a SdCardUnavailable (in case of sd salt)
            # to PinCancelled exception.
            # Ignore exception, retry loop.
            pass
        except BaseException as e:
            # other exceptions here are unexpected and should halt the device
            if __debug__:
                log.exception(__name__, e)
            utils.halt(e.__class__.__name__)


config.init()
if __debug__ and not utils.EMULATOR:
    config.wipe()
loop.schedule(bootscreen())
loop.run()

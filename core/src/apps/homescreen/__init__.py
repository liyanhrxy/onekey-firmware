from typing import TYPE_CHECKING, Generator
import lvgl as lv
from trezor import loop, utils
from micropython import const

_TIMER_DELAY_MS = const(10)
signal_channel = loop.chan()
class TaskBase:

    TICKER_SLEEP: loop.Syscall = loop.sleep(_TIMER_DELAY_MS)
    # def __iter__(self) -> Generator:
    #     while True:
    #         lv.task_handler()
    #         if utils.EMULATOR:
    #             import SDL
    #             if not signal_channel.putters:
    #                 yield self.TICKER_SLEEP
    #                 lv.tick_inc(_TIMER_DELAY_MS)
    #                 SDL.refresh()
    #             else:
    #                 yield from signal_channel.take()
    #                 return
    async def __iter__(self) -> Generator:
        while True:
            lv.task_handler()
            if utils.EMULATOR:
                import SDL
                if not signal_channel.putters:
                    yield self.TICKER_SLEEP
                    lv.tick_inc(_TIMER_DELAY_MS)
                    SDL.refresh()
                else:
                    await signal_channel.take()
                    return

    if TYPE_CHECKING:
        def __await__(self) -> Generator:
            return self.__iter__()  # type: ignore

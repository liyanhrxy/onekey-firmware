import lvgl as lv
from .. import ui_images
from trezor import utils, log

lv.init()
if utils.EMULATOR:
    def emulate_init():
        import SDL
        SDL.init()
        # Register SDL display driver.
        draw_buf = lv.disp_draw_buf_t()
        buf1_1 = bytearray(480 * 10)
        draw_buf.init(buf1_1, None, len(buf1_1) // 4)
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = draw_buf
        disp_drv.flush_cb = SDL.monitor_flush
        disp_drv.hor_res = 480
        disp_drv.ver_res = 800
        disp_drv.register()

        # Regsiter SDL mouse driver

        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = SDL.mouse_read
        indev_drv.register()
        log.info('emulate_init', 'initialized successfully')
    try:
        emulate_init()
    except:
        log.error('emulate_init', 'failed to initialize emulator')

dispp = lv.disp_get_default()
theme = lv.theme_default_init(dispp, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.RED), True, lv.font_default())
dispp.set_theme(theme)
font_PJSBOLD36 = lv.font_load("A:ui_font_PJSBOLD36.bin")
font_PJSBOLD24 = lv.font_load("A:ui_font_PJSBOLD24.bin")
font_PJSMID20 = lv.font_load("A:ui_font_PJSMID20.bin")
font_MONO20 = lv.font_load("A:ui_font_MONO20.bin")
font_PJSBOLD32 = lv.font_load("A:ui_font_PJSBOLD32.bin")
font_PJSBOLD16 = lv.font_load("A:ui_font_PJSBOLD16.bin")
font_MONO24 = lv.font_load("A:ui_font_MONO24.bin")


def status_bar_init():
    ble = lv.img(lv.layer_top())
    ble.set_src(ui_images.ui_img_ble_png)
    ble.set_width(lv.SIZE.CONTENT)  # 0
    ble.set_height(lv.SIZE.CONTENT)   # 0
    ble.set_x(-30)
    ble.set_y(5)
    ble.set_align(lv.ALIGN.TOP_RIGHT)
    ble.set_pivot(0, 0)
    ble.set_angle(0)
    ble.set_zoom(255)
    battery = lv.img(lv.layer_top())
    battery.set_src(ui_images.ui_img_battery_png)
    battery.set_width(lv.SIZE.CONTENT)  # 96
    battery.set_height(lv.SIZE.CONTENT)   # 96
    battery.set_x(-5)
    battery.set_y(5)
    battery.set_align(lv.ALIGN.TOP_RIGHT)
    battery.set_pivot(0, 0)
    battery.set_angle(0)
    battery.set_zoom(255)


status_bar_init()

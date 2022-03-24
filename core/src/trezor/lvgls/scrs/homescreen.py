from .common import *
class MainScreen(Screen):
    def __init__(self, device_name='OneKey Touch'):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            lv.scr_load(self)
            return
        super().__init__()
        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_img_src(ui_images.ui_img_wallpaper_dark_png, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_img_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.device_name = lv.label(self)
        self.device_name.set_long_mode(lv.label.LONG.WRAP)
        self.device_name.set_text(device_name)
        self.device_name.set_width(lv.SIZE.CONTENT)  # 1
        self.device_name.set_height(lv.SIZE.CONTENT)   # 1
        self.device_name.set_x(0)
        self.device_name.set_y(-200)
        self.device_name.set_align(lv.ALIGN.CENTER)
        self.device_name.set_style_text_font(font_PJSBOLD36, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)
        lv.scr_load(self)
    def eventhandler(self, event_obj):
        target = event_obj.get_target()
        code = event_obj.code
        # dir = lv.indev_t.get_gesture_dir(lv.indev_get_act())
        # if dir == lv.DIR.TOP:
        #     print('top')
        if code == lv.EVENT.CLICKED:
            print('clicked home')
            # self.load_screen(InputPin(self))

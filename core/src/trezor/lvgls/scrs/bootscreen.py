from .common import *  # noqa: F401,F403


class BootScreen(Screen):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        super().__init__(*args, **kwargs)
        self.img = lv.img(self)
        self.img.set_src(ui_images.ui_img_onekey_png)
        self.img.set_width(lv.SIZE.CONTENT)  # 72
        self.img.set_height(lv.SIZE.CONTENT)   # 72
        self.img.set_x(0)
        self.img.set_y(-96)
        self.img.set_align(lv.ALIGN.CENTER)
        self.img.add_flag(lv.obj.FLAG.ADV_HITTEST)
        self.img.set_pivot(0, 0)
        self.img.set_angle(0)
        self.img.set_zoom(256)

        self.bar = lv.bar(self)
        self.bar.set_width(288)
        self.bar.set_height(8)
        self.bar.set_x(14)
        self.bar.set_y(236)
        self.bar.set_align(lv.ALIGN.CENTER)
        self.bar.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_border_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_border_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_border_width(1, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.bar.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.bar.set_style_bg_opa(255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.bar.set_style_anim_time(1000, lv.PART.MAIN)
        self.bar.set_value(100, lv.ANIM.OFF)
        lv.scr_load(self)

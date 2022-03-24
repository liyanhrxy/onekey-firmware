from ..common import *  # noqa: F401,F403


class NormalButton(lv.btn):
    def __init__(self, parent, text="Next", pos=(-6, 300), enable=True) -> None:
        super().__init__(parent)
        self.set_width(320)
        self.set_height(62)
        self.set_x(pos[0])
        self.set_y(pos[1])
        self.set_align(lv.ALIGN.CENTER)
        self.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        if enable:
            self.enable()
        else:
            self.disable()
        # the next btn label
        self.label = lv.label(self)
        self.label.set_long_mode(lv.label.LONG.WRAP)
        self.label.set_text(text)
        self.label.set_width(lv.SIZE.CONTENT)  # 1
        self.label.set_height(lv.SIZE.CONTENT)   # 1
        self.label.set_align(lv.ALIGN.CENTER)

    def disable(self) -> None:
        self.set_style_bg_color(lv.color_hex(0x323232), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.clear_flag(lv.btn.FLAG.CLICKABLE)

    def enable(self) -> None:
        self.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.add_flag(lv.btn.FLAG.CLICKABLE)

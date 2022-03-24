from trezor import config, loop
from apps.homescreen import signal_channel
from .common import *  # noqa: F401,F403
from .components.Button import NormalButton
from .components.keyboard import NumberKeyboard

PIN_MODE_SET = 1
PIN_MODE_VERIFY = 2
class PinTip(Screen):
    def __init__(self):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        kwargs = {"title": "Set a PIN"}
        super().__init__(**kwargs)

        self.btn = NormalButton(self, text="Continue")
        self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)

        self.sub_title = lv.label(self)
        self.sub_title.set_long_mode(lv.label.LONG.WRAP)
        self.sub_title.set_text("Set a PIN to protect you wallet. OneKey will ask for PIN eachtime when unlock your device. So you need to know:")
        self.sub_title.set_width(lv.pct(80))
        self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
        self.sub_title.set_x(0)
        self.sub_title.set_y(lv.pct(30))
        # self.sub_title.add_style(SubTitleStyle(), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_align(lv.ALIGN.TOP_MID)
        self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.cb_bg1 = lv.obj(self)
        self.cb_bg1.set_width(400)
        self.cb_bg1.set_height(107)
        self.cb_bg1.set_x(-10)
        self.cb_bg1.set_y(0)
        self.cb_bg1.set_align(lv.ALIGN.CENTER)
        self.cb_bg1.set_style_radius(16, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg1.set_style_bg_color(lv.color_hex(0x191919), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg1.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg1.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg1.set_style_border_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg1.add_flag(lv.obj.FLAG.HIDDEN)

        self.cb1 = lv.checkbox(self)
        self.cb1.set_width(40)
        self.cb1.set_height(40)
        self.cb1.set_x(40)
        self.cb1.set_y(380)
        self.cb1.set_text("")
        self.cb1.set_style_radius(8, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb1.set_style_border_color(lv.color_hex(0x1E1E1E), lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb1.set_style_border_opa(255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb1.set_style_bg_color(lv.color_hex(0x1BAC44), lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.cb1.set_style_bg_opa(255, lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.cb1.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)

        self.tip1 = lv.label(self)
        self.tip1.set_long_mode(lv.label.LONG.WRAP)
        self.tip1.set_text("Using a strong PIN to protects your wallet from unauthorized physical access.")
        self.tip1.set_width(lv.pct(70))
        self.tip1.set_height(lv.SIZE.CONTENT)   # 1
        self.tip1.set_x(0)
        self.tip1.set_y(380)
        self.tip1.set_align(lv.ALIGN.TOP_MID)
        self.tip1.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.tip1.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.tip1.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.tip1.set_style_text_line_space(5, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.tip1.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.tip1.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.cb_bg2 = lv.obj(self)
        self.cb_bg2.set_width(400)
        self.cb_bg2.set_height(82)
        self.cb_bg2.set_x(-10)
        self.cb_bg2.set_y(100)
        self.cb_bg2.set_align(lv.ALIGN.CENTER)
        self.cb_bg2.set_style_radius(16, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg2.set_style_bg_color(lv.color_hex(0x191919), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg2.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg2.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg2.set_style_border_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.cb_bg2.add_flag(lv.obj.FLAG.HIDDEN)

        self.cb2 = lv.checkbox(self)
        self.cb2.set_width(40)
        self.cb2.set_height(40)
        self.cb2.set_x(40)
        self.cb2.set_y(100)
        self.cb2.set_align(lv.ALIGN.LEFT_MID)
        self.cb2.set_text("")
        self.cb2.set_style_radius(8, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb2.set_style_border_color(lv.color_hex(0x1E1E1E), lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb2.set_style_border_opa(255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.cb2.set_style_bg_color(lv.color_hex(0x1BAC44), lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.cb2.set_style_bg_opa(255, lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.cb2.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)

        tip2 = lv.label(self)
        tip2.set_long_mode(lv.label.LONG.WRAP)
        tip2.set_text("Keeping your PIN secured, be sure to store it separate from recovery phrase.")
        tip2.set_width(lv.pct(70))
        tip2.set_height(lv.SIZE.CONTENT)   # 1
        tip2.set_x(0)
        tip2.set_y(480)
        tip2.set_align(lv.ALIGN.TOP_MID)
        tip2.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
        tip2.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        tip2.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        tip2.set_style_text_line_space(5, lv.PART.MAIN | lv.STATE.DEFAULT)
        tip2.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
        tip2.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.cb_cnt = 0

    def on_click(self, target):
        self.load_screen(InputPin(self, PIN_MODE_SET))

    def on_value_changed(self, target):
            if target == self.cb1:
                if target.get_state() & lv.STATE.CHECKED:
                    self.cb_bg1.clear_flag(lv.obj.FLAG.HIDDEN)
                    self.cb_cnt += 1
                else:
                    self.cb_bg1.add_flag(lv.obj.FLAG.HIDDEN)
                    self.cb_cnt -= 1
            elif target == self.cb2:
                if target.get_state() & lv.STATE.CHECKED:
                    self.cb_bg2.clear_flag(lv.obj.FLAG.HIDDEN)
                    self.cb_cnt += 1
                else:
                    self.cb_bg2.add_flag(lv.obj.FLAG.HIDDEN)
                    self.cb_cnt -= 1
            if self.cb_cnt == 2:
                self.btn.enable()
            elif self.cb_cnt < 3:
                self.btn.disable()
pin_channel = loop.chan()
class InputPin(Screen):
    def __init__(self, prev_scr, pin_mode=PIN_MODE_VERIFY):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        super().__init__(prev_scr, nav_back=True)
        self.title = lv.label(self)
        self.title.set_long_mode(lv.label.LONG.WRAP)
        self.pin_mode = pin_mode
        if pin_mode == PIN_MODE_SET:
            self.title.set_text("Set PIN")
        else:
            self.title.set_text("Enter PIN")
        self.title.set_width(lv.SIZE.CONTENT)  # 1
        self.title.set_height(lv.SIZE.CONTENT)   # 1
        self.title.set_x(lv.pct(0))
        self.title.set_y(lv.pct(15))

        self.title.set_align(lv.ALIGN.TOP_MID)

        self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.title.set_style_text_font(font_PJSBOLD36, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_tile = lv.label(self)
        self.sub_tile.set_long_mode(lv.label.LONG.WRAP)
        self.sub_tile.set_text("Incorrect PIN. Try again.")
        self.sub_tile.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)  # 1
        self.sub_tile.set_style_text_color(lv.color_hex(0xFF0000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_tile.align_to(self.title, lv.ALIGN.OUT_BOTTOM_MID, 0, 24)
        self.sub_tile.add_flag(lv.obj.FLAG.HIDDEN)
        self.keyboard = NumberKeyboard(self)
        self.keyboard.add_event_cb(self.on_ready, lv.EVENT.READY | lv.EVENT.VALUE_CHANGED, None)
        self.first_pin = ""
    def on_ready(self, event_obj):
        code = event_obj.code
        if code == lv.EVENT.VALUE_CHANGED:
            self.sub_tile.add_flag(lv.obj.FLAG.HIDDEN)
            return
        input = self.keyboard.ta.get_text()
        if input == "":
            return
        if self.pin_mode == PIN_MODE_SET:
            if self.first_pin:
                if self.first_pin == input:
                    # self.msg_channel.publish(input)
                    # self.first_pin = ""
                    self.change_pin(input)
                else:
                    self.sub_tile.clear_flag(lv.obj.FLAG.HIDDEN)
            else:
                self.first_pin = input
                self.keyboard.ta.set_text("")
                self.title.set_text("Enter PIN Again")
        else:
            pin_channel.publish(input)
            signal_channel.publish('exit')
            self.load_screen(self.prev_scr, destory_self=True)


    def change_pin(self, pin):
        # write into storage
        if not config.change_pin("", pin, None, None):
            raise RuntimeError("Failed to change pin")
        else:
            self.load_screen(SetupComplete(), destory_self=True)

class SetupComplete(Screen):

    def __init__(self, sub_title=""):
        if not hasattr(self, "_init"):
                self._init = True
        else:
            return
        super().__init__()
        self.title = lv.label(self)
        self.title.set_long_mode(lv.label.LONG.WRAP)
        self.title.set_text("Setup Complete")
        self.title.set_width(lv.pct(80))
        self.title.set_height(lv.SIZE.CONTENT)   # 1
        self.title.set_x(lv.pct(0))
        self.title.set_y(lv.pct(35))
        self.title.set_align( lv.ALIGN.TOP_MID)
        self.title.set_style_text_color( lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
        self.title.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        self.title.set_style_text_letter_space( 0, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.title.set_style_text_line_space( 10, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.title.set_style_text_align( lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.title.set_style_text_font( font_PJSBOLD36, lv.PART.MAIN | lv.STATE.DEFAULT )

        self.sub_title = lv.label(self)
        self.sub_title.set_long_mode(lv.label.LONG.WRAP)
        self.sub_title.set_text(sub_title)
        self.sub_title.set_width(lv.pct(80))
        self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
        self.sub_title.set_x(0)
        self.sub_title.set_y(lv.pct(42))
        self.sub_title.set_align( lv.ALIGN.TOP_MID)
        self.sub_title.set_style_text_color( lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT )
        self.sub_title.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        self.sub_title.set_style_text_align( lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.sub_title.set_style_text_font( font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT )

        self.btn = lv.btn(self)
        self.btn.set_width(320)
        self.btn.set_height(62)
        self.btn.set_x(-6)
        self.btn.set_y(300)
        self.btn.set_align( lv.ALIGN.CENTER)
        self.btn.set_style_radius( 32, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.btn.set_style_bg_color( lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT )
        self.btn.set_style_bg_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        self.btn.set_style_text_color( lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT )
        self.btn.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT )
        self.btn.set_style_text_font( font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT )
        self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED | lv.EVENT.PRESSED, None)

        self.btn_label = lv.label(self.btn)
        self.btn_label.set_long_mode(lv.label.LONG.WRAP)
        self.btn_label.set_text("Done")
        self.btn_label.set_width(lv.SIZE.CONTENT)	# 1
        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
        self.btn_label.set_align( lv.ALIGN.CENTER)
        self.btn_label.set_style_text_font( font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT )

        self.icon = lv.img(self)
        self.icon.set_src(ui_images.ui_img_success_icon_png)
        self.icon.set_width(lv.SIZE.CONTENT)	# 1
        self.icon.set_height(lv.SIZE.CONTENT)   # 1
        self.icon.set_align(lv.ALIGN.CENTER)
        self.icon.set_x(lv.pct(0))
        self.icon.set_y(lv.pct(-30))
        self.icon.set_pivot(0,0)
        self.icon.set_angle(0)
        self.icon.set_zoom(256)
    def on_click(self, target):
        # self.load_screen(LockScreen())
        # apps.base.set_homescreen()
        pass

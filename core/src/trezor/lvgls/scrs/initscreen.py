import storage
from trezor.crypto import bip39, hashlib, random
from trezor.enums import BackupType
from .common import *
from .components.Button import NormalButton
from .components.Style import SubTitleStyle
from ..lv_colors import lv_colors
from .components.keyboard import CharacterKeyboard
from .pinscreen import PinTip

word_cnt_strength_map = {
    12: 128,
    18: 192,
    24: 256,
}
select_word_cnt = 12
mnemonics = []
mnemonic_str = ''
check_index = 0
check_selected = ""


class InitScreen(Screen):
    """Language and Init way select screens."""
    def __init__(self) -> None:
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        kwargs = {
            "title": "Select Language",
            "title_pos": (lv.pct(0), lv.pct(-5)),
            "title_align": lv.ALIGN.CENTER,
        }
        super().__init__(**kwargs)
        print("InitScreen==================")

        # earth icon
        self.icon = lv.img(self)
        self.icon.set_src(ui_images.ui_img_language_png)
        self.icon.set_width(lv.SIZE.CONTENT)  # 100
        self.icon.set_height(lv.SIZE.CONTENT)   # 100
        self.icon.set_x(lv.pct(0))
        self.icon.set_y(lv.pct(-30))
        self.icon.set_align(lv.ALIGN.CENTER)
        self.icon.set_pivot(0, 0)
        self.icon.set_angle(0)
        self.icon.set_zoom(255)
        # the roller of select language
        self.roller = lv.roller(self)
        self.roller.set_options("English\nChinese", lv.roller.MODE.NORMAL)
        self.roller.set_width(448)
        self.roller.set_height(157)
        self.roller.set_x(0)
        self.roller.set_y(lv.pct(15))
        self.roller.set_align(lv.ALIGN.CENTER)
        self.roller.set_style_text_color(lv.color_hex(0x666666), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_line_space(40, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x191919), lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(255, lv.PART.SELECTED | lv.STATE.DEFAULT)
        # add callback for roller
        self.roller.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)
        # the btn next
        self.btn = lv.btn(self)
        self.btn.set_width(320)
        self.btn.set_height(62)
        self.btn.set_x(-6)
        self.btn.set_y(300)
        self.btn.set_align(lv.ALIGN.CENTER)
        self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        # add callback for btn next
        self.btn.add_event_cb(self.eventhandler, lv.EVENT.PRESSED | lv.EVENT.CLICKED, None)
        # the next btn label
        self.btn_label = lv.label(self.btn)
        self.btn_label.set_long_mode(lv.label.LONG.WRAP)
        self.btn_label.set_text("Next")
        self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
        self.btn_label.set_align(lv.ALIGN.CENTER)
        self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        lv.scr_load(self)

    def on_click(self, target):
        self.load_screen(self.QuickStart(self))

    def on_value_changed(self, target):
        str = " " * 10
        target.get_selected_str(str, len(str))
        print(f"roller value changed index ==== {target.get_selected()} ===str== {str.strip()}")

    class QuickStart(Screen):
        def __init__(self, prev_scr):
            if not hasattr(self, "_init"):
                self._init = True
            else:
                return
            print("QuickStart==================")
            kwargs = {"title": "Quick Start"}
            super().__init__(prev_scr, nav_back=True, **kwargs)
            self.selected_index = 0
            self.selected_str = ""

            # the init type roller
            self.roller = lv.roller(self)
            self.roller.set_options("Create New Wallet\nRestore Wallet", lv.roller.MODE.NORMAL)
            self.roller.set_width(448)
            self.roller.set_height(157)
            self.roller.set_x(0)
            self.roller.set_y(lv.pct(15))
            self.roller.set_align(lv.ALIGN.CENTER)
            self.roller.set_style_text_color(lv.color_hex(0x666666), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_text_line_space(40, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_radius(24, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_border_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.roller.set_style_radius(24, lv.PART.SELECTED | lv.STATE.DEFAULT)
            self.roller.set_style_bg_color(lv.color_hex(0x191919), lv.PART.SELECTED | lv.STATE.DEFAULT)
            self.roller.set_style_bg_opa(255, lv.PART.SELECTED | lv.STATE.DEFAULT)
            self.roller.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)
            # the btn start
            self.btn = lv.btn(self)
            self.btn.set_width(320)
            self.btn.set_height(62)
            self.btn.set_x(-6)
            self.btn.set_y(300)
            self.btn.set_align(lv.ALIGN.CENTER)
            self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED | lv.EVENT.PRESSED, None)
            # the btn start label
            self.btn_label = lv.label(self.btn)
            self.btn_label.set_long_mode(lv.label.LONG.WRAP)
            self.btn_label.set_text("Start")
            self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
            self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
            self.btn_label.set_x(0)
            self.btn_label.set_y(0)
            self.btn_label.set_align(lv.ALIGN.CENTER)
            self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
            # the sub title
            self.sub_title = lv.label(self)
            self.sub_title.set_long_mode(lv.label.LONG.WRAP)
            self.sub_title.set_text("Create a new wallet, or restore wallet used before from a backup.")
            self.sub_title.set_width(lv.pct(80))
            self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
            self.sub_title.set_x(0)
            self.sub_title.set_y(lv.pct(25))
            self.sub_title.set_align(lv.ALIGN.TOP_MID)
            self.sub_title.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
            self.sub_title.set_scroll_dir(lv.DIR.ALL)
            self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

        def on_click(self, target):
            if self.selected_index == 0:
                self.load_screen(CreateNew(self))
            elif self.selected_index == 1:
                self.load_screen(Recovery(self))
            else:
                print("error, unknown operation")

        def on_value_changed(self, target):
            self.selected_index = target.get_selected()
            self.selected_str = " " * 20
            target.get_selected_str(self.selected_str, len(self.selected_str))
            print(f"roller value changed index ==== {self.selected_index} ===str== {self.selected_str.strip()}")

class CreateNew(Screen):
    """Screens associated with creating a new wallet"""
    def __init__(self, prev_scr):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        kwargs = {"title": "Create a new wallet"}
        super().__init__(prev_scr, nav_back=True, **kwargs)

        # the roller
        self.roller = lv.roller(self)
        self.roller.set_options("12\n18\n24", lv.roller.MODE.NORMAL)
        self.roller.set_width(448)
        self.roller.set_height(157)
        self.roller.set_x(0)
        self.roller.set_y(lv.pct(15))
        self.roller.set_align(lv.ALIGN.CENTER)
        self.roller.set_style_text_color(lv.color_hex(0x666666), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_line_space(40, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x191919), lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(255, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)
        # the btn
        self.btn = lv.btn(self)
        self.btn.set_width(320)
        self.btn.set_height(62)
        self.btn.set_x(-6)
        self.btn.set_y(300)
        self.btn.set_align(lv.ALIGN.CENTER)
        self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)
        # the btn label
        self.btn_label = lv.label(self.btn)
        self.btn_label.set_long_mode(lv.label.LONG.WRAP)
        self.btn_label.set_text("Create")
        self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
        self.btn_label.set_x(0)
        self.btn_label.set_y(0)
        self.btn_label.set_align(lv.ALIGN.CENTER)
        self.btn_label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
        self.btn_label.set_scroll_dir(lv.DIR.ALL)
        self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        # the subtitle
        self.sub_title = lv.label(self)
        self.sub_title.set_long_mode(lv.label.LONG.WRAP)
        self.sub_title.set_text("Select the number of words.")
        self.sub_title.set_width(lv.pct(80))
        self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
        self.sub_title.set_x(0)
        self.sub_title.set_y(lv.pct(25))
        self.sub_title.set_align(lv.ALIGN.TOP_MID)
        self.sub_title.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
        self.sub_title.set_scroll_dir(lv.DIR.ALL)
        self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.word_cnt_list = [12, 18, 24]
        global select_word_cnt
        select_word_cnt = 12

    def on_click(self, target):
        self.load_screen(self.BackupTip(self))

    def on_value_changed(self, target):
        global select_word_cnt
        selected_index = int(target.get_selected())
        select_word_cnt = self.word_cnt_list[selected_index]

    class BackupTip(Screen):
        def __init__(self, prev_scr):
            if not hasattr(self, "_init"):
                self._init = True
            else:
                return
            kwargs = {"title": "Back Up Recovery Phrase"}
            super().__init__(prev_scr, nav_back=True, **kwargs)

            self.btn = NormalButton(self, text="Continue")
            self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)

            self.sub_title = lv.label(self)
            self.sub_title.set_long_mode(lv.label.LONG.WRAP)
            self.sub_title.set_text("Next, OneKey will display a list of words, which is called the recovery phrase of wallet. So you need to know:")
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
            self.cb_bg1.set_height(80)
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
            self.tip1.set_text("If you lose recovery phrase, you will lose all your fund.")
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
            self.cb_bg2.set_height(80)
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
            tip2.set_text("Never take photo or make digital copys, and never upload it online.")
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

            self.cb_bg3 = lv.obj(self)
            self.cb_bg3.set_width(400)
            self.cb_bg3.set_height(80)
            self.cb_bg3.set_x(-10)
            self.cb_bg3.set_y(200)
            self.cb_bg3.set_align(lv.ALIGN.CENTER)
            self.cb_bg3.set_style_radius(16, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.cb_bg3.set_style_bg_color(lv.color_hex(0x191919), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.cb_bg3.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.cb_bg3.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.cb_bg3.set_style_border_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.cb_bg3.add_flag(lv.obj.FLAG.HIDDEN)

            self.cb3 = lv.checkbox(self)
            self.cb3.set_width(40)
            self.cb3.set_height(40)
            self.cb3.set_x(40)
            self.cb3.set_y(200)
            self.cb3.set_text("")
            self.cb3.set_align(lv.ALIGN.LEFT_MID)
            self.cb3.set_style_radius(8, lv.PART.INDICATOR | lv.STATE.DEFAULT)
            self.cb3.set_style_border_color(lv.color_hex(0x1E1E1E), lv.PART.INDICATOR | lv.STATE.DEFAULT)
            self.cb3.set_style_border_opa(255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
            self.cb3.set_style_bg_color(lv.color_hex(0x1BAC44), lv.PART.INDICATOR | lv.STATE.CHECKED)
            self.cb3.set_style_bg_opa(255, lv.PART.INDICATOR | lv.STATE.CHECKED)
            self.cb3.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)

            tip3 = lv.label(self)
            tip3.set_long_mode(lv.label.LONG.WRAP)
            tip3.set_text("Keeping your backup secured and never send it to anyone.")
            tip3.set_width(lv.pct(70))
            tip3.set_height(lv.SIZE.CONTENT)   # 1
            tip3.set_x(0)
            tip3.set_y(580)
            tip3.set_align(lv.ALIGN.TOP_MID)
            tip3.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
            tip3.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tip3.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
            tip3.set_style_text_line_space(5, lv.PART.MAIN | lv.STATE.DEFAULT)
            tip3.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
            tip3.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

            self.cb_cnt = 0

        def on_click(self, target):
            self.load_screen(self.ManualBackup(self))

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
                elif target == self.cb3:
                    if target.get_state() & lv.STATE.CHECKED:
                        self.cb_bg3.clear_flag(lv.obj.FLAG.HIDDEN)
                        self.cb_cnt += 1
                    else:
                        self.cb_bg3.add_flag(lv.obj.FLAG.HIDDEN)
                        self.cb_cnt -= 1
                if self.cb_cnt == 3:
                    self.btn.enable()
                elif self.cb_cnt < 3:
                    self.btn.disable()

        class ManualBackup(Screen):
            def __init__(self, prev_scr):
                if not hasattr(self, "_init"):
                    self._init = True
                else:
                    return
                kwargs = {"title": "Manual Backup"}
                super().__init__(prev_scr, nav_back=True, **kwargs)
                print("========ManualBackup")

                self.sub_title = lv.label(self)
                self.sub_title.set_long_mode(lv.label.LONG.WRAP)
                global select_word_cnt
                self.sub_title.set_text(f"Write down the following {select_word_cnt} words in order.")
                self.sub_title.set_width(lv.pct(80))
                self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
                self.sub_title.set_x(0)
                self.sub_title.set_y(lv.pct(22))
                self.sub_title.set_align(lv.ALIGN.TOP_MID)
                self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
                self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

                self.btn = NormalButton(self)
                # self.btn.set_width(320)
                # self.btn.set_height(62)
                # self.btn.set_x(-6)
                # self.btn.set_y(300)
                # self.btn.set_align(lv.ALIGN.CENTER)
                # self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
                # self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
                # self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                # self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
                # self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                # self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)

                # self.btn_label = lv.label(self.btn)
                # self.btn_label.set_long_mode(lv.label.LONG.WRAP)
                # self.btn_label.set_text("Next")
                # self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
                # self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
                # self.btn_label.set_align(lv.ALIGN.CENTER)
                # self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)

                self.words_panel = lv.obj(self)
                self.words_panel.set_width(lv.SIZE.CONTENT)
                self.words_panel.set_height(lv.SIZE.CONTENT)
                self.words_panel.align(lv.ALIGN.CENTER, 0, 0)
                self.words_panel.set_style_radius(16, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.words_panel.set_style_bg_color(lv.color_hex(0x323232), lv.PART.MAIN | lv.STATE.DEFAULT)
                self.words_panel.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.words_panel.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
                self.words_panel.set_style_border_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                # label display the first column
                self.word_col = lv.label(self.words_panel)
                self.word_col.set_pos(0, 0)
                self.word_col.set_width(180)
                self.word_col.set_height(lv.SIZE.CONTENT)
                self.word_col.set_style_text_font(font_MONO20, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col.set_style_pad_all(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col.set_style_text_line_space(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                # label display the second column
                self.word_col2 = lv.label(self.words_panel)
                self.word_col2.set_pos(210, 0)
                self.word_col2.set_width(180)
                self.word_col2.set_height(lv.SIZE.CONTENT)
                self.word_col2.set_style_text_font(font_MONO20, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col2.set_style_text_align(lv.TEXT_ALIGN.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col2.set_style_pad_ver(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col2.set_style_pad_left(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                self.word_col2.set_style_text_line_space(10, lv.PART.MAIN | lv.STATE.DEFAULT)

                global mnemonics
                mnemonics = init_device(word_cnt_strength_map[select_word_cnt])
                text_col = ""
                text_col2 = ""
                for index in range(0, select_word_cnt / 2):
                    text_col += f'{index+1:>2}. {mnemonics[index]}\n'
                    text_col2 += f'{int(index+select_word_cnt/2+1):>2}. {mnemonics[int(index+select_word_cnt/2)]}\n'
                self.word_col.set_text(text_col.strip())
                self.word_col2.set_text(text_col2.strip())

            def on_click(self, target):
                self.load_screen(self.CheckRecoveryPhrase(self))

            class CheckRecoveryPhrase(Screen):
                def __init__(self, prev_scr):
                    if not hasattr(self, "_init"):
                        self._init = True
                    else:
                        return
                    kwargs = {"title": "Check Recovery Phrase", "subtitle": ""}
                    super().__init__(prev_scr, nav_back=True, **kwargs)

                    self.btn = NormalButton(self, text="Continue")
                    self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)

                    self.sub_title = lv.label(self)
                    self.sub_title.set_long_mode(lv.label.LONG.WRAP)
                    global select_word_cnt
                    self.sub_title.set_text(f"Check {select_word_cnt} words again, make sure they are exactly the same as the backup you just wrote down.")
                    self.sub_title.set_width(lv.pct(80))
                    self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
                    self.sub_title.set_x(0)
                    self.sub_title.set_y(lv.pct(30))
                    self.sub_title.set_align(lv.ALIGN.TOP_MID)
                    self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
                    self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                    self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
                    self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

                def on_click(self, target):
                    self.load_screen(self.CheckWord(self))
                class CheckWord(Screen):
                    def __init__(self, prev_scr):
                        if not hasattr(self, "_init"):
                            self._init = True
                        else:
                            return
                        kwargs = {"title": "Check Word #1", "subtitle": ""}
                        super().__init__(prev_scr, nav_back=True, **kwargs)
                        # the roller
                        self.roller = lv.roller(self)
                        choices = get_choices()
                        global check_selected
                        check_selected = choices[1]
                        self.roller.set_options(f"{choices[0]}\n{choices[1]}\n{choices[2]}", lv.roller.MODE.NORMAL)
                        self.roller.set_width(448)
                        self.roller.set_height(157)
                        self.roller.set_x(0)
                        self.roller.set_y(lv.pct(15))
                        self.roller.set_align(lv.ALIGN.CENTER)
                        self.roller.set_style_text_color(lv.color_hex(0x666666), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_text_line_space(40, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_radius(24, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_border_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.roller.set_style_radius(24, lv.PART.SELECTED | lv.STATE.DEFAULT)
                        self.roller.set_style_bg_color(lv.color_hex(0x191919), lv.PART.SELECTED | lv.STATE.DEFAULT)
                        self.roller.set_visible_row_count(3)
                        self.roller.set_selected(1, lv.ANIM.OFF)
                        self.roller.set_style_bg_opa(255, lv.PART.SELECTED | lv.STATE.DEFAULT)
                        self.roller.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)
                        # the btn
                        self.btn = lv.btn(self)
                        self.btn.set_width(320)
                        self.btn.set_height(62)
                        self.btn.set_x(-6)
                        self.btn.set_y(300)
                        self.btn.set_align(lv.ALIGN.CENTER)
                        self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED, None)
                        # the btn label
                        self.btn_label = lv.label(self.btn)
                        self.btn_label.set_long_mode(lv.label.LONG.WRAP)
                        self.btn_label.set_text("Next")
                        self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
                        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
                        self.btn_label.set_align(lv.ALIGN.CENTER)
                        self.btn_label.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
                        self.btn_label.set_scroll_dir(lv.DIR.ALL)
                        self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
                        # the subtitle
                        self.sub_title = lv.label(self)
                        self.sub_title.set_long_mode(lv.label.LONG.WRAP)
                        self.sub_title.set_text("Choose the correct word.")
                        self.sub_title.set_width(lv.pct(80))
                        self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
                        self.sub_title.set_x(0)
                        self.sub_title.set_y(lv.pct(25))
                        self.sub_title.set_align(lv.ALIGN.TOP_MID)
                        self.sub_title.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
                        self.sub_title.set_scroll_dir(lv.DIR.ALL)
                        self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
                        self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)

                    def on_click(self, target):
                        global check_index, check_selected
                        if check_selected == mnemonics[check_index]:
                            check_index += 1
                            if check_index >= len(mnemonics):
                                save_mnemonics()
                                self.load_screen(WalletReady("You have successfully created your wallet."))
                            else:
                                choices = get_choices()
                                check_selected = choices[1]
                                self.roller.set_options(f"{choices[0]}\n{choices[1]}\n{choices[2]}", lv.roller.MODE.NORMAL)
                                self.roller.set_selected(1, lv.ANIM.OFF)
                                self.title.set_text(f"Check Word #{check_index+1}")
                                self.sub_title.set_text(f"Choose the correct word.")
                                self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
                        else:
                            self.sub_title.set_text("Incorrect word, try again.")
                            self.sub_title.set_style_text_color(lv_colors.RED, lv.PART.MAIN | lv.STATE.DEFAULT)

                    def on_value_changed(self, target):
                        global check_selected
                        check_selected = " " * 11
                        target.get_selected_str(check_selected, len(check_selected))
                        check_selected = check_selected.strip()[:-1]
class Recovery(Screen):
    """Screens associated with importing a wallet"""
    def __init__(self, prev_scr):
        if not hasattr(self, "_init"):
            self._init = True
        else:
            return
        kwargs = {"title": "Import Wallet", "sub_title": ""}
        super().__init__(prev_scr, nav_back=True, **kwargs)

        # the roller
        self.roller = lv.roller(self)
        self.roller.set_options("12\n18\n24", lv.roller.MODE.NORMAL)
        self.roller.set_width(448)
        self.roller.set_height(157)
        self.roller.set_x(0)
        self.roller.set_y(lv.pct(15))
        self.roller.set_align(lv.ALIGN.CENTER)
        self.roller.set_style_text_color(lv.color_hex(0x666666), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_letter_space(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_line_space(40, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_border_opa(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.roller.set_style_radius(24, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_color(lv.color_hex(0x191919), lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.set_style_bg_opa(255, lv.PART.SELECTED | lv.STATE.DEFAULT)
        self.roller.add_event_cb(self.eventhandler, lv.EVENT.VALUE_CHANGED, None)
        # the btn
        self.btn = lv.btn(self)
        self.btn.set_width(320)
        self.btn.set_height(62)
        self.btn.set_x(-6)
        self.btn.set_y(300)
        self.btn.set_align(lv.ALIGN.CENTER)
        self.btn.set_style_radius(32, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.btn.add_event_cb(self.eventhandler, lv.EVENT.CLICKED | lv.EVENT.PRESSED, None)
        # the btn label
        self.btn_label = lv.label(self.btn)
        self.btn_label.set_long_mode(lv.label.LONG.WRAP)
        self.btn_label.set_text("Continue")
        self.btn_label.set_width(lv.SIZE.CONTENT)  # 1
        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
        self.btn_label.set_x(0)
        self.btn_label.set_y(0)
        self.btn_label.set_align(lv.ALIGN.CENTER)
        self.btn_label.set_style_text_font(font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT)
        # the sub title
        self.sub_title = lv.label(self)
        self.sub_title.set_long_mode(lv.label.LONG.WRAP)
        self.sub_title.set_text("Select the number of words.")
        self.sub_title.set_width(lv.pct(80))
        self.sub_title.set_height(lv.SIZE.CONTENT)   # 1
        self.sub_title.set_x(0)
        self.sub_title.set_y(lv.pct(25))
        self.sub_title.set_align(lv.ALIGN.TOP_MID)
        self.sub_title.set_style_text_color(lv.color_hex(0xCCCCCC), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.sub_title.set_style_text_font(font_PJSMID20, lv.PART.MAIN | lv.STATE.DEFAULT)
        global select_word_cnt
        select_word_cnt = 12
    def on_click(self, target):
        self.load_screen(self.EnterWord(self))

    def on_value_changed(self, target):
        global select_word_cnt
        # self.selected_index = target.get_selected()
        selected_str = " " * 3
        target.get_selected_str(selected_str, len(selected_str))
        select_word_cnt = int(selected_str.strip()[:-1])
    class EnterWord(Screen):
        def __init__(self, prev_scr):
            if not hasattr(self, "_init"):
                self._init = True
            else:
                return
            super().__init__(prev_scr, nav_back=True)

            self.title = lv.label(self)
            self.title.set_long_mode(lv.label.LONG.WRAP)
            self.title.set_text(f"Enter Word #1")
            self.title.set_width(lv.SIZE.CONTENT)  # 1
            self.title.set_height(lv.SIZE.CONTENT)   # 1
            self.title.set_x(lv.pct(0))
            self.title.set_y(lv.pct(15))

            self.title.set_align(lv.ALIGN.TOP_MID)

            self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.title.set_style_text_font(font_PJSBOLD36, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.keyboard = CharacterKeyboard(self)
            self.keyboard.add_event_cb(self.on_ready, lv.EVENT.READY, None)
            self.num_th = 1
        def on_ready(self, target):
            global mnemonics, select_word_cnt
            input = self.keyboard.ta.get_text()
            if input == "" or self.num_th > select_word_cnt + 1:
                return
            # if wordlist.index(select) != -1:
            self.num_th += 1
            mnemonics.append(input)
            if self.num_th == select_word_cnt + 1:
                global mnemonic_str
                mnemonic_str = " ".join(mnemonics)
                if bip39.check(mnemonic_str):
                    save_mnemonics()
                    self.load_screen(WalletReady("You have successfully imported your wallet."), destory_self=True)
                else:
                    print(f"not valid mnemonic {' '.join(mnemonics)}")
                    mnemonics.clear()
                    return
            else:
                self.title.set_text(f"Enter Word #{self.num_th}")
                self.keyboard.ta.set_text("")
            # else:
            #     print(f"not in wordlist {select}")
            #     return
            print(f"on_ready == {input}")

class WalletReady(Screen):
    """Screen for the wallet ready"""
    def __init__(self, sub_title=""):
        if not hasattr(self, "_init"):
                self._init = True
        else:
            return
        super().__init__()
        self.title = lv.label(self)
        self.title.set_long_mode(lv.label.LONG.WRAP)
        self.title.set_text("Wallet is Ready")
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
        self.btn_label.set_text("Next")
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
        self.load_screen(PinTip())

class RecoveryFail(Screen):

    def __init__(self, sub_title="The recovery phrase you entered is invalid. Check your backup carefully and try again."):
        if not hasattr(self, "_init"):
                self._init = True
        else:
            return
        super().__init__()
        self.title = lv.label(self)
        self.title.set_long_mode(lv.label.LONG.WRAP)
        self.title.set_text("Invalid Recovery Phrase")
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
        self.btn_label.set_text("Try Again")
        self.btn_label.set_width(lv.SIZE.CONTENT)	# 1
        self.btn_label.set_height(lv.SIZE.CONTENT)   # 1
        self.btn_label.set_align( lv.ALIGN.CENTER)
        self.btn_label.set_style_text_font( font_PJSBOLD24, lv.PART.MAIN | lv.STATE.DEFAULT )

        self.icon = lv.img(self)
        self.icon.set_src(ui_images.ui_img_danger_png)
        self.icon.set_width(lv.SIZE.CONTENT)	# 1
        self.icon.set_height(lv.SIZE.CONTENT)   # 1
        self.icon.set_align(lv.ALIGN.CENTER)
        self.icon.set_x(lv.pct(0))
        self.icon.set_y(lv.pct(-30))
        self.icon.set_pivot(0,0)
        self.icon.set_angle(0)
        self.icon.set_zoom(256)
    def on_click(self, target):
        self.load_screen(Recovery(), destory_self=True)


def init_device(strength=128) -> list[str]:
    """
    Initialize the device
    :return: the mnemonic string
    """
    # wipe storage to make sure the device is in a clear state
    # storage.wipe()
    storage.reset()
    # generate internal entropy
    int_entropy = random.bytes(32)
    ext_entropy = random.bytes(32)

    def _compute_secret_from_entropy(
        int_entropy: bytes, ext_entropy: bytes, strength_in_bytes: int
    ) -> bytes:
        # combine internal and external entropy
        ehash = hashlib.sha256()
        ehash.update(int_entropy)
        ehash.update(ext_entropy)
        entropy = ehash.digest()
        # take a required number of bytes
        strength = strength_in_bytes // 8
        secret = entropy[:strength]
        return secret
    # For SLIP-39 this is the Encrypted Master Secret
    secret = _compute_secret_from_entropy(int_entropy, ext_entropy, strength)
    # in BIP-39 we store mnemonic string instead of the secret
    secret = bip39.from_data(secret).encode()
    print(f"secret========= {secret}")
    global mnemonic_str
    mnemonic_str = secret
    return secret.decode("utf-8").strip(" ").split(" ")

def save_mnemonics():
    # write settings and master secret into storage
    storage.device.set_passphrase_enabled(False)
    storage.device.store_mnemonic_secret(
        mnemonic_str,  # for SLIP-39, this is the EMS
        BackupType.Bip39,
        needs_backup=False,
        no_backup=False,
    )

def get_choices() -> list[str]:
    """
    Get the choices for the number of words
    :param mnemonic_str: mnemonic string
    :return: the choices
    """
    global mnemonics
    dummy_mnemonics = list(set(mnemonics))
    dummy_mnemonics.remove(mnemonics[check_index])
    random.shuffle(dummy_mnemonics)
    choices = [mnemonics[check_index]] + dummy_mnemonics[-2:]
    random.shuffle(choices)
    return choices
"""
wordlist = [
    "abandon",  "ability",  "able",     "about",    "above",    "absent",
    "absorb",   "abstract", "absurd",   "abuse",    "access",   "accident",
    "account",  "accuse",   "achieve",  "acid",     "acoustic", "acquire",
    "across",   "act",      "action",   "actor",    "actress",  "actual",
    "adapt",    "add",      "addict",   "address",  "adjust",   "admit",
    "adult",    "advance",  "advice",   "aerobic",  "affair",   "afford",
    "afraid",   "again",    "age",      "agent",    "agree",    "ahead",
    "aim",      "air",      "airport",  "aisle",    "alarm",    "album",
    "alcohol",  "alert",    "alien",    "all",      "alley",    "allow",
    "almost",   "alone",    "alpha",    "already",  "also",     "alter",
    "always",   "amateur",  "amazing",  "among",    "amount",   "amused",
    "analyst",  "anchor",   "ancient",  "anger",    "angle",    "angry",
    "animal",   "ankle",    "announce", "annual",   "another",  "answer",
    "antenna",  "antique",  "anxiety",  "any",      "apart",    "apology",
    "appear",   "apple",    "approve",  "april",    "arch",     "arctic",
    "area",     "arena",    "argue",    "arm",      "armed",    "armor",
    "army",     "around",   "arrange",  "arrest",   "arrive",   "arrow",
    "art",      "artefact", "artist",   "artwork",  "ask",      "aspect",
    "assault",  "asset",    "assist",   "assume",   "asthma",   "athlete",
    "atom",     "attack",   "attend",   "attitude", "attract",  "auction",
    "audit",    "august",   "aunt",     "author",   "auto",     "autumn",
    "average",  "avocado",  "avoid",    "awake",    "aware",    "away",
    "awesome",  "awful",    "awkward",  "axis",     "baby",     "bachelor",
    "bacon",    "badge",    "bag",      "balance",  "balcony",  "ball",
    "bamboo",   "banana",   "banner",   "bar",      "barely",   "bargain",
    "barrel",   "base",     "basic",    "basket",   "battle",   "beach",
    "bean",     "beauty",   "because",  "become",   "beef",     "before",
    "begin",    "behave",   "behind",   "believe",  "below",    "belt",
    "bench",    "benefit",  "best",     "betray",   "better",   "between",
    "beyond",   "bicycle",  "bid",      "bike",     "bind",     "biology",
    "bird",     "birth",    "bitter",   "black",    "blade",    "blame",
    "blanket",  "blast",    "bleak",    "bless",    "blind",    "blood",
    "blossom",  "blouse",   "blue",     "blur",     "blush",    "board",
    "boat",     "body",     "boil",     "bomb",     "bone",     "bonus",
    "book",     "boost",    "border",   "boring",   "borrow",   "boss",
    "bottom",   "bounce",   "box",      "boy",      "bracket",  "brain",
    "brand",    "brass",    "brave",    "bread",    "breeze",   "brick",
    "bridge",   "brief",    "bright",   "bring",    "brisk",    "broccoli",
    "broken",   "bronze",   "broom",    "brother",  "brown",    "brush",
    "bubble",   "buddy",    "budget",   "buffalo",  "build",    "bulb",
    "bulk",     "bullet",   "bundle",   "bunker",   "burden",   "burger",
    "burst",    "bus",      "business", "busy",     "butter",   "buyer",
    "buzz",     "cabbage",  "cabin",    "cable",    "cactus",   "cage",
    "cake",     "call",     "calm",     "camera",   "camp",     "can",
    "canal",    "cancel",   "candy",    "cannon",   "canoe",    "canvas",
    "canyon",   "capable",  "capital",  "captain",  "car",      "carbon",
    "card",     "cargo",    "carpet",   "carry",    "cart",     "case",
    "cash",     "casino",   "castle",   "casual",   "cat",      "catalog",
    "catch",    "category", "cattle",   "caught",   "cause",    "caution",
    "cave",     "ceiling",  "celery",   "cement",   "census",   "century",
    "cereal",   "certain",  "chair",    "chalk",    "champion", "change",
    "chaos",    "chapter",  "charge",   "chase",    "chat",     "cheap",
    "check",    "cheese",   "chef",     "cherry",   "chest",    "chicken",
    "chief",    "child",    "chimney",  "choice",   "choose",   "chronic",
    "chuckle",  "chunk",    "churn",    "cigar",    "cinnamon", "circle",
    "citizen",  "city",     "civil",    "claim",    "clap",     "clarify",
    "claw",     "clay",     "clean",    "clerk",    "clever",   "click",
    "client",   "cliff",    "climb",    "clinic",   "clip",     "clock",
    "clog",     "close",    "cloth",    "cloud",    "clown",    "club",
    "clump",    "cluster",  "clutch",   "coach",    "coast",    "coconut",
    "code",     "coffee",   "coil",     "coin",     "collect",  "color",
    "column",   "combine",  "come",     "comfort",  "comic",    "common",
    "company",  "concert",  "conduct",  "confirm",  "congress", "connect",
    "consider", "control",  "convince", "cook",     "cool",     "copper",
    "copy",     "coral",    "core",     "corn",     "correct",  "cost",
    "cotton",   "couch",    "country",  "couple",   "course",   "cousin",
    "cover",    "coyote",   "crack",    "cradle",   "craft",    "cram",
    "crane",    "crash",    "crater",   "crawl",    "crazy",    "cream",
    "credit",   "creek",    "crew",     "cricket",  "crime",    "crisp",
    "critic",   "crop",     "cross",    "crouch",   "crowd",    "crucial",
    "cruel",    "cruise",   "crumble",  "crunch",   "crush",    "cry",
    "crystal",  "cube",     "culture",  "cup",      "cupboard", "curious",
    "current",  "curtain",  "curve",    "cushion",  "custom",   "cute",
    "cycle",    "dad",      "damage",   "damp",     "dance",    "danger",
    "daring",   "dash",     "daughter", "dawn",     "day",      "deal",
    "debate",   "debris",   "decade",   "december", "decide",   "decline",
    "decorate", "decrease", "deer",     "defense",  "define",   "defy",
    "degree",   "delay",    "deliver",  "demand",   "demise",   "denial",
    "dentist",  "deny",     "depart",   "depend",   "deposit",  "depth",
    "deputy",   "derive",   "describe", "desert",   "design",   "desk",
    "despair",  "destroy",  "detail",   "detect",   "develop",  "device",
    "devote",   "diagram",  "dial",     "diamond",  "diary",    "dice",
    "diesel",   "diet",     "differ",   "digital",  "dignity",  "dilemma",
    "dinner",   "dinosaur", "direct",   "dirt",     "disagree", "discover",
    "disease",  "dish",     "dismiss",  "disorder", "display",  "distance",
    "divert",   "divide",   "divorce",  "dizzy",    "doctor",   "document",
    "dog",      "doll",     "dolphin",  "domain",   "donate",   "donkey",
    "donor",    "door",     "dose",     "double",   "dove",     "draft",
    "dragon",   "drama",    "drastic",  "draw",     "dream",    "dress",
    "drift",    "drill",    "drink",    "drip",     "drive",    "drop",
    "drum",     "dry",      "duck",     "dumb",     "dune",     "during",
    "dust",     "dutch",    "duty",     "dwarf",    "dynamic",  "eager",
    "eagle",    "early",    "earn",     "earth",    "easily",   "east",
    "easy",     "echo",     "ecology",  "economy",  "edge",     "edit",
    "educate",  "effort",   "egg",      "eight",    "either",   "elbow",
    "elder",    "electric", "elegant",  "element",  "elephant", "elevator",
    "elite",    "else",     "embark",   "embody",   "embrace",  "emerge",
    "emotion",  "employ",   "empower",  "empty",    "enable",   "enact",
    "end",      "endless",  "endorse",  "enemy",    "energy",   "enforce",
    "engage",   "engine",   "enhance",  "enjoy",    "enlist",   "enough",
    "enrich",   "enroll",   "ensure",   "enter",    "entire",   "entry",
    "envelope", "episode",  "equal",    "equip",    "era",      "erase",
    "erode",    "erosion",  "error",    "erupt",    "escape",   "essay",
    "essence",  "estate",   "eternal",  "ethics",   "evidence", "evil",
    "evoke",    "evolve",   "exact",    "example",  "excess",   "exchange",
    "excite",   "exclude",  "excuse",   "execute",  "exercise", "exhaust",
    "exhibit",  "exile",    "exist",    "exit",     "exotic",   "expand",
    "expect",   "expire",   "explain",  "expose",   "express",  "extend",
    "extra",    "eye",      "eyebrow",  "fabric",   "face",     "faculty",
    "fade",     "faint",    "faith",    "fall",     "false",    "fame",
    "family",   "famous",   "fan",      "fancy",    "fantasy",  "farm",
    "fashion",  "fat",      "fatal",    "father",   "fatigue",  "fault",
    "favorite", "feature",  "february", "federal",  "fee",      "feed",
    "feel",     "female",   "fence",    "festival", "fetch",    "fever",
    "few",      "fiber",    "fiction",  "field",    "figure",   "file",
    "film",     "filter",   "final",    "find",     "fine",     "finger",
    "finish",   "fire",     "firm",     "first",    "fiscal",   "fish",
    "fit",      "fitness",  "fix",      "flag",     "flame",    "flash",
    "flat",     "flavor",   "flee",     "flight",   "flip",     "float",
    "flock",    "floor",    "flower",   "fluid",    "flush",    "fly",
    "foam",     "focus",    "fog",      "foil",     "fold",     "follow",
    "food",     "foot",     "force",    "forest",   "forget",   "fork",
    "fortune",  "forum",    "forward",  "fossil",   "foster",   "found",
    "fox",      "fragile",  "frame",    "frequent", "fresh",    "friend",
    "fringe",   "frog",     "front",    "frost",    "frown",    "frozen",
    "fruit",    "fuel",     "fun",      "funny",    "furnace",  "fury",
    "future",   "gadget",   "gain",     "galaxy",   "gallery",  "game",
    "gap",      "garage",   "garbage",  "garden",   "garlic",   "garment",
    "gas",      "gasp",     "gate",     "gather",   "gauge",    "gaze",
    "general",  "genius",   "genre",    "gentle",   "genuine",  "gesture",
    "ghost",    "giant",    "gift",     "giggle",   "ginger",   "giraffe",
    "girl",     "give",     "glad",     "glance",   "glare",    "glass",
    "glide",    "glimpse",  "globe",    "gloom",    "glory",    "glove",
    "glow",     "glue",     "goat",     "goddess",  "gold",     "good",
    "goose",    "gorilla",  "gospel",   "gossip",   "govern",   "gown",
    "grab",     "grace",    "grain",    "grant",    "grape",    "grass",
    "gravity",  "great",    "green",    "grid",     "grief",    "grit",
    "grocery",  "group",    "grow",     "grunt",    "guard",    "guess",
    "guide",    "guilt",    "guitar",   "gun",      "gym",      "habit",
    "hair",     "half",     "hammer",   "hamster",  "hand",     "happy",
    "harbor",   "hard",     "harsh",    "harvest",  "hat",      "have",
    "hawk",     "hazard",   "head",     "health",   "heart",    "heavy",
    "hedgehog", "height",   "hello",    "helmet",   "help",     "hen",
    "hero",     "hidden",   "high",     "hill",     "hint",     "hip",
    "hire",     "history",  "hobby",    "hockey",   "hold",     "hole",
    "holiday",  "hollow",   "home",     "honey",    "hood",     "hope",
    "horn",     "horror",   "horse",    "hospital", "host",     "hotel",
    "hour",     "hover",    "hub",      "huge",     "human",    "humble",
    "humor",    "hundred",  "hungry",   "hunt",     "hurdle",   "hurry",
    "hurt",     "husband",  "hybrid",   "ice",      "icon",     "idea",
    "identify", "idle",     "ignore",   "ill",      "illegal",  "illness",
    "image",    "imitate",  "immense",  "immune",   "impact",   "impose",
    "improve",  "impulse",  "inch",     "include",  "income",   "increase",
    "index",    "indicate", "indoor",   "industry", "infant",   "inflict",
    "inform",   "inhale",   "inherit",  "initial",  "inject",   "injury",
    "inmate",   "inner",    "innocent", "input",    "inquiry",  "insane",
    "insect",   "inside",   "inspire",  "install",  "intact",   "interest",
    "into",     "invest",   "invite",   "involve",  "iron",     "island",
    "isolate",  "issue",    "item",     "ivory",    "jacket",   "jaguar",
    "jar",      "jazz",     "jealous",  "jeans",    "jelly",    "jewel",
    "job",      "join",     "joke",     "journey",  "joy",      "judge",
    "juice",    "jump",     "jungle",   "junior",   "junk",     "just",
    "kangaroo", "keen",     "keep",     "ketchup",  "key",      "kick",
    "kid",      "kidney",   "kind",     "kingdom",  "kiss",     "kit",
    "kitchen",  "kite",     "kitten",   "kiwi",     "knee",     "knife",
    "knock",    "know",     "lab",      "label",    "labor",    "ladder",
    "lady",     "lake",     "lamp",     "language", "laptop",   "large",
    "later",    "latin",    "laugh",    "laundry",  "lava",     "law",
    "lawn",     "lawsuit",  "layer",    "lazy",     "leader",   "leaf",
    "learn",    "leave",    "lecture",  "left",     "leg",      "legal",
    "legend",   "leisure",  "lemon",    "lend",     "length",   "lens",
    "leopard",  "lesson",   "letter",   "level",    "liar",     "liberty",
    "library",  "license",  "life",     "lift",     "light",    "like",
    "limb",     "limit",    "link",     "lion",     "liquid",   "list",
    "little",   "live",     "lizard",   "load",     "loan",     "lobster",
    "local",    "lock",     "logic",    "lonely",   "long",     "loop",
    "lottery",  "loud",     "lounge",   "love",     "loyal",    "lucky",
    "luggage",  "lumber",   "lunar",    "lunch",    "luxury",   "lyrics",
    "machine",  "mad",      "magic",    "magnet",   "maid",     "mail",
    "main",     "major",    "make",     "mammal",   "man",      "manage",
    "mandate",  "mango",    "mansion",  "manual",   "maple",    "marble",
    "march",    "margin",   "marine",   "market",   "marriage", "mask",
    "mass",     "master",   "match",    "material", "math",     "matrix",
    "matter",   "maximum",  "maze",     "meadow",   "mean",     "measure",
    "meat",     "mechanic", "medal",    "media",    "melody",   "melt",
    "member",   "memory",   "mention",  "menu",     "mercy",    "merge",
    "merit",    "merry",    "mesh",     "message",  "metal",    "method",
    "middle",   "midnight", "milk",     "million",  "mimic",    "mind",
    "minimum",  "minor",    "minute",   "miracle",  "mirror",   "misery",
    "miss",     "mistake",  "mix",      "mixed",    "mixture",  "mobile",
    "model",    "modify",   "mom",      "moment",   "monitor",  "monkey",
    "monster",  "month",    "moon",     "moral",    "more",     "morning",
    "mosquito", "mother",   "motion",   "motor",    "mountain", "mouse",
    "move",     "movie",    "much",     "muffin",   "mule",     "multiply",
    "muscle",   "museum",   "mushroom", "music",    "must",     "mutual",
    "myself",   "mystery",  "myth",     "naive",    "name",     "napkin",
    "narrow",   "nasty",    "nation",   "nature",   "near",     "neck",
    "need",     "negative", "neglect",  "neither",  "nephew",   "nerve",
    "nest",     "net",      "network",  "neutral",  "never",    "news",
    "next",     "nice",     "night",    "noble",    "noise",    "nominee",
    "noodle",   "normal",   "north",    "nose",     "notable",  "note",
    "nothing",  "notice",   "novel",    "now",      "nuclear",  "number",
    "nurse",    "nut",      "oak",      "obey",     "object",   "oblige",
    "obscure",  "observe",  "obtain",   "obvious",  "occur",    "ocean",
    "october",  "odor",     "off",      "offer",    "office",   "often",
    "oil",      "okay",     "old",      "olive",    "olympic",  "omit",
    "once",     "one",      "onion",    "online",   "only",     "open",
    "opera",    "opinion",  "oppose",   "option",   "orange",   "orbit",
    "orchard",  "order",    "ordinary", "organ",    "orient",   "original",
    "orphan",   "ostrich",  "other",    "outdoor",  "outer",    "output",
    "outside",  "oval",     "oven",     "over",     "own",      "owner",
    "oxygen",   "oyster",   "ozone",    "pact",     "paddle",   "page",
    "pair",     "palace",   "palm",     "panda",    "panel",    "panic",
    "panther",  "paper",    "parade",   "parent",   "park",     "parrot",
    "party",    "pass",     "patch",    "path",     "patient",  "patrol",
    "pattern",  "pause",    "pave",     "payment",  "peace",    "peanut",
    "pear",     "peasant",  "pelican",  "pen",      "penalty",  "pencil",
    "people",   "pepper",   "perfect",  "permit",   "person",   "pet",
    "phone",    "photo",    "phrase",   "physical", "piano",    "picnic",
    "picture",  "piece",    "pig",      "pigeon",   "pill",     "pilot",
    "pink",     "pioneer",  "pipe",     "pistol",   "pitch",    "pizza",
    "place",    "planet",   "plastic",  "plate",    "play",     "please",
    "pledge",   "pluck",    "plug",     "plunge",   "poem",     "poet",
    "point",    "polar",    "pole",     "police",   "pond",     "pony",
    "pool",     "popular",  "portion",  "position", "possible", "post",
    "potato",   "pottery",  "poverty",  "powder",   "power",    "practice",
    "praise",   "predict",  "prefer",   "prepare",  "present",  "pretty",
    "prevent",  "price",    "pride",    "primary",  "print",    "priority",
    "prison",   "private",  "prize",    "problem",  "process",  "produce",
    "profit",   "program",  "project",  "promote",  "proof",    "property",
    "prosper",  "protect",  "proud",    "provide",  "public",   "pudding",
    "pull",     "pulp",     "pulse",    "pumpkin",  "punch",    "pupil",
    "puppy",    "purchase", "purity",   "purpose",  "purse",    "push",
    "put",      "puzzle",   "pyramid",  "quality",  "quantum",  "quarter",
    "question", "quick",    "quit",     "quiz",     "quote",    "rabbit",
    "raccoon",  "race",     "rack",     "radar",    "radio",    "rail",
    "rain",     "raise",    "rally",    "ramp",     "ranch",    "random",
    "range",    "rapid",    "rare",     "rate",     "rather",   "raven",
    "raw",      "razor",    "ready",    "real",     "reason",   "rebel",
    "rebuild",  "recall",   "receive",  "recipe",   "record",   "recycle",
    "reduce",   "reflect",  "reform",   "refuse",   "region",   "regret",
    "regular",  "reject",   "relax",    "release",  "relief",   "rely",
    "remain",   "remember", "remind",   "remove",   "render",   "renew",
    "rent",     "reopen",   "repair",   "repeat",   "replace",  "report",
    "require",  "rescue",   "resemble", "resist",   "resource", "response",
    "result",   "retire",   "retreat",  "return",   "reunion",  "reveal",
    "review",   "reward",   "rhythm",   "rib",      "ribbon",   "rice",
    "rich",     "ride",     "ridge",    "rifle",    "right",    "rigid",
    "ring",     "riot",     "ripple",   "risk",     "ritual",   "rival",
    "river",    "road",     "roast",    "robot",    "robust",   "rocket",
    "romance",  "roof",     "rookie",   "room",     "rose",     "rotate",
    "rough",    "round",    "route",    "royal",    "rubber",   "rude",
    "rug",      "rule",     "run",      "runway",   "rural",    "sad",
    "saddle",   "sadness",  "safe",     "sail",     "salad",    "salmon",
    "salon",    "salt",     "salute",   "same",     "sample",   "sand",
    "satisfy",  "satoshi",  "sauce",    "sausage",  "save",     "say",
    "scale",    "scan",     "scare",    "scatter",  "scene",    "scheme",
    "school",   "science",  "scissors", "scorpion", "scout",    "scrap",
    "screen",   "script",   "scrub",    "sea",      "search",   "season",
    "seat",     "second",   "secret",   "section",  "security", "seed",
    "seek",     "segment",  "select",   "sell",     "seminar",  "senior",
    "sense",    "sentence", "series",   "service",  "session",  "settle",
    "setup",    "seven",    "shadow",   "shaft",    "shallow",  "share",
    "shed",     "shell",    "sheriff",  "shield",   "shift",    "shine",
    "ship",     "shiver",   "shock",    "shoe",     "shoot",    "shop",
    "short",    "shoulder", "shove",    "shrimp",   "shrug",    "shuffle",
    "shy",      "sibling",  "sick",     "side",     "siege",    "sight",
    "sign",     "silent",   "silk",     "silly",    "silver",   "similar",
    "simple",   "since",    "sing",     "siren",    "sister",   "situate",
    "six",      "size",     "skate",    "sketch",   "ski",      "skill",
    "skin",     "skirt",    "skull",    "slab",     "slam",     "sleep",
    "slender",  "slice",    "slide",    "slight",   "slim",     "slogan",
    "slot",     "slow",     "slush",    "small",    "smart",    "smile",
    "smoke",    "smooth",   "snack",    "snake",    "snap",     "sniff",
    "snow",     "soap",     "soccer",   "social",   "sock",     "soda",
    "soft",     "solar",    "soldier",  "solid",    "solution", "solve",
    "someone",  "song",     "soon",     "sorry",    "sort",     "soul",
    "sound",    "soup",     "source",   "south",    "space",    "spare",
    "spatial",  "spawn",    "speak",    "special",  "speed",    "spell",
    "spend",    "sphere",   "spice",    "spider",   "spike",    "spin",
    "spirit",   "split",    "spoil",    "sponsor",  "spoon",    "sport",
    "spot",     "spray",    "spread",   "spring",   "spy",      "square",
    "squeeze",  "squirrel", "stable",   "stadium",  "staff",    "stage",
    "stairs",   "stamp",    "stand",    "start",    "state",    "stay",
    "steak",    "steel",    "stem",     "step",     "stereo",   "stick",
    "still",    "sting",    "stock",    "stomach",  "stone",    "stool",
    "story",    "stove",    "strategy", "street",   "strike",   "strong",
    "struggle", "student",  "stuff",    "stumble",  "style",    "subject",
    "submit",   "subway",   "success",  "such",     "sudden",   "suffer",
    "sugar",    "suggest",  "suit",     "summer",   "sun",      "sunny",
    "sunset",   "super",    "supply",   "supreme",  "sure",     "surface",
    "surge",    "surprise", "surround", "survey",   "suspect",  "sustain",
    "swallow",  "swamp",    "swap",     "swarm",    "swear",    "sweet",
    "swift",    "swim",     "swing",    "switch",   "sword",    "symbol",
    "symptom",  "syrup",    "system",   "table",    "tackle",   "tag",
    "tail",     "talent",   "talk",     "tank",     "tape",     "target",
    "task",     "taste",    "tattoo",   "taxi",     "teach",    "team",
    "tell",     "ten",      "tenant",   "tennis",   "tent",     "term",
    "test",     "text",     "thank",    "that",     "theme",    "then",
    "theory",   "there",    "they",     "thing",    "this",     "thought",
    "three",    "thrive",   "throw",    "thumb",    "thunder",  "ticket",
    "tide",     "tiger",    "tilt",     "timber",   "time",     "tiny",
    "tip",      "tired",    "tissue",   "title",    "toast",    "tobacco",
    "today",    "toddler",  "toe",      "together", "toilet",   "token",
    "tomato",   "tomorrow", "tone",     "tongue",   "tonight",  "tool",
    "tooth",    "top",      "topic",    "topple",   "torch",    "tornado",
    "tortoise", "toss",     "total",    "tourist",  "toward",   "tower",
    "town",     "toy",      "track",    "trade",    "traffic",  "tragic",
    "train",    "transfer", "trap",     "trash",    "travel",   "tray",
    "treat",    "tree",     "trend",    "trial",    "tribe",    "trick",
    "trigger",  "trim",     "trip",     "trophy",   "trouble",  "truck",
    "true",     "truly",    "trumpet",  "trust",    "truth",    "try",
    "tube",     "tuition",  "tumble",   "tuna",     "tunnel",   "turkey",
    "turn",     "turtle",   "twelve",   "twenty",   "twice",    "twin",
    "twist",    "two",      "type",     "typical",  "ugly",     "umbrella",
    "unable",   "unaware",  "uncle",    "uncover",  "under",    "undo",
    "unfair",   "unfold",   "unhappy",  "uniform",  "unique",   "unit",
    "universe", "unknown",  "unlock",   "until",    "unusual",  "unveil",
    "update",   "upgrade",  "uphold",   "upon",     "upper",    "upset",
    "urban",    "urge",     "usage",    "use",      "used",     "useful",
    "useless",  "usual",    "utility",  "vacant",   "vacuum",   "vague",
    "valid",    "valley",   "valve",    "van",      "vanish",   "vapor",
    "various",  "vast",     "vault",    "vehicle",  "velvet",   "vendor",
    "venture",  "venue",    "verb",     "verify",   "version",  "very",
    "vessel",   "veteran",  "viable",   "vibrant",  "vicious",  "victory",
    "video",    "view",     "village",  "vintage",  "violin",   "virtual",
    "virus",    "visa",     "visit",    "visual",   "vital",    "vivid",
    "vocal",    "voice",    "void",     "volcano",  "volume",   "vote",
    "voyage",   "wage",     "wagon",    "wait",     "walk",     "wall",
    "walnut",   "want",     "warfare",  "warm",     "warrior",  "wash",
    "wasp",     "waste",    "water",    "wave",     "way",      "wealth",
    "weapon",   "wear",     "weasel",   "weather",  "web",      "wedding",
    "weekend",  "weird",    "welcome",  "west",     "wet",      "whale",
    "what",     "wheat",    "wheel",    "when",     "where",    "whip",
    "whisper",  "wide",     "width",    "wife",     "wild",     "will",
    "win",      "window",   "wine",     "wing",     "wink",     "winner",
    "winter",   "wire",     "wisdom",   "wise",     "wish",     "witness",
    "wolf",     "woman",    "wonder",   "wood",     "wool",     "word",
    "work",     "world",    "worry",    "worth",    "wrap",     "wreck",
    "wrestle",  "wrist",    "write",    "wrong",    "yard",     "year",
    "yellow",   "you",      "young",    "youth",    "zebra",    "zero",
    "zone",     "zoo" ]
"""

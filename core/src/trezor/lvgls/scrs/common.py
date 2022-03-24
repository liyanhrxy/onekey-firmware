
from . import *
class Screen(lv.obj):
    """Singleton screen object."""
    def __init__(self, prev_scr=None, **kwargs):
        super().__init__()
        self.prev_scr = prev_scr
        self.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_bg_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        # title
        if 'title' in kwargs:
            self.title = lv.label(self)
            self.title.set_long_mode(lv.label.LONG.WRAP)
            self.title.set_text(kwargs['title'])
            self.title.set_size(lv.SIZE.CONTENT, lv.SIZE.CONTENT)
            title_pos = kwargs.get('title_pos', (lv.pct(0), lv.pct(15)))
            self.title.set_pos(title_pos[0], title_pos[1])
            title_align = kwargs.get('title_align', lv.ALIGN.TOP_MID)
            self.title.set_align(title_align)
            self.title.set_style_text_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
            self.title.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
            self.title.set_style_text_font(font_PJSBOLD36, lv.PART.MAIN | lv.STATE.DEFAULT)

        # subtitle
        if 'subtitle' in kwargs:
            pass
        # roller
        if 'roller' in kwargs:
            pass
        # btn
        if 'btn' in kwargs:
            pass
        # nav_back
        if 'nav_back' in kwargs:
            self.nav_back = lv.imgbtn(self)
            self.nav_back.set_src(lv.imgbtn.STATE.RELEASED, None, ui_images.ui_img_1312433837, None)
            self.nav_back.set_size(48, 48)
            self.nav_back.set_pos(-192, -305)
            self.nav_back.add_flag(lv.imgbtn.FLAG.CLICKABLE)
            self.nav_back.set_align(lv.ALIGN.CENTER)
            self.nav_back.add_event_cb(self.eventhandler, lv.EVENT.CLICKED | lv.EVENT.PRESSED , None)

    # event callback
    def eventhandler(self, event_obj):
        event = event_obj.code
        target = event_obj.get_target()
        if event == lv.EVENT.CLICKED | lv.EVENT.PRESSED:
            if isinstance(target, lv.imgbtn):
                if target == self.nav_back:
                    self.load_screen(self.prev_scr, destory_self=True)
            else:
                if target == self.btn:
                    self.on_click(target)
        elif event == lv.EVENT.VALUE_CHANGED:
            self.on_value_changed(target)

    # click event callback
    def on_click(self, target):
        pass

    # value changed callback
    def on_value_changed(self, target):
        pass

    #NOTE:====================Functional Code Don't Edit========================

    def __new__(cls, pre_scr=None):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_screen(self, scr, destory_self=False):
        lv.scr_load_anim(scr, lv.SCR_LOAD_ANIM.OVER_LEFT, 200, 0, False)
        if destory_self:
            self.del_delayed(1000)
            del self.__class__._instance
            del self._init

    def __del__(self):
        try:
            self.delete()
            print('deleted in destructor')
        except BaseException as e:
            print(f"{e} in destructor")
    #NOTE:====================Functional Code Don't Edit========================

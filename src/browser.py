import tkinter

from url import URL

WIDTH = 800
HEIGHT = 600

HSTEP = 13
VSTEP = 18

SCROLL_STEP = 0

class Browser:
    def __init__(self) -> None:
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    # 第一次load url时, 展示相应的html内容
    def load(self, url: URL) -> None:
        body = url.request()
        text = lex(body)

        # 确定文本的layout
        #   即, 确定text 在page coordinate中的坐标
        self.layout: list[tuple[str, tuple[int, int]]] = layout(text)

        self.draw()

            
    def draw(self):
        self.canvas.delete('all')
        # 绘制text
        for c, (cursor_x, cursor_y) in self.layout:
            self.canvas.create_text(cursor_x, cursor_y, text=c)
        

    # browser 窗口 sroclldown事件 的 callback.
    def scrolldown(self, e): # type: ignore
        pass

# 获得http1.0 response中 entity-body部分(html版) 的文本内容, 只是简单地去除了tag.
#   http1.0 response的syntax 详见:https://www.w3.org/Protocols/HTTP/1.0/spec.html#Response
#   html syntax 详见: https://html.spec.whatwg.org/multipage/
def lex(body: str) -> str:
    text = ""

    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
    return text

def layout(text: str) -> list[tuple[str, tuple[int, int]]]:
    layout_list: list[tuple[str, tuple[int, int]]] = []

    c_cursor_x_last = -HSTEP
    c_cursor_y_last = 0

    for c in text:
        c_cursor_x_new = c_cursor_x_last + HSTEP
        c_cursor_y_new = c_cursor_y_last

        if c_cursor_x_new > WIDTH:
            c_cursor_x_new = 0
            c_cursor_y_new += VSTEP

        layout_list.append((c, (c_cursor_x_new, c_cursor_y_new)))

        c_cursor_x_last = c_cursor_x_new
        c_cursor_y_last = c_cursor_y_new

    return layout_list

if __name__ == "__main__":
    import sys
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
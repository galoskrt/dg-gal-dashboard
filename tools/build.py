# -*- coding: utf-8 -*-
"""Build the dashboard from src into index.html.

The page must stay one self-contained file: it is served from Pages and any
external request would be a second thing that can fail while Gal is trying to
see who to call. The font is the subset WOFF2 the funnel uses, and the salt is
the one the worker's key was derived against, so it is not a secret.
"""
import base64
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "src", "dash.html")
OUT = os.path.join(REPO, "index.html")
FONTS = os.path.join(REPO, "src", "fonts")

SALT = "8f1cdaf9bbd12314431c09a532e6f3af"


def b64(p):
    return base64.b64encode(io.open(p, "rb").read()).decode("ascii")


def build():
    css = ""
    for weight, name in ((400, "tlv-400.woff2"), (800, "tlv-800.woff2")):
        css += ("@font-face{font-family:'TelAviv';font-weight:%d;font-style:normal;"
                "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}\n"
                % (weight, b64(os.path.join(FONTS, name))))
    h = io.open(SRC, encoding="utf-8").read()
    h = h.replace("/*FONT*/", css).replace("/*SALT*/", SALT)
    io.open(OUT, "w", encoding="utf-8").write(h)
    print("dashboard built: %d KB" % (len(h.encode()) // 1024))


if __name__ == "__main__":
    build()

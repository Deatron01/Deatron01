"""Builds the animated Dea scenes shown next to each project in the profile README.

Each scene is Dea plus a prop from her room, drawn on a soft rounded card. Pixel art is scaled by a
whole number (SCALE) so it stays sharp; the card itself is drawn at full resolution so its corners
and shadows are smooth. Output is animated WebP at twice the display size, so it is also sharp on
high-density screens. The README shows each file at half its pixel size.

  python tools/make_scenes.py --dea ../dea --out assets/scenes
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

SCALE = 6                                   # device pixels per art pixel (3 CSS px on the page)
WALL_TOP, WALL_BOTTOM = (50, 43, 61), (37, 32, 45)
FLOOR_TOP, FLOOR_BOTTOM = (31, 27, 38), (26, 22, 32)
GLOW = (154, 132, 234)                      # Dea's violet
EDGE = (255, 255, 255, 18)

# Scene sizes in art pixels.
WIDE = (96, 72)
SMALL = (52, 64)

# name -> size, Dea (sprite, x of her left edge or None to centre), props [(sprite, x, sink)]
# `sink` moves a prop's base relative to Dea's floor line (negative = further back).
SCENES = {
    "hero":         (WIDE,  ("dea_wave", None),            [("monstera", 8, -4), ("andon", 76, -6)]),
    "vrtelemetry":  (WIDE,  ("dea_fidget_glasses", 62),    [("desk", 4, -6)]),
    "robot_bridge": (WIDE,  ("dea_tinker", 52),            [("claw_machine", 14, -4)]),
    "mimir":        (WIDE,  ("dea_learn", 60),             [("bookcase", 4, -8)]),
    "tinytribe":    (WIDE,  ("dea_game", 62),              [("tv_set", 2, -6)]),
    "aiworkgroup":  (WIDE,  ("act:bmo_dance", None),       [("pc_tower", 6, -6)]),
    "freetex":      (WIDE,  ("dea_write", 52),             [("side_table", 20, -4), ("andon", 74, -8)]),
    "phonemirror":  (SMALL, ("dea_scroll", None),          []),
    "adblocker":    (SMALL, ("dea_emote_disagree", None),  []),
    "photoshop":    (SMALL, ("dea_photo", None),           []),
    "zizgo":        (SMALL, ("dea_fidget_look", None),     []),
}

FLOOR = 10      # floor band height, art pixels


def load_anim(dea, name):
    m = json.loads((dea / "assets/manifest.json").read_text())
    if name.startswith("act:"):
        meta = next(a for a in m["acts"] if a["id"] == name[4:])
        sheet = Image.open(dea / f"assets/acts/{name[4:]}_day.png").convert("RGBA")
    else:
        meta = m["dea"][name]
        sheet = Image.open(dea / f"assets/dea/{name}.png").convert("RGBA")
    w, h, ms = meta["w"], meta["h"], meta["ms"]
    return [sheet.crop((i * w, 0, i * w + w, h)) for i in range(len(ms))], ms


def load_prop(dea, name):
    return Image.open(dea / f"assets/objects/{name}_day.png").convert("RGBA")


def vgradient(size, top, bottom):
    w, h = size
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        g.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return g.resize((w, h))


def card(size, shadows):
    """The smooth background: wall, floor, glow, soft contact shadows, rounded corners."""
    W, H = size[0] * SCALE, size[1] * SCALE
    floor_y = (size[1] - FLOOR) * SCALE
    bg = Image.new("RGBA", (W, H))
    bg.paste(vgradient((W, floor_y), WALL_TOP, WALL_BOTTOM), (0, 0))
    bg.paste(vgradient((W, H - floor_y), FLOOR_TOP, FLOOR_BOTTOM), (0, floor_y))

    glow = Image.new("L", (W, H), 0)
    cx = W // 2
    ImageDraw.Draw(glow).ellipse((cx - W * 0.32, H * 0.08, cx + W * 0.32, floor_y + H * 0.1), fill=46)
    glow = glow.filter(ImageFilter.GaussianBlur(W * 0.08))
    bg = Image.composite(Image.new("RGBA", (W, H), GLOW + (255,)), bg, glow)

    line = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(line).rectangle((0, floor_y - 2, W, floor_y), fill=(255, 255, 255, 14))
    bg.alpha_composite(line)

    shade = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(shade)
    for x0, x1, y in shadows:
        d.ellipse((x0 * SCALE, (y - 2.5) * SCALE, x1 * SCALE, (y + 1.5) * SCALE), fill=150)
    shade = shade.filter(ImageFilter.GaussianBlur(SCALE * 1.2))
    bg = Image.composite(Image.new("RGBA", (W, H), (12, 9, 16, 255)), bg, shade)

    # Rounded corners and a hairline edge, drawn 4x larger and scaled down so they are smooth.
    r, ss = 26, 4
    mask = Image.new("L", (W * ss, H * ss), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W * ss - 1, H * ss - 1), r * ss, fill=255)
    edge = Image.new("L", (W * ss, H * ss), 0)
    ImageDraw.Draw(edge).rounded_rectangle((0, 0, W * ss - 1, H * ss - 1), r * ss, outline=255, width=2 * ss)
    mask = mask.resize((W, H), Image.LANCZOS)
    edge = edge.resize((W, H), Image.LANCZOS)
    clear = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bg.alpha_composite(Image.composite(Image.new("RGBA", (W, H), EDGE), clear, edge))
    bg.putalpha(mask)
    return bg


def build(dea, size, dea_spec, props):
    w, h = size
    floor = h - FLOOR + 4                  # where feet touch, art pixels
    frames, ms = load_anim(dea, dea_spec[0])
    fw, fh = frames[0].size
    dx = (w - fw) // 2 if dea_spec[1] is None else dea_spec[1]
    placed, shadows = [], []
    for name, x, sink in props:
        p = load_prop(dea, name)
        placed.append((p, x, floor + sink - p.height))
        shadows.append((x + 1, x + p.width - 1, floor + sink))
    shadows.append((dx + fw * 0.2, dx + fw * 0.8, floor))
    bg = card(size, shadows)
    alpha = bg.getchannel("A")
    out = []
    for f in frames:
        art = Image.new("RGBA", size, (0, 0, 0, 0))
        for p, x, y in sorted(placed, key=lambda t: t[2] + t[0].height):
            art.alpha_composite(p, (x, y))
        art.alpha_composite(f, (dx, floor - fh))
        frame = bg.copy()
        frame.alpha_composite(art.resize((w * SCALE, h * SCALE), Image.NEAREST))
        frame.putalpha(alpha)
        out.append(frame)
    return out, ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dea", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    for name, (size, dea_spec, props) in SCENES.items():
        if a.only and name not in a.only:
            continue
        frames, ms = build(a.dea, size, dea_spec, props)
        path = a.out / f"{name}.webp"
        frames[0].save(path, save_all=True, append_images=frames[1:], duration=ms, loop=0,
                       lossless=True, method=4)
        print(f"{name:13} {frames[0].width}x{frames[0].height}  shows at "
              f"{frames[0].width // 2}x{frames[0].height // 2}  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()

"""Renders what Dea is doing right now, as an animated WebP for the GitHub profile.

Picks an activity from her daily schedule in Budapest time (asleep 0-6, cooking 6-7, reading 7-8,
at her PC 8-12 and 13-16, cooking or lunch 12-13, free time 16-24 with a seeded pick per hour),
draws one loop of it in her room with the day/night lighting, and adds a caption bar.

  python dea_now.py --assets assets --out dea.webp [--at 2026-10-21T14:30] [--scene reading]
"""
import argparse, json, math, random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageChops

TZ = ZoneInfo("Europe/Budapest")
SCALE = 2
BAR = 12                        # caption bar height (room pixels)
INK, MUTED, VIOLET, PANEL = (241, 235, 225), (169, 159, 181), (154, 132, 234), (38, 33, 44)

# ---------------------------------------------------------------- what she can be doing
# act: a furniture vignette (assets/acts); anim: her own animation at pos (feet), optional z.
SCENES = {
    "cook":      dict(act="cook", label="is making pancakes"),
    "fridge":    dict(act="fridge", hide=["fridge"], label="is raiding the fridge"),
    "desk":      dict(act="desk", hide=["gaming_chair"], label="is coding at her desk"),
    "arcade":    dict(act="arcade", hide=["arcade"], label="is playing the arcade"),
    "claw":      dict(act="claw", hide=["claw_machine"], label="is trying the claw machine"),
    "kotatsu":   dict(act="kotatsu", hide=["kotatsu", "cat", "candles", "zab_back"], label="is warm under the kotatsu"),
    "sleep":     dict(act="sleep", hide=["futon"], label="is asleep. shh."),
    "reading":   dict(act="reading", hide=["reading_nook", "mini_nook"], label="is reading in her nook"),
    "hug":       dict(act="hug", hide=["beanbag", "plush_bunny"], label="is hugging her bunny"),
    "pet_cat":   dict(act="pet_cat", hide=["cat"], label="is petting the cat"),
    "bmo_dance": dict(act="bmo_dance", hide=["bmo", "zab_back"], label="is dancing with BMO"),
    "moon":      dict(act="moon", label="is looking at the moon"),
    "tea":       dict(anim=["dea_tea"], pos=(118, 116), label="is sipping tea"),
    "eat":       dict(anim=["dea_eat"], pos=(118, 116), label="is having lunch at the island"),
    "game":      dict(anim=["dea_game"], pos=(252, 101), z=117, label="is gaming on the beanbag"),
    "laptop":    dict(anim=["dea_code", "dea_code_angry", "dea_code_good"], pos=(140, 136), label="is coding on her laptop"),
    "music":     dict(anim=["dea_music"], pos=(300, 150), label="is listening to music"),
    "water":     dict(anim=["dea_water"], pos=(152, 230), label="is watering the monstera"),
    "flower":    dict(anim=["dea_flower"], pos=(196, 84), label="is looking after her pansies"),
    "learn":     dict(anim=["dea_learn"], pos=(140, 136), label="is studying"),
    "write":     dict(anim=["dea_write"], pos=(216, 136), label="is writing in her journal"),
    "potion":    dict(anim=["dea_potion"], pos=(118, 102), label="is brewing something (probably tea)"),
    "scroll":    dict(anim=["dea_scroll"], pos=(320, 140), label="is scrolling her phone"),
}
# Her day, by hour (Budapest time): [start, end) -> what she may be doing, with weights.
FREE_TIME = dict(kotatsu=3, game=3, arcade=2, claw=2, hug=2, reading=2, pet_cat=2, bmo_dance=2, music=2,
                 laptop=1, learn=1, write=1, tea=2, potion=1, scroll=1, water=1, flower=1, moon=2)
SCHEDULE = [
    (0, 6, dict(sleep=1)),
    (6, 7, dict(cook=1)),
    (7, 8, dict(reading=1)),
    (8, 12, dict(desk=1)),
    (12, 13, dict(cook=1, eat=1)),
    (13, 16, dict(desk=1)),
    (16, 24, FREE_TIME),
]

def night_amount(h):
    """0 = day, 1 = night; dusk 18:30-20:00, dawn 6:00-7:00 (same as the app)."""
    if h >= 20 or h < 6: return 1.0
    if h >= 18.5: return (h - 18.5) / 1.5
    if h < 7: return 1 - (h - 6)
    return 0.0

def choose(now):
    h = now.hour + now.minute / 60
    options = dict(next(o for a, b, o in SCHEDULE if a <= h < b))
    dark = night_amount(h) > 0.5
    for k in (["water", "flower"] if dark else ["moon"]): options.pop(k, None)   # plants by day, moon by night
    rng = random.Random(now.strftime("%Y-%m-%d-%H"))
    return rng.choices(list(options), weights=list(options.values()))[0]

# ---------------------------------------------------------------- 3x5 pixel font
# Glyphs from pxl (github.com/crsolver/claude-pxl, MIT).
FONT = {
  "A": "###/#.#/###/#.#/#.#", "B": "##./#.#/##./#.#/##.", "C": "###/#../#../#../###",
  "D": "##./#.#/#.#/#.#/##.", "E": "###/#../##./#../###", "F": "###/#../##./#../#..",
  "G": "###/#../#.#/#.#/###", "H": "#.#/#.#/###/#.#/#.#", "I": "###/.#./.#./.#./###",
  "J": "..#/..#/..#/#.#/###", "K": "#.#/#.#/##./#.#/#.#", "L": "#../#../#../#../###",
  "M": "#.#/###/###/#.#/#.#", "N": "##./#.#/#.#/#.#/#.#", "O": "###/#.#/#.#/#.#/###",
  "P": "###/#.#/###/#../#..", "Q": "###/#.#/#.#/###/..#", "R": "##./#.#/##./#.#/#.#",
  "S": "###/#../###/..#/###", "T": "###/.#./.#./.#./.#.", "U": "#.#/#.#/#.#/#.#/###",
  "V": "#.#/#.#/#.#/#.#/.#.", "W": "#.#/#.#/###/###/#.#", "X": "#.#/#.#/.#./#.#/#.#",
  "Y": "#.#/#.#/###/.#./.#.", "Z": "###/..#/.#./#../###",
  "0": "###/#.#/#.#/#.#/###", "1": "##./.#./.#./.#./###", "2": "###/..#/###/#../###",
  "3": "###/..#/.##/..#/###", "4": "#.#/#.#/###/..#/..#", "5": "###/#../###/..#/###",
  "6": "###/#../###/#.#/###", "7": "###/..#/..#/.#./.#.", "8": "###/#.#/###/#.#/###",
  "9": "###/#.#/###/..#/###", " ": ".../.../.../.../...", ".": "././././#",
  ",": "../../../.#/#.", "!": "#/#/#/./#", "?": "###/..#/.##/.../.#.", ":": "./#/./#/.",
  "'": "#/#/././.", "-": ".../.../###/.../...", "(": ".#/#./#./#./.#", ")": "#./.#/.#/.#/#.",
}

def text_width(s):
    return sum(len(FONT.get(c.upper(), FONT["?"]).split("/")[0]) + 1 for c in s) - 1

def draw_text(img, x, y, s, color):
    px = img.load()
    for c in s:
        rows = FONT.get(c.upper(), FONT["?"]).split("/")
        for j, row in enumerate(rows):
            for i, k in enumerate(row):
                if k == "#": px[x + i, y + j] = color + (255,)
        x += len(rows[0]) + 1

# ---------------------------------------------------------------- drawing
class Room:
    def __init__(self, assets):
        self.a = Path(assets)
        self.m = json.loads((self.a / "manifest.json").read_text())
        self.objs = [dict(o, z=-1 if o.get("z") == "flat" else o.get("z", o["y"] + o["h"])) for o in self.m["objects"]]
        self.acts = {a["id"]: a for a in self.m["acts"]}
        self.cache = {}

    def img(self, rel):
        if rel not in self.cache: self.cache[rel] = Image.open(self.a / rel).convert("RGBA")
        return self.cache[rel]

    def cell(self, rel, i, w, h):
        return self.img(rel).crop((i * w, 0, i * w + w, h))

    def lit(self, sprite, x, y):
        """Multiply a free sprite by the night light map (as the app does)."""
        light = self.img("light_night.png").crop((x, y, x + sprite.width, y + sprite.height)).convert("RGB")
        rgb = ImageChops.multiply(sprite.convert("RGB"), light)
        rgb.putalpha(sprite.getchannel("A"))
        return rgb

    def frame(self, v, t, scene):
        out = self.img(f"bg_{v}.png").copy()
        hide = set(scene.get("hide", []))
        if "act" in scene:
            a = self.acts[scene["act"]]
            z = a["y"] + a["h"]
            def actor():
                out.alpha_composite(self.cell(f"acts/{a['id']}_{v}.png", frame_at(a["ms"], t), a["w"], a["h"]), (a["x"], a["y"]))
        else:
            name, local = anim_at(self.m["dea"], scene["anim"], t)
            d = self.m["dea"][name]
            x, y = round(scene["pos"][0] - d["w"] / 2), round(scene["pos"][1] - d["h"])
            z = scene.get("z", scene["pos"][1])
            def actor():
                spr = self.cell(f"dea/{name}.png", frame_at(d["ms"], local), d["w"], d["h"])
                out.alpha_composite(self.lit(spr, x, y) if v == "night" else spr, (x, y))
        front = []
        for o in self.objs:
            if o["id"] in hide: continue
            if o["z"] > z: front.append(o); continue
            self.obj(out, o, v, t)
        actor()
        for o in front: self.obj(out, o, v, t)
        return out

    def obj(self, out, o, v, t):
        f = frame_at(o.get("ms"), t) if o["frames"] > 1 else 0
        out.alpha_composite(self.cell(f"objects/{o['id']}_{v}.png", f, o["w"], o["h"]), (o["x"], o["y"]))

def frame_at(ms, t):
    if not ms or len(ms) < 2: return 0
    r = t % sum(ms)
    for i, m in enumerate(ms):
        if r < m: return i
        r -= m
    return len(ms) - 1

def anim_at(dea, names, t):
    """For a sequence of animations played one loop each: which one, and the time inside it."""
    total = sum(sum(dea[n]["ms"]) for n in names)
    r = t % total
    for n in names:
        span = sum(dea[n]["ms"])
        if r < span: return n, r
        r -= span
    return names[-1], 0

def timeline(room, scene):
    """Frame start times and durations for one loop of the scene (at least ~2.4 s)."""
    if "act" in scene: ms = list(room.acts[scene["act"]]["ms"] or [200])
    else: ms = [m for n in scene["anim"] for m in room.m["dea"][n]["ms"]]
    loops = max(1, math.ceil(2400 / sum(ms)))
    ms = ms * loops
    starts = [sum(ms[:i]) for i in range(len(ms))]
    return starts, ms

def render(assets, now, scene_id=None):
    room = Room(assets)
    sid = scene_id or choose(now)
    scene = SCENES[sid]
    n = night_amount(now.hour + now.minute / 60)
    caption = f"DEA {scene['label']}"
    stamp = f"{now:%H}:00 BUDAPEST"
    frames = []
    starts, ms = timeline(room, scene)
    for t in starts:
        if n <= 0: img = room.frame("day", t, scene)
        elif n >= 1: img = room.frame("night", t, scene)
        else: img = Image.blend(room.frame("day", t, scene), room.frame("night", t, scene), n)
        full = Image.new("RGBA", (img.width, img.height + BAR), PANEL + (255,))
        full.paste(img, (0, 0))
        y = img.height + (BAR - 5) // 2
        draw_text(full, 6, y, caption.upper(), INK)
        draw_text(full, full.width - 6 - text_width(stamp), y, stamp, VIOLET if n > 0.5 else MUTED)
        frames.append(full.resize((full.width * SCALE, full.height * SCALE), Image.NEAREST))
    return sid, frames, ms

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--assets", default="assets")
    ap.add_argument("--out", default="dist/dea.webp")
    ap.add_argument("--at", help="pretend it is this local Budapest time (ISO), for testing")
    ap.add_argument("--scene", choices=sorted(SCENES), help="force an activity, for testing")
    args = ap.parse_args()
    now = datetime.fromisoformat(args.at).replace(tzinfo=TZ) if args.at else datetime.now(TZ)
    sid, frames, ms = render(args.assets, now, args.scene)
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=ms, loop=0, lossless=True, method=4)
    print(f"{now:%Y-%m-%d %H:%M} {sid}: {len(frames)} frames, {out.stat().st_size // 1024} KB -> {out}")

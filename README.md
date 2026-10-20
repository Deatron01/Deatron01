# dea

Renderer behind the "Dea, right now" picture on the profile README.

`.github/workflows/dea.yml` on `main` checks out this branch every hour, runs

```bash
pip install pillow
python dea_now.py --assets assets --out dist/dea.webp
```

and publishes `dist/` to the `dea-output` branch. `assets/` holds the rendered layers of her
pixel-art home and her animations. Try a moment with `--at 2026-10-21T19:15` or `--scene reading`.

# GTA Trailer Parts – static site (Vercel)

Plain HTML/CSS/JS. No build step is needed on Vercel – `index.html` is in the repo root.

## Deploy
1. Upload every file in this folder to the **root** of your GitHub repo (so `index.html` sits at the top level, not inside another folder).
2. In Vercel: Import the repo. Framework Preset: **Other**. Build Command: leave empty. Output Directory: leave empty (root).
3. Deploy.

## Update content
Edit `data.json` (phone, address, hours, texts, systems, parts), then run `python3 build.py` and commit. Vercel redeploys automatically.
- Part photos: put the file in `assets/img/` and set `"image": "yourfile.jpg"` on the part (blank = uses the section image).
- Section photos: replace `assets/img/system-1.jpg` … `system-8.jpg` and `logo.png` with your originals.

## Notes
- The quote form opens the visitor's email app addressed to the email in `data.json`. For a real form that emails you directly, connect Formspree or similar.
- Search is client-side over the parts in `data.json`.

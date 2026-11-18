#!/usr/bin/env python3
"""Generates the static site from data.json.  Run:  python3 build.py
Edit data.json (text, phone, systems, parts), run the script, commit, and Vercel redeploys."""
import json, html, os, shutil
D = json.load(open('data.json', encoding='utf-8'))
S = D['site']; SYS = D['systems']
e = html.escape
ICON = {
 'pin':'<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>',
 'clock':'<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 'phone':'<path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8.1 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z"/>',
 'truck':'<path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
 'shield':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
 'dollar':'<path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>',
 'return':'<path d="M1 4v6h6"/><path d="M3.5 15a9 9 0 102.1-9.4L1 10"/>',
 'bag':'<path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 01-8 0"/>',
 'check':'<circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/>',
 'info':'<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>',
 'bolt':'<path d="M13 2L3 14h9l-1 8 10-12h-9z"/>'}
def ic(n): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICON[n]}</svg>'
tel = 'tel:' + ''.join(c for c in S['phone'] if c.isdigit() or c == '+')
two = lambda n: f'{int(n):02d}'
def write(path, content):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(content)

def head(title, desc, root):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:image" content="{root}assets/img/logo.png">
<link rel="icon" href="{root}assets/img/logo.png">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css"></head><body>'''

def top(root):
    drop = ''.join(f'<li><a href="{root}system/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SYS)
    return f'''<div class="announce">{ic("bolt")} {e(S["announce"])} <a href="{tel}">{e(S["announce_btn"])}</a></div>
<div class="infobar mono"><div class="wrap wide"><div><span>{ic("pin")} {e(S["address"])}</span><span>{ic("clock")} {e(S["hours"])}</span></div><div><span>{ic("phone")} <b>{e(S["phone_label"])}</b></span></div></div></div>
<header class="site-header"><div class="wrap wide">
<a class="brand" href="{root}"><span class="logo"><img src="{root}assets/img/logo.png" alt="GTA Trailer Parts"></span><span><span class="name"><i>GTA</i>Trailer Parts</span><small>{e(S["tagline"])}</small></span></a>
<nav class="nav" id="site-nav"><ul><li><a href="{root}">Home</a></li><li class="menu-item-has-children"><a href="{root}#catalog">Catalog</a><ul class="sub-menu">{drop}</ul></li><li><a href="{root}#why">Why GTA</a></li><li><a href="{root}#contact">Contact</a></li></ul>
<form class="hsearch" action="{root}search/" method="get"><input type="search" name="q" placeholder="Search part # or item..." aria-label="Search parts"></form>
<a class="btn dark nav-quote" href="{root}quote/">{ic("bag")} Quote</a><a class="btn" href="{tel}">{ic("phone")} {e(S["phone"])}</a></nav>
<button class="menu-toggle" aria-controls="site-nav" aria-expanded="false">Menu</button></div></header>'''

def foot(root):
    return f'''<footer class="site-footer"><div class="wrap wide"><div><b>{e(S["name"])}</b><br>{e(S["address"])}<br>{e(S["hours"])}</div>
<div><a href="{tel}">{e(S["phone"])}</a><br><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></div><div>&copy; 2026 GTA Trailer Parts &mdash; {e(S["trust"][0])} &middot; {e(S["trust"][2])} &middot; {e(S["trust"][3])}</div></div></footer>
<script src="{root}assets/js/main.js"></script></body></html>'''

def quote_url(root, p): return f'{root}quote/?part=' + html.escape(('#' + p['no'] + ' ' if p['no'] else '') + p['title']).replace(' ', '%20')

def card(p, s, root):
    img = f'{root}assets/img/' + (p['image'] or s['image'])
    tags = ''.join(f'<span>{e(t)}</span>' for t in p['tags'] if t)
    feats = ''.join(f'<li>{ic("check")}<span>{e(f)}</span></li>' for f in p['features'][:3] if f)
    spec = f'<figcaption class="spec">{e(p["spec"])}</figcaption>' if p['spec'] else ''
    return f'''<article class="pcard"><div class="ph"><span class="no mono">Part #{e(p["no"])}</span><h3 class="display">{e(p["title"])}</h3><span class="cvsa">{ic("info")} CVSA</span></div>
<figure class="pimg"><img src="{img}" alt="{e(p["title"])}" loading="lazy">{spec}</figure>
<div class="pbody"><p>{e(p["desc"])}</p><div class="tags">{tags}</div><ul class="feat">{feats}</ul><div class="pfoot"><a class="btn" href="{quote_url(root,p)}">{ic("bag")} Request Quote</a></div></div></article>'''

# ---- home ----
trust = ''.join(f'<div>{ic(i)} {e(t)}</div>' for i, t in zip(['truck','shield','dollar','return'], S['trust']))
cards = ''.join(f'''<a class="sys-card" href="system/{s["slug"]}/" style="--sc:{s["color"]}"><div class="sys-top"><b>{two(s["n"])}</b><span>{e(s["name"])}</span></div>
<div class="sys-img"><img src="assets/img/{s["image"]}" alt="{e(s["name"])}" loading="lazy"></div><div class="sys-body"><p>{e(s["desc"])}</p><span class="view">View Parts &rarr;</span></div></a>''' for s in SYS)
why = ''.join(f'<div><b>{two(i+1)}</b><h4>{e(t)}</h4><p>{e(d)}</p></div>' for i, (t, d) in enumerate(S['why']))
home = head(S['name'] + ' | Canada Commercial Trailer Parts', 'Commercial trailer parts distributor in Brampton, ON. Brake drums, air valves, leaf springs, hardware & CVSA certified parts.', '') + top('') + f'''
<div class="trust"><div class="wrap">{trust}</div></div>
<section class="sec" id="catalog"><div class="wrap"><div class="sec-head"><span class="eyebrow">The Catalog</span><h2>{e(S["cat_title"])}</h2><p>{e(S["cat_intro"])}</p></div><div class="sys-grid">{cards}</div></div></section>
<section class="sec why" id="why"><div class="wrap"><div class="sec-head"><span class="eyebrow">Why GTA</span><h2>{e(S["why_title"])}</h2><p>{e(S["why_intro"])}</p></div><div class="why-grid">{why}</div></div></section>
<section class="sec" id="contact"><div class="wrap"><div class="contact-grid"><div class="sec-head"><span class="eyebrow">Contact</span><h2>{e(S["contact_title"])}</h2><p>{e(S["contact_intro"])}</p>
<p style="margin-top:22px"><a class="btn lg" href="{tel}">{ic("phone")} {e(S["phone"])}</a> <a class="btn lg dark" style="color:var(--ink);border-color:var(--line)" href="quote/">Request a Quote</a></p></div>
<div class="cbox"><div class="row"><span>Address</span><div>{e(S["address"])}</div></div><div class="row"><span>Phone</span><div><a href="{tel}">{e(S["phone"])}</a></div></div><div class="row"><span>Email</span><div><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></div></div><div class="row"><span>Hours</span><div>{e(S["hours"])}</div></div></div></div></div></section>''' + foot('')
write('index.html', home)

# ---- system pages ----
for s in SYS:
    r = '../../'
    n = two(s['n'])
    body = head(f'{s["name"]} | {S["name"]}', s['desc'], r) + top(r) + f'''<div class="wrap wide"><div class="sec-hero"><div class="txt"><span class="pill">Section <em>{n}</em> &middot; {e(s["tagline"])}</span><h1>{e(s["name"])}</h1><p>{e(s["desc"])}</p>
<div class="facts"><span class="box">{len(s["parts"])} products in this section</span><span class="ok">{ic("check")} Brampton Warehouse Verified Stock</span></div></div>
<div class="img"><img src="{r}assets/img/{s["image"]}" alt="{e(s["name"])}"></div></div>
<div class="parts-head"><h2>Parts in Section {n}</h2><span class="mono">{len(s["parts"])} Items Listed</span></div>
<div class="part-grid">{"".join(card(p, s, r) for p in s["parts"])}</div></div>''' + foot(r)
    write(f'system/{s["slug"]}/index.html', body)

# ---- quote page (opens the visitor's email app, no backend needed) ----
r = '../'
write('quote/index.html', head('Request a Quote | ' + S['name'], 'Request a quote', r) + top(r) + f'''<div class="wrap"><div class="content"><h1>Request a Quote</h1>
<form class="qform" id="qf" data-to="{e(S["email"])}"><div><label>Name</label><input name="name" required></div><div><label>Email</label><input type="email" name="email" required></div>
<div><label>Phone</label><input name="phone"></div><div><label>Part / brand / quantity</label><input name="part" id="qpart" required></div>
<div><label>Notes (trailer make, VIN, delivery or pick-up)</label><textarea name="msg" rows="5"></textarea></div><div><button class="btn lg" type="submit">Send Request</button></div></form>
<p style="color:var(--grey);font-size:13px">Or call <a href="{tel}" style="color:var(--red);font-weight:700">{e(S["phone"])}</a>.</p></div></div>''' + foot(r))

# ---- search page (client side) ----
index = [{'t': p['title'], 'no': p['no'], 'd': p['desc'], 's': s['name'], 'u': f'system/{s["slug"]}/'} for s in SYS for p in s['parts']]
r = '../'
write('search/index.html', head('Search | ' + S['name'], 'Search parts', r) + top(r) + '''<div class="wrap wide"><div class="parts-head" style="margin-top:50px"><h2 id="st">Search</h2><span class="mono" id="sc"></span></div><div id="sr" class="part-grid" style="grid-template-columns:1fr"></div></div>''' + foot(r).replace('<script src=', f'<script>window.GTA_INDEX={json.dumps(index)};</script><script src=', 1))

# ---- js ----
write('assets/js/main.js', '''(function(){
var t=document.querySelector('.menu-toggle'),n=document.getElementById('site-nav');
if(t&&n)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
var p=new URLSearchParams(location.search);
var qp=document.getElementById('qpart');if(qp&&p.get('part'))qp.value=p.get('part');
var f=document.getElementById('qf');
if(f)f.addEventListener('submit',function(ev){ev.preventDefault();var d=new FormData(f);
 var b='Name: '+d.get('name')+'\\nEmail: '+d.get('email')+'\\nPhone: '+d.get('phone')+'\\nPart / brand / qty: '+d.get('part')+'\\n\\n'+d.get('msg');
 location.href='mailto:'+f.dataset.to+'?subject='+encodeURIComponent('Quote request from '+d.get('name'))+'&body='+encodeURIComponent(b);});
var sr=document.getElementById('sr');
if(sr&&window.GTA_INDEX){var q=(p.get('q')||'').toLowerCase().trim();
 document.getElementById('st').textContent='Search: \\u201c'+(p.get('q')||'')+'\\u201d';
 var r=window.GTA_INDEX.filter(function(i){return q&&(i.t+' '+i.no+' '+i.d+' '+i.s).toLowerCase().indexOf(q)>-1;});
 document.getElementById('sc').textContent=r.length+' results';
 sr.innerHTML=r.length?r.map(function(i){var a=document.createElement('a');return '<div class="cbox"><b>Part #'+i.no+'</b> &mdash; <a href="../'+i.u+'" style="color:#e4173a">'+i.t.replace(/</g,'&lt;')+'</a><br><small>'+i.s+'</small><p>'+i.d.replace(/</g,'&lt;')+'</p></div>';}).join(''):'<div class="cbox">No parts matched. Call us and we will source it.</div>';}
})();''')

write('vercel.json', json.dumps({"cleanUrls": True, "trailingSlash": True}, indent=2))
print('built', 1 + len(SYS) + 2, 'pages')

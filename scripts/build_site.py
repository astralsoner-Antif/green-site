#!/usr/bin/env python3
"""data/products.json → index.html + products/{code}.html + assets/site.css
Chopard型のカタログ構成 × GReENトーン。ja/en/zh 切替(localStorage)。
使い方: python3 scripts/build_site.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PS = json.load(open(os.path.join(ROOT, "data", "products.json")))
FONTFACE = open(os.path.join(ROOT, "scripts", "fontface.css")).read()

BEACON = '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "ac6972d86f8941fc8c3107604cccd97c"}\'></script>'

UI = {
  "brand":      {"ja": "GReEN", "en": "GReEN", "zh": "GReEN"},
  "contact":    {"ja": "お問い合わせ", "en": "Contact", "zh": "联系我们"},
  "jewellery":  {"ja": "ジュエリー", "en": "Jewellery", "zh": "珠宝"},
  "countFmt":   {"ja": "{shown} / {total} 点を表示中", "en": "Showing {shown} of {total}", "zh": "显示 {shown} / {total} 件"},
  "more":       {"ja": "さらに表示", "en": "Load more", "zh": "加载更多"},
  "new":        {"ja": "新作", "en": "New", "zh": "新品"},
  "introTitle": {"ja": "ジュエリー", "en": "Jewellery", "zh": "珠宝"},
  "introLead":  {"ja": "<span>ダイヤモンドから、</span><span>アコヤ・南洋・淡水のパールまで。</span><span>プラチナやゴールドの地金で仕立てた</span><span>ペンダント、ネックレス、ピアス、</span><span>リング、ブレスレットのコレクションを、</span><span>東京・東日本橋のショールームで</span><span>ご覧いただけます。</span>", "en": "<span>From diamonds to Akoya,</span> <span>South Sea and freshwater pearls —</span> <span>a collection of pendants, necklaces,</span> <span>earrings, rings and bracelets</span> <span>in platinum and gold,</span> <span>at our showroom in Higashi-Nihonbashi, Tokyo.</span>", "zh": "<span>从钻石到Akoya珍珠、</span><span>南洋珍珠与淡水珍珠——</span><span>铂金与K金打造的吊坠、项链、</span><span>耳环、戒指与手链系列，</span><span>尽在东京东日本桥陈列室。</span>"},
  "inquire":    {"ja": "お問い合わせ", "en": "Inquire", "zh": "咨询"},
  "inquireNote":{"ja": "在庫・ご来店のご相談は、品番を添えてご連絡ください。", "en": "For availability or a showroom visit, please contact us with the reference number.", "zh": "如需确认库存或预约到店，请附上产品编号与我们联系。"},
  "specH":      {"ja": "説明および仕様", "en": "Description & Specifications", "zh": "描述与规格"},
  "shopH":      {"ja": "ショールーム情報", "en": "Showroom", "zh": "陈列室信息"},
  "ref":        {"ja": "品番", "en": "Reference", "zh": "编号"},
  "type":       {"ja": "分類", "en": "Category", "zh": "类别"},
  "mat":        {"ja": "地金素材", "en": "Material", "zh": "材质"},
  "carat":      {"ja": "総カラット", "en": "Total carat", "zh": "总克拉"},
  "price":      {"ja": "価格（税込）", "en": "Price (tax incl.)", "zh": "价格（含税）"},
  "photoNote":  {"ja": "撮影環境により、実物と色味が異なる場合があります。", "en": "Colours may differ slightly from the actual piece due to photography conditions.", "zh": "因拍摄环境，实物颜色可能略有差异。"},
  "reco":       {"ja": "こちらもおすすめです", "en": "You may also like", "zh": "您可能还喜欢"},
  "coShop":     {"ja": "名称", "en": "Name", "zh": "名称"},
  "coAddr":     {"ja": "所在地", "en": "Address", "zh": "地址"},
  "coAddrV":    {"ja": "〒103-0004 東京都中央区東日本橋2丁目11-5 邇邇藝ビル 2F", "en": "Ninigi Bldg. 2F, 2-11-5 Higashi-Nihonbashi, Chuo-ku, Tokyo 103-0004", "zh": "东京都中央区东日本桥2丁目11-5 邇邇藝大厦2F 〒103-0004"},
  "coOp":       {"ja": "運営会社", "en": "Operated by", "zh": "运营公司"},
  "coOpV":      {"ja": "株式会社キュムラス", "en": "Cumulus Inc.", "zh": "Cumulus株式会社"},
  "coRep":      {"ja": "代表者", "en": "Representative", "zh": "代表人"},
  "coRepV":     {"ja": "原 孝之", "en": "Takayuki Hara", "zh": "原孝之"},
  "coCap":      {"ja": "資本金", "en": "Capital", "zh": "注册资本"},
  "coCapV":     {"ja": "1,000万円", "en": "JPY 10,000,000", "zh": "1,000万日元"},
  "coBiz":      {"ja": "事業内容", "en": "Business", "zh": "业务内容"},
  "coBizV":     {"ja": "ジュエリーの販売・ライブコマース事業", "en": "Jewellery retail and live commerce", "zh": "珠宝销售与直播电商"},
  "coContact":  {"ja": "お問い合わせ", "en": "Contact", "zh": "联系方式"},
  "backAll":    {"ja": "ジュエリー一覧", "en": "All jewellery", "zh": "全部珠宝"},
}

# 大分類(メインナビ・Chopardのウォッチ/ジュエリー/アクセサリーに相当)
NAVS = [
  ("all",      {"ja": "すべてのジュエリー", "en": "All Jewellery", "zh": "全部珠宝"}),
  ("ring",     {"ja": "リング", "en": "Rings", "zh": "戒指"}),
  ("earrings", {"ja": "ピアス", "en": "Earrings", "zh": "耳环"}),
  ("pendant",  {"ja": "ペンダント", "en": "Pendants", "zh": "吊坠"}),
  ("necklace", {"ja": "ネックレス", "en": "Necklaces", "zh": "项链"}),
  ("bracelet", {"ja": "ブレスレット", "en": "Bracelets", "zh": "手链"}),
]

# 小分類(コレクションチップ・Chopardのハッピーダイヤモンド等に相当=素材)
CHIPS = [
  ("all",   {"ja": "すべて", "en": "All", "zh": "全部"}),
  ("new",   {"ja": "新作", "en": "New", "zh": "新品"}),
  ("high",  {"ja": "ハイジュエリー", "en": "High Jewellery", "zh": "高级珠宝"}),
  ("dia",   {"ja": "ダイヤモンド", "en": "Diamonds", "zh": "钻石"}),
  ("pearl", {"ja": "パール", "en": "Pearls", "zh": "珍珠"}),
]

def yen(p):
    return "¥ {:,}".format(int(p)) if p else ""

def price_disp(p):
    s = yen(p["price"])
    if p.get("price_max"):
        s += " – " + yen(p["price_max"])
    return s

CSS = FONTFACE + """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --paper: #fefefe; --ink: #101513; --emerald: #0f6b52; --emerald-deep: #0b3d2f;
  --gold: #c9b37e; --muted: #7d8a83; --hairline: rgba(16,21,19,0.12); --tile: #f5f4f2;
  --serif: "Hiragino Mincho ProN", "Yu Mincho", "Songti SC", "Noto Serif JP", Palatino, Georgia, serif;
  --sans: "Hiragino Kaku Gothic ProN", "PingFang SC", -apple-system, "Helvetica Neue", Arial, sans-serif;
  --display: "Shippori Mincho", "Hiragino Mincho ProN", "Yu Mincho", "Songti SC", serif;
}
html { -webkit-text-size-adjust: 100%; }
body { background: var(--paper); color: var(--ink); font-family: var(--serif); line-height: 1.7; }
a { color: inherit; text-decoration: none; }
img { max-width: 100%; }

/* ---- top bar ---- */
.topbar { display: flex; justify-content: space-between; align-items: center;
  padding: 9px 20px; border-bottom: 1px solid var(--hairline);
  font-family: var(--sans); font-size: 11px; letter-spacing: 0.08em; color: var(--muted); }
.topbar a:hover { color: var(--emerald-deep); }
.langs { display: flex; gap: 14px; }
.langs button { background: none; border: none; cursor: pointer; font: inherit;
  color: var(--muted); letter-spacing: 0.08em; padding: 0; }
.langs button.on { color: var(--emerald-deep); border-bottom: 1px solid var(--emerald-deep); }

/* ---- brand bar ---- */
.brandbar { display: flex; justify-content: center; align-items: center;
  padding: 22px 20px 18px; border-bottom: 1px solid var(--hairline); background: var(--paper); }
.brandbar img { height: 56px; width: auto; display: block; }
@media (max-width: 700px) { .brandbar img { height: 44px; } .brandbar { padding: 16px 16px 13px; } }

/* ---- main nav (大分類) ---- */
.mainnav { display: flex; justify-content: center; gap: 34px; overflow-x: auto; scrollbar-width: none;
  padding: 15px 20px 13px; border-bottom: 1px solid var(--hairline); background: var(--paper); }
.mainnav::-webkit-scrollbar { display: none; }
.mainnav button { flex: 0 0 auto; background: none; border: none; cursor: pointer;
  font-family: var(--sans); font-size: 12px; letter-spacing: 0.18em; color: var(--ink);
  padding: 2px 0; border-bottom: 1px solid transparent; white-space: nowrap; }
.mainnav button:hover { color: var(--emerald-deep); }
.mainnav button.on { color: var(--emerald-deep); border-bottom-color: var(--emerald-deep); }
@media (max-width: 760px) { .mainnav { gap: 22px; justify-content: flex-start; } }

/* ---- listing intro (カテゴリ紹介パース) ---- */
.intro { text-align: center; padding: 46px 24px 10px; }
.intro .eyebrow { font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.34em; color: var(--gold); margin-bottom: 14px; }
.intro h1 { font-family: var(--display); font-weight: 600; font-size: 30px; letter-spacing: 0.22em; line-height: 1.6; }
.intro .lead { font-family: var(--serif); font-size: 13.5px; letter-spacing: 0.06em; line-height: 2.1;
  color: var(--ink); max-width: 640px; margin: 18px auto 0; }
.intro .lead span { display: inline-block; }
@media (max-width: 700px) { .intro h1 { font-size: 23px; } .intro { padding-top: 34px; }
  .intro .lead { font-size: 12.5px; } }

/* ---- chips ---- */
.chipswrap { position: sticky; top: 0; z-index: 30; background: var(--paper);
  border-bottom: 1px solid var(--hairline); }
.chips { display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none;
  padding: 14px 20px; max-width: 1380px; margin: 0 auto; }
.chips::-webkit-scrollbar { display: none; }
.chip { flex: 0 0 auto; font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.14em;
  padding: 7px 16px; border: 1px solid var(--hairline); border-radius: 999px;
  background: none; cursor: pointer; color: var(--ink); white-space: nowrap; }
.chip.on { background: var(--emerald-deep); border-color: var(--emerald-deep); color: #fff; }

/* ---- grid ---- */
.count { font-family: var(--sans); font-size: 11px; letter-spacing: 0.18em; color: var(--muted);
  text-align: center; padding: 26px 20px 4px; }
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 34px 22px;
  max-width: 1380px; margin: 0 auto; padding: 22px 20px 10px; }
@media (max-width: 1100px) { .grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 760px)  { .grid { grid-template-columns: repeat(2, 1fr); gap: 26px 12px; padding: 18px 12px 6px; } }
.card { display: block; }
.card .tile { position: relative; background: var(--tile); aspect-ratio: 1 / 1;
  display: flex; align-items: center; justify-content: center; overflow: hidden; }
.card .tile img { width: 86%; height: 86%; object-fit: contain; mix-blend-mode: multiply;
  transition: transform 0.5s ease; }
.card:hover .tile img { transform: scale(1.045); }
.badge { position: absolute; top: 10px; left: 12px; font-family: var(--sans);
  font-size: 10px; letter-spacing: 0.22em; color: var(--emerald-deep); }
.card .nm { font-family: var(--display); font-size: 14px; font-weight: 600;
  letter-spacing: 0.08em; line-height: 1.6; margin: 13px 2px 0;
  word-break: keep-all; overflow-wrap: anywhere; }
.card .sp { font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.1em;
  color: var(--muted); margin: 3px 2px 0; line-height: 1.6;
  word-break: keep-all; overflow-wrap: anywhere; }
.card .pr { font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.06em;
  margin: 6px 2px 0; font-variant-numeric: tabular-nums; }
.morewrap { text-align: center; padding: 30px 20px 64px; }
.morebtn { font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.24em;
  padding: 13px 44px; border: 1px solid var(--emerald-deep); color: var(--emerald-deep);
  background: none; cursor: pointer; }
.morebtn:hover { background: var(--emerald-deep); color: #fff; }

/* ---- PDP ---- */
.crumbs { font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.14em; color: var(--muted);
  max-width: 1380px; margin: 0 auto; padding: 16px 20px 0; }
.crumbs a:hover { color: var(--emerald-deep); }
.pdp { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); gap: 48px;
  max-width: 1380px; margin: 0 auto; padding: 22px 20px 30px; align-items: start; }
@media (max-width: 900px) { .pdp { grid-template-columns: 1fr; gap: 26px; } }
.pdp .tile { background: var(--tile); aspect-ratio: 1 / 1;
  display: flex; align-items: center; justify-content: center; position: sticky; top: 76px; }
@media (max-width: 900px) { .pdp .tile { position: relative; top: 0; } }
.pdp .tile img { width: 82%; height: 82%; object-fit: contain; mix-blend-mode: multiply; }
.pdp .badge { top: 14px; left: 16px; }
.pinfo .ref { font-family: var(--sans); font-size: 10px; letter-spacing: 0.26em; color: var(--muted); margin-bottom: 12px; }
.pinfo h1 { font-family: var(--display); font-size: 26px; font-weight: 600;
  letter-spacing: 0.1em; line-height: 1.7; text-wrap: balance;
  word-break: keep-all; overflow-wrap: anywhere; }
@media (max-width: 700px) { .pinfo h1 { font-size: 21px; } }
.pinfo .spec { font-family: var(--sans); font-size: 12px; letter-spacing: 0.14em;
  color: var(--emerald-deep); margin-top: 10px; line-height: 1.9;
  word-break: keep-all; overflow-wrap: anywhere; }
.pinfo .price { font-family: var(--sans); font-size: 19px; letter-spacing: 0.04em;
  margin-top: 22px; font-variant-numeric: tabular-nums; }
.pinfo .cta { display: block; text-align: center; font-family: var(--sans); font-size: 12px;
  letter-spacing: 0.28em; padding: 16px 10px; margin-top: 26px;
  background: var(--emerald-deep); color: #fff; }
.pinfo .cta:hover { background: var(--emerald); }
.pinfo .ctanote { font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.06em;
  color: var(--muted); margin-top: 10px; line-height: 1.9; }
.acc { border-top: 1px solid var(--hairline); margin-top: 30px; }
.acc details { border-bottom: 1px solid var(--hairline); }
.acc summary { font-family: var(--sans); font-size: 12px; letter-spacing: 0.2em;
  padding: 17px 2px; cursor: pointer; list-style: none; display: flex; justify-content: space-between; }
.acc summary::-webkit-details-marker { display: none; }
.acc summary::after { content: "+"; color: var(--muted); font-size: 14px; }
.acc details[open] summary::after { content: "−"; }
.acc .accbody { padding: 2px 2px 20px; }
.spectable { width: 100%; border-collapse: collapse; }
.spectable th, .spectable td { font-size: 12px; text-align: left; padding: 7px 0;
  vertical-align: top; font-weight: normal; }
.spectable th { font-family: var(--sans); letter-spacing: 0.12em; color: var(--muted); width: 38%; }
.spectable td { font-family: var(--sans); letter-spacing: 0.05em; }
.note { font-family: var(--sans); font-size: 10.5px; color: var(--muted);
  letter-spacing: 0.04em; margin-top: 12px; line-height: 1.9; }

/* ---- recommendations ---- */
.reco { max-width: 1380px; margin: 0 auto; padding: 26px 20px 60px; }
.reco h2 { font-family: var(--display); font-size: 18px; font-weight: 600;
  letter-spacing: 0.16em; text-align: center; margin-bottom: 24px; }
.recorow { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(180px, 1fr);
  gap: 18px; overflow-x: auto; scrollbar-width: none; padding-bottom: 6px; }
.recorow::-webkit-scrollbar { display: none; }

/* ---- shop section / footer ---- */
.shop { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: center;
  max-width: 1180px; margin: 0 auto; padding: 40px 24px 70px; border-top: 1px solid var(--hairline); }
@media (max-width: 800px) { .shop { grid-template-columns: 1fr; gap: 24px; padding: 32px 18px 50px; } }
.shop .photo img { width: 100%; display: block; }
.shop .eyebrow { font-family: var(--sans); font-size: 10.5px; letter-spacing: 0.34em; color: var(--gold); margin-bottom: 10px; }
.shop h2 { font-family: var(--display); font-size: 20px; font-weight: 600; letter-spacing: 0.14em; margin-bottom: 16px; }
.profile div { display: grid; grid-template-columns: 108px 1fr; gap: 12px;
  padding: 8px 0; border-bottom: 1px solid var(--hairline); }
.profile dt { font-family: var(--sans); font-size: 11px; letter-spacing: 0.12em; color: var(--muted); padding-top: 2px; }
.profile dd { font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.04em; }
footer { text-align: center; padding: 34px 20px 44px; border-top: 1px solid var(--hairline); }
footer .mark { font-family: Palatino, Georgia, serif; font-size: 17px; letter-spacing: 0.3em; color: var(--emerald-deep); }
footer p:last-child { font-family: var(--sans); font-size: 10px; letter-spacing: 0.18em; color: var(--muted); margin-top: 8px; }
"""

JS = """
(function () {
  var LANGS = ["ja", "en", "zh"];
  function getLang() {
    try { var v = localStorage.getItem("green-lang"); if (LANGS.indexOf(v) >= 0) return v; } catch (e) {}
    return "ja";
  }
  window.GREEN_LANG = getLang();
  window.setLang = function (l) {
    if (LANGS.indexOf(l) < 0) return;
    window.GREEN_LANG = l;
    try { localStorage.setItem("green-lang", l); } catch (e) {}
    apply();
  };
  function apply() {
    var l = window.GREEN_LANG;
    document.documentElement.lang = l === "zh" ? "zh-Hans" : l;
    document.querySelectorAll("[data-i]").forEach(function (el) {
      var d = el.getAttribute("data-" + l);
      if (d !== null) el.innerHTML = d;
    });
    document.querySelectorAll(".langs button").forEach(function (b) {
      b.classList.toggle("on", b.getAttribute("data-l") === l);
    });
    if (window.onLangChange) window.onLangChange(l);
  }
  document.addEventListener("DOMContentLoaded", apply);
})();
"""

def lang_buttons():
    return ('<div class="langs">'
            '<button data-l="ja" onclick="setLang(\'ja\')">日本語</button>'
            '<button data-l="en" onclick="setLang(\'en\')">English</button>'
            '<button data-l="zh" onclick="setLang(\'zh\')">简体中文</button></div>')

def tri(key):
    u = UI[key]
    return ('data-i data-ja="%s" data-en="%s" data-zh="%s"' %
            (html.escape(u["ja"], quote=True), html.escape(u["en"], quote=True), html.escape(u["zh"], quote=True)))

def head(title, desc, depth, og_img=None):
    p = "../" * depth
    og = ('<meta property="og:image" content="https://cumulus2026.com/%s">' % og_img) if og_img else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{og}
<link rel="icon" href="{p}img/logo.png">
<link rel="stylesheet" href="{p}assets/site.css">
<script src="{p}assets/site.js"></script>
</head>
<body>
"""

def topbars(depth):
    p = "../" * depth
    return f"""<div class="topbar">
  <a href="mailto:info@cumulus2026.com" {tri("contact")}>お問い合わせ</a>
  {lang_buttons()}
</div>
<div class="brandbar"><a href="{p}index.html"><img src="{p}img/logo-bar.png" alt="GReEN"></a></div>
"""

def shop_section(depth):
    p = "../" * depth
    # 運営会社・代表者・資本金・事業内容は非表示(2026-08-13 Koki指示。後日リーガル欄へ)
    rows = [("coShop", '<dd data-i data-ja="GReEN" data-en="GReEN" data-zh="GReEN">GReEN</dd>'),
            ("coAddr", f'<dd {tri("coAddrV")}>{UI["coAddrV"]["ja"]}</dd>'),
            ("coContact", '<dd>info@cumulus2026.com</dd>')]
    dl = "".join(f'<div><dt {tri(k)}>{UI[k]["ja"]}</dt>{dd}</div>' for k, dd in rows)
    return f"""<section class="shop">
  <div class="photo"><img src="{p}img/hero.jpg" alt="GReEN showroom" loading="lazy"></div>
  <div>
    <p class="eyebrow">Information</p>
    <h2 {tri("shopH")}>{UI["shopH"]["ja"]}</h2>
    <dl class="profile">{dl}</dl>
  </div>
</section>
"""

FOOTER = """<footer>
  <p class="mark">GReEN</p>
  <p>© 2026 GReEN — CUMULUS INC.</p>
</footer>
"""

# ---------------- listing ----------------
def build_index():
    items = []
    for p in PS:
        items.append({
            "c": p["code"], "n": p["names"], "s": p["spec"], "p": price_disp(p),
            "g": p["group"], "gem": p["gem"], "new": p["new"], "high": p["high"],
        })
    chips_html = "".join(
        '<button class="chip%s" data-f="%s" data-i data-ja="%s" data-en="%s" data-zh="%s">%s</button>' %
        (" on" if key == "all" else "", key, c["ja"], c["en"], c["zh"], c["ja"])
        for key, c in CHIPS)
    nav_html = "".join(
        '<button data-g="%s" class="%s" data-i data-ja="%s" data-en="%s" data-zh="%s">%s</button>' %
        (key, "on" if key == "all" else "", c["ja"], c["en"], c["zh"], c["ja"])
        for key, c in NAVS)
    doc = head("GReEN — ジュエリーコレクション | 東京・東日本橋",
               "GReEN 東京・東日本橋のジュエリーショールーム。ダイヤモンド・パールを中心とした全コレクション。", 0)
    doc += topbars(0)
    doc += f"""<nav class="mainnav" id="mainnav">{nav_html}</nav>
<section class="intro">
  <p class="eyebrow">HIGASHI-NIHONBASHI · TOKYO</p>
  <h1 {tri("introTitle")}>{UI["introTitle"]["ja"]}</h1>
  <p class="lead" {tri("introLead")}>{UI["introLead"]["ja"]}</p>
</section>
<div class="chipswrap"><div class="chips">{chips_html}</div></div>
<p class="count" id="count"></p>
<div class="grid" id="grid"></div>
<div class="morewrap"><button class="morebtn" id="more" {tri("more")}>{UI["more"]["ja"]}</button></div>
"""
    doc += shop_section(0)
    doc += FOOTER
    doc += "<script>var PRODUCTS = %s;</script>" % json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    doc += """<script>
(function () {
  var PAGE = 24, shown = PAGE, cat = "all", filter = "all";
  var grid = document.getElementById("grid"), count = document.getElementById("count"),
      more = document.getElementById("more");
  var NEW = {ja: "新作", en: "New", zh: "新品"};
  var FMT = {ja: "{total} 点中 {shown} 点を表示中", en: "Showing {shown} of {total}", zh: "显示 {shown} / {total} 件"};
  function match(p) {
    if (cat !== "all" && p.g !== cat) return false;
    if (filter === "all") return true;
    if (filter === "new") return p.new;
    if (filter === "high") return p.high;
    return p.gem === filter;
  }
  function render() {
    var l = window.GREEN_LANG || "ja";
    var list = PRODUCTS.filter(match);
    var vis = list.slice(0, shown);
    grid.innerHTML = vis.map(function (p) {
      return '<a class="card" href="products/' + encodeURIComponent(p.c) + '.html">' +
        '<div class="tile">' + (p.new ? '<span class="badge">' + NEW[l] + "</span>" : "") +
        '<img src="img/products/t/' + encodeURIComponent(p.c) + '.jpg" alt="' + p.n[l] + '" loading="lazy"></div>' +
        '<p class="nm">' + p.n[l] + '</p><p class="sp">' + p.s[l] + '</p><p class="pr">' + p.p + "</p></a>";
    }).join("");
    count.textContent = FMT[l].replace("{shown}", vis.length).replace("{total}", list.length);
    more.style.display = list.length > shown ? "" : "none";
  }
  function toTop() {
    window.scrollTo({top: document.querySelector(".chipswrap").offsetTop - 60, behavior: "smooth"});
  }
  document.querySelectorAll("#mainnav button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll("#mainnav button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      cat = b.getAttribute("data-g");
      if (history.replaceState) history.replaceState(null, "", cat === "all" ? "index.html" : "#" + cat);
      shown = PAGE;
      render();
      toTop();
    });
  });
  document.querySelectorAll(".chip").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      filter = b.getAttribute("data-f");
      shown = PAGE;
      render();
      toTop();
    });
  });
  more.addEventListener("click", function () { shown += PAGE; render(); });
  var h = (location.hash || "").replace("#", "");
  if (["ring", "earrings", "pendant", "necklace", "bracelet"].indexOf(h) >= 0) {
    cat = h;
    document.querySelectorAll("#mainnav button").forEach(function (x) {
      x.classList.toggle("on", x.getAttribute("data-g") === h);
    });
  }
  window.onLangChange = render;
  document.addEventListener("DOMContentLoaded", render);
})();
</script>
"""
    doc += BEACON + "\n</body>\n</html>\n"
    open(os.path.join(ROOT, "index.html"), "w").write(doc)

# ---------------- PDP ----------------
GROUP_LABEL = {"pendant": {"ja": "ペンダント", "en": "Pendants", "zh": "吊坠"},
               "necklace": {"ja": "ネックレス", "en": "Necklaces", "zh": "项链"},
               "earrings": {"ja": "ピアス", "en": "Earrings", "zh": "耳环"},
               "ring": {"ja": "リング", "en": "Rings", "zh": "戒指"},
               "bracelet": {"ja": "ブレスレット", "en": "Bracelets", "zh": "手链"},
               "other": {"ja": "ジュエリー", "en": "Jewellery", "zh": "珠宝"}}
TYPE_LABEL = {"PD NECKLES": {"ja": "ペンダントネックレス", "en": "Pendant necklace", "zh": "吊坠项链"},
              "PENDANT": {"ja": "ペンダントトップ", "en": "Pendant top", "zh": "吊坠"},
              "NECKLES": {"ja": "ネックレス", "en": "Necklace", "zh": "项链"},
              "PIERCE": {"ja": "ピアス", "en": "Pierced earrings", "zh": "耳环"},
              "EAR CUFF": {"ja": "イヤーカフ", "en": "Ear cuff", "zh": "耳骨夹"},
              "RING": {"ja": "リング", "en": "Ring", "zh": "戒指"},
              "BRACELET": {"ja": "ブレスレット", "en": "Bracelet", "zh": "手链"}}

def related(p):
    def score(q):
        s = 0
        if q["group"] == p["group"]: s -= 100
        if q["gem"] == p["gem"]: s -= 50
        if q["price"] and p["price"]: s += abs(q["price"] - p["price"]) / 1e6
        return s
    others = [q for q in PS if q["code"] != p["code"]]
    others.sort(key=score)
    return others[:6]

def tri_txt(d):
    return ('data-i data-ja="%s" data-en="%s" data-zh="%s"' %
            (html.escape(d["ja"], quote=True), html.escape(d["en"], quote=True), html.escape(d["zh"], quote=True)))

def build_pdp(p):
    code = p["code"]
    grp = GROUP_LABEL.get(p["group"], GROUP_LABEL["other"])
    tyl = TYPE_LABEL.get(p["cat"], GROUP_LABEL["other"])
    title = f'{p["names"]["ja"]} {code} | GReEN'
    desc = f'{p["spec"]["ja"]} — GReEN 東京・東日本橋のジュエリーショールーム'
    doc = head(title, desc, 1, og_img=f'img/products/{code}.jpg')
    doc += topbars(1)
    badge = f'<span class="badge" {tri("new")}>{UI["new"]["ja"]}</span>' if p["new"] else ""
    ct_row = ""
    if p["ct"]:
        ct_row = f'<tr><th {tri("carat")}>{UI["carat"]["ja"]}</th><td>{p["ct"]}ct</td></tr>'
    subject = f'?subject={code}%20{UI["contact"]["ja"]}'
    grp_href = f'../index.html#{p["group"]}' if p["group"] in GROUP_LABEL and p["group"] != "other" else "../index.html"
    doc += f"""<p class="crumbs"><a href="../index.html" {tri("backAll")}>{UI["backAll"]["ja"]}</a>
  &nbsp;›&nbsp; <a href="{grp_href}" {tri_txt(grp)}>{grp["ja"]}</a> &nbsp;›&nbsp; {code}</p>
<div class="pdp">
  <div class="tile">{badge}<img src="../img/products/{code}.jpg" alt="{html.escape(p["names"]["ja"])}"></div>
  <div class="pinfo">
    <p class="ref">REF. {code}</p>
    <h1 {tri_txt(p["names"])}>{p["names"]["ja"]}</h1>
    <p class="spec" {tri_txt(p["spec"])}>{p["spec"]["ja"]}</p>
    <p class="price">{price_disp(p)}</p>
    <a class="cta" href="mailto:info@cumulus2026.com{subject}" {tri("inquire")}>{UI["inquire"]["ja"]}</a>
    <p class="ctanote" {tri("inquireNote")}>{UI["inquireNote"]["ja"]}</p>
    <div class="acc">
      <details open>
        <summary {tri("specH")}>{UI["specH"]["ja"]}</summary>
        <div class="accbody">
          <table class="spectable">
            <tr><th {tri("ref")}>{UI["ref"]["ja"]}</th><td>{code}</td></tr>
            <tr><th {tri("type")}>{UI["type"]["ja"]}</th><td {tri_txt(tyl)}>{tyl["ja"]}</td></tr>
            <tr><th {tri("mat")}>{UI["mat"]["ja"]}</th><td>{html.escape(p["mat"])}</td></tr>
            {ct_row}
            <tr><th {tri("price")}>{UI["price"]["ja"]}</th><td>{price_disp(p)}</td></tr>
          </table>
          <p class="note" {tri("photoNote")}>{UI["photoNote"]["ja"]}</p>
        </div>
      </details>
      <details>
        <summary {tri("shopH")}>{UI["shopH"]["ja"]}</summary>
        <div class="accbody">
          <table class="spectable">
            <tr><th {tri("coAddr")}>{UI["coAddr"]["ja"]}</th><td {tri("coAddrV")}>{UI["coAddrV"]["ja"]}</td></tr>
            <tr><th {tri("coContact")}>{UI["coContact"]["ja"]}</th><td>info@cumulus2026.com</td></tr>
          </table>
        </div>
      </details>
    </div>
  </div>
</div>
<section class="reco">
  <h2 {tri("reco")}>{UI["reco"]["ja"]}</h2>
  <div class="recorow">
"""
    for q in related(p):
        qb = f'<span class="badge" {tri("new")}>{UI["new"]["ja"]}</span>' if q["new"] else ""
        doc += (f'<a class="card" href="{q["code"]}.html"><div class="tile">{qb}'
                f'<img src="../img/products/t/{q["code"]}.jpg" alt="{html.escape(q["names"]["ja"])}" loading="lazy"></div>'
                f'<p class="nm" {tri_txt(q["names"])}>{q["names"]["ja"]}</p>'
                f'<p class="sp" {tri_txt(q["spec"])}>{q["spec"]["ja"]}</p>'
                f'<p class="pr">{price_disp(q)}</p></a>\n')
    doc += "</div>\n</section>\n"
    doc += FOOTER
    doc += BEACON + "\n</body>\n</html>\n"
    open(os.path.join(ROOT, "products", f"{code}.html"), "w").write(doc)

def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "products"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "site.css"), "w").write(CSS)
    open(os.path.join(ROOT, "assets", "site.js"), "w").write(JS)
    build_index()
    for p in PS:
        build_pdp(p)
    print(f"built index + {len(PS)} product pages")

if __name__ == "__main__":
    main()

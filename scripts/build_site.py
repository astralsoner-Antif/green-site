#!/usr/bin/env python3
"""data/products.json → index.html + products/{code}.html + assets/site.css
Chopard型のカタログ構成 × GReENトーン。ja/en/zh 切替(localStorage)。
使い方: python3 scripts/build_site.py
"""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PS = json.load(open(os.path.join(ROOT, "data", "products.json")))
FX = json.load(open(os.path.join(ROOT, "data", "fx.json")))  # scripts/update_fx.py で更新

def sig3(x):
    from math import log10, floor
    if x <= 0: return 0
    d = 2 - int(floor(log10(abs(x))))
    return int(round(x, min(d, 0))) if d <= 0 else int(round(x))

def fx_line(jpy, rng=False):
    cny = sig3(jpy * FX["cny"]); usd = sig3(jpy * FX["usd"])
    tail = "〜" if rng else ""
    return "≈ CNY {:,}{} · USD {:,}{}".format(cny, tail, usd, tail)
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
  "introLead":  {"ja": "<span>かたちは、石のためにある。</span><span>ダイヤモンドのパヴェが光を放つモチーフペンダント、</span><span>照りで選び抜いたアコヤパールの連、</span><span>カラーダイヤモンドや南洋パールの一点物など、</span><span>プラチナとゴールドの地金で仕立てた</span><span>コレクションをご覧ください。</span>", "en": "<span>Form exists for the stone.</span> <span>Motif pendants paved with diamonds,</span> <span>strands of Akoya pearls chosen for their lustre,</span> <span>one-off coloured diamonds and South Sea pearls —</span> <span>a collection crafted in platinum and gold.</span>", "zh": "<span>造型，为宝石而生。</span><span>铺镶钻石的造型吊坠、</span><span>以光泽甄选的Akoya珍珠链、</span><span>彩钻与南洋珍珠的独件之作——</span><span>以铂金与K金精心打造的系列，</span><span>敬请鉴赏。</span>"},
  # キャッチコピー(2026-08-13確定・動画モジュール実装時に使用):
  #   ja「石を、解き放つ。」 en "Set the stone free." zh「让宝石，自由。」
  "inquire":    {"ja": "お問い合わせ", "en": "Inquire", "zh": "咨询"},
  "inquireNote":{"ja": "在庫・ご来店のご相談は、品番を添えてご連絡ください。海外への発送にも対応しています。", "en": "For availability or a showroom visit, please contact us with the reference number. International shipping is available.", "zh": "如需确认库存或预约到店，请附上产品编号与我们联系。支持海外配送。"},
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
  "fxNote":     {"ja": "参考換算（%sレート）", "en": "Approx. conversion (rate as of %s)", "zh": "参考换算（%s汇率）"},
  "annBar":     {"ja": "東京・東日本橋ショールーム ｜ 海外への発送に対応しています", "en": "Showroom in Higashi-Nihonbashi, Tokyo — international shipping available", "zh": "东京·东日本桥陈列室 ｜ 支持海外配送"},
  "gemRow":     {"ja": "宝石", "en": "Gemstone", "zh": "宝石"},
  "sizeRow":    {"ja": "サイズ", "en": "Size", "zh": "尺寸"},
  "stockOne":   {"ja": "在庫一点限りです。", "en": "One piece available.", "zh": "仅此一件。"},
  "recent":     {"ja": "最近ご覧になったアイテム", "en": "Recently viewed", "zh": "最近浏览"},
  "popular":    {"ja": "人気", "en": "Popular", "zh": "热卖"},
  "classic":    {"ja": "定番", "en": "Classic", "zh": "经典"},
  "catalog":    {"ja": "カタログ", "en": "Catalogue", "zh": "目录"},
  "catLead":    {"ja": "気になる商品を集めて、まとめてお問い合わせいただけます。", "en": "Collect the pieces you are interested in and send a single enquiry.", "zh": "收藏感兴趣的商品，一键统一咨询。"},
  "catEmpty":   {"ja": "カタログはまだ空です。商品の ♡ から追加できます。", "en": "Your catalogue is empty. Tap ♡ on any piece to add it.", "zh": "目录还是空的。点击商品上的 ♡ 即可加入。"},
  "catMail":    {"ja": "まとめてお問い合わせ", "en": "Send enquiry for all", "zh": "一键咨询全部"},
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

# 大分類ごとの見出し+リード文(2026-08-13 Koki指示: カテゴリ別に出し分け)
CAT_INTROS = {
  "ring": {
    "h": {"ja": "リング", "en": "Rings", "zh": "戒指"},
    "l": {"ja": "<span>指もとに宿る、一粒の存在感。</span><span>照りの良いアコヤパールを4mmから8mm、</span><span>10mmのブラックパールまで揃え、</span><span>プラチナとゴールドの地金にセッティングしました。</span><span>日々の仕草に、さりげない輝きを添えます。</span>",
          "en": "<span>A single pearl's quiet presence upon the hand.</span> <span>Akoya pearls from 4mm to 8mm</span> <span>and a 10mm black pearl,</span> <span>set in platinum and gold —</span> <span>a subtle brilliance for everyday gestures.</span>",
          "zh": "<span>指间，一粒珍珠的静谧存在。</span><span>Akoya珍珠从4mm到8mm，</span><span>另有10mm黑珍珠，</span><span>镶嵌于铂金与K金——</span><span>为日常举手投足，添一份低调光芒。</span>"},
  },
  "earrings": {
    "h": {"ja": "ピアス", "en": "Earrings", "zh": "耳环"},
    "l": {"ja": "<span>顔まわりを明るく照らす、光のスタッド。</span><span>粒を揃えたアコヤパールは3mmから7.5mm、</span><span>花モチーフの一点や、ダイヤモンド、</span><span>トリートブルーダイヤモンド、</span><span>イエローダイヤモンドのイヤーカフまで。</span><span>プラチナからK10まで、</span><span>その日の装いに合わせてお選びいただけます。</span>",
          "en": "<span>Studs of light to frame the face.</span> <span>Matched Akoya pearls from 3mm to 7.5mm,</span> <span>floral pieces, diamond earrings,</span> <span>a treated-blue diamond pair</span> <span>and a yellow-diamond ear cuff —</span> <span>from platinum to 10-karat gold,</span> <span>a brilliance for every look.</span>",
          "zh": "<span>点亮面庞的光之耳钉。</span><span>粒径齐整的Akoya珍珠从3mm到7.5mm，</span><span>亦有花朵造型、钻石耳环、</span><span>处理蓝钻与黄钻耳骨夹——</span><span>从铂金到K10，</span><span>随当日装扮自由挑选。</span>"},
  },
  "pendant": {
    "h": {"ja": "ペンダント", "en": "Pendants", "zh": "吊坠"},
    "l": {"ja": "<span>クロス、フラワー、ホースシュー —</span><span>胸もとに物語を宿すモチーフたち。</span><span>ダイヤモンドのパヴェを中心に、</span><span>イエローやピンクのカラーダイヤモンド、</span><span>エメラルドの一点物、</span><span>12mm級の南洋白蝶パールやブラックパールなど、</span><span>最も幅広いコレクションをご覧ください。</span>",
          "en": "<span>Cross, flower, horseshoe —</span> <span>motifs that carry a story at the chest.</span> <span>Pavé diamond pendant necklaces</span> <span>alongside yellow and pink diamonds,</span> <span>a one-off emerald,</span> <span>and 12mm-class South Sea and black pearls —</span> <span>discover our widest collection.</span>",
          "zh": "<span>十字、花朵、马蹄——</span><span>承载故事的胸前造型。</span><span>以铺镶钻石吊坠项链为主，</span><span>另有黄钻粉钻、独件祖母绿、</span><span>12mm级南洋白珠与黑珍珠——</span><span>最丰富的系列，敬请鉴赏。</span>"},
  },
  "necklace": {
    "h": {"ja": "ネックレス", "en": "Necklaces", "zh": "项链"},
    "l": {"ja": "<span>首もとに沿う、光の連なり。</span><span>照りを揃えたアコヤパールの連は4.5mmから8.5mm、</span><span>バロックやナチュラルカラー、</span><span>2.5mmの小粒淡水から16mm級の大珠まで。</span><span>45cmから85cmまでの長さが、</span><span>装いに合わせた表情を叶えます。</span>",
          "en": "<span>A line of light along the neck.</span> <span>Akoya strands matched for lustre,</span> <span>4.5mm to 8.5mm, baroque and natural colours,</span> <span>freshwater pearls from 2.5mm to a bold 16mm —</span> <span>in lengths of 45cm to 85cm</span> <span>to suit the occasion.</span>",
          "zh": "<span>沿颈而下的光之线条。</span><span>光泽齐整的Akoya珍珠链从4.5mm到8.5mm，</span><span>巴洛克与天然色、</span><span>2.5mm小珠至16mm大珠的淡水珍珠——</span><span>长度45cm至85cm，</span><span>随场合展现风情。</span>"},
  },
  "bracelet": {
    "h": {"ja": "ブレスレット", "en": "Bracelets", "zh": "手链"},
    "l": {"ja": "<span>腕もとで、光が軽やかに踊る。</span><span>総カラット1.88のダイヤモンドブレスレットと、</span><span>K18のメタルブレスレット —</span><span>仕草のひとつひとつに輝きを添えます。</span>",
          "en": "<span>Light that dances at the wrist.</span> <span>A diamond bracelet totalling 1.88 carats</span> <span>and a metal bracelet in 18-karat gold —</span> <span>brilliance in every gesture.</span>",
          "zh": "<span>腕间，光在轻盈起舞。</span><span>总重1.88克拉的钻石手链，</span><span>与K18金属手链——</span><span>举手投足，皆添光彩。</span>"},
  },
}

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
  --script: "Great Vibes", "Snell Roundhand", cursive;
}
html { -webkit-text-size-adjust: 100%; }
body { background: var(--paper); color: var(--ink); font-family: var(--serif); line-height: 1.7; }
a { color: inherit; text-decoration: none; }
img { max-width: 100%; }

/* ---- announcement bar (Chopard型の細いバー) ---- */
.annbar { background: var(--emerald-deep); color: rgba(255,255,255,0.92);
  font-family: var(--sans); font-size: 10px; letter-spacing: 0.14em;
  text-align: center; padding: 7px 14px; }

/* ---- top bar ---- */
.topbar { display: flex; justify-content: space-between; align-items: center;
  padding: 9px 20px; border-bottom: 1px solid var(--hairline);
  font-family: var(--sans); font-size: 11px; letter-spacing: 0.08em; color: var(--muted); }
.topbar a:hover { color: var(--emerald-deep); }
.topbar .tl { display: flex; gap: 18px; align-items: center; }
.catlink:hover { color: var(--emerald-deep); }
.catlink #catcount { color: var(--emerald-deep); margin-left: 2px; }
.langs { display: flex; gap: 14px; }
.langs button { background: none; border: none; cursor: pointer; font: inherit;
  color: var(--muted); letter-spacing: 0.08em; padding: 0; }
.langs button.on { color: var(--emerald-deep); border-bottom: 1px solid var(--emerald-deep); }

/* ---- brand bar ---- */
.brandbar { display: flex; justify-content: center; align-items: center;
  padding: 22px 20px 18px; border-bottom: 1px solid var(--hairline); background: var(--paper); }
.brandbar { position: relative; }
.brandbar::after { content: ""; position: absolute; left: 50%; bottom: -1px;
  transform: translateX(-50%); width: 72px; height: 1px; background: var(--gold); }
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

/* ---- listing intro (カテゴリ紹介パース) ----
   階層: 彫刻体アクセント(Engravers風caps/金) → 見出し(しっぽり明朝) → リード(明朝) → 詳細(サンセリフ) */
.intro { text-align: center; padding: 42px 24px 10px; }
.intro .accent { font-family: Palatino, "Palatino Linotype", Georgia, serif;
  font-size: 12.5px; font-weight: 400; letter-spacing: 0.55em; padding-left: 0.55em;
  text-transform: uppercase; color: var(--gold); margin-bottom: 12px; }
.intro h1 { font-family: var(--display); font-weight: 600; font-size: 32px; letter-spacing: 0.24em; line-height: 1.6; }
.intro .lead { font-family: var(--display); font-size: 15px; letter-spacing: 0.07em; line-height: 2.15;
  color: var(--ink); max-width: 660px; margin: 20px auto 0; }
.intro .lead span { display: inline-block; }
html[lang="en"] .intro .accent { display: none; } /* 英語時はH1と重複するため */
@media (max-width: 700px) { .intro h1 { font-size: 24px; } .intro { padding-top: 30px; }
  .intro .accent { font-size: 11px; } .intro .lead { font-size: 13px; } }

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
.badge.popular { color: #a8873f; }
.badge.classic { color: var(--muted); }
.fav { position: absolute; top: 7px; right: 9px; z-index: 2; background: none; border: none;
  cursor: pointer; font-size: 15px; line-height: 1; color: var(--muted); padding: 4px; }
.fav.on { color: #b3542f; }
.favbtn { display: block; width: 100%; text-align: center; font-family: var(--sans);
  font-size: 11px; letter-spacing: 0.18em; padding: 13px 10px; margin-top: 10px;
  background: none; border: 1px solid var(--hairline); color: var(--ink); cursor: pointer; }
.favbtn:hover { border-color: var(--emerald-deep); color: var(--emerald-deep); }
.card .nm { font-family: var(--display); font-size: 14px; font-weight: 600;
  letter-spacing: 0.08em; line-height: 1.6; margin: 13px 2px 0;
  word-break: keep-all; overflow-wrap: anywhere; }
.card .sp { font-family: var(--sans); font-size: 9.5px; letter-spacing: 0.03em;
  color: var(--muted); opacity: 0.9; margin: 3px 2px 0; line-height: 1.55;
  word-break: keep-all; overflow-wrap: anywhere; }
.card .pr { font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.06em;
  margin: 6px 2px 0; font-variant-numeric: tabular-nums; }
.card .prfx { font-family: var(--sans); font-size: 10px; letter-spacing: 0.05em;
  color: var(--muted); margin: 2px 2px 0; font-variant-numeric: tabular-nums; }
.pager { display: flex; gap: 7px; justify-content: center; align-items: center;
  padding: 30px 20px 64px; flex-wrap: wrap; }
.pager button { min-width: 34px; height: 34px; border: 1px solid var(--hairline);
  background: none; font-family: var(--sans); font-size: 11.5px; letter-spacing: 0.04em;
  cursor: pointer; color: var(--ink); }
.pager button.on { background: var(--emerald-deep); border-color: var(--emerald-deep); color: #fff; }
.pager button:disabled { opacity: 0.35; cursor: default; }

/* ---- カタログページ ---- */
.catwrap { max-width: 860px; margin: 0 auto; padding: 10px 20px 70px; }
.catrow { display: grid; grid-template-columns: 84px 1fr auto auto; gap: 16px;
  align-items: center; border-bottom: 1px solid var(--hairline); padding: 14px 0; }
.catrow .cimg { width: 84px; height: 84px; background: var(--tile);
  display: flex; align-items: center; justify-content: center; }
.catrow .cimg img { width: 88%; height: 88%; object-fit: contain; mix-blend-mode: multiply; }
.catrow .cnm { font-family: var(--display); font-size: 13.5px; font-weight: 600; letter-spacing: 0.05em; }
.catrow .csp { font-family: var(--sans); font-size: 9.5px; color: var(--muted); margin-top: 3px; }
.catrow .cpr { font-family: var(--sans); font-size: 12.5px; font-variant-numeric: tabular-nums; white-space: nowrap; }
.catrow .crm { background: none; border: none; cursor: pointer; font-size: 15px; color: var(--muted); padding: 6px; }
.catrow .crm:hover { color: #b3542f; }
.catsum { font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.06em; text-align: right;
  padding: 18px 2px 6px; font-variant-numeric: tabular-nums; }
.catsum .cfx { display: block; font-size: 10.5px; color: var(--muted); margin-top: 3px; }
.catcta { display: block; text-align: center; font-family: var(--sans); font-size: 12px;
  letter-spacing: 0.28em; padding: 16px 10px; margin-top: 18px;
  background: var(--emerald-deep); color: #fff; }
.catcta:hover { background: var(--emerald); }
.catempty { font-family: var(--sans); font-size: 12px; color: var(--muted);
  text-align: center; padding: 46px 10px; letter-spacing: 0.08em; }
@media (max-width: 560px) { .catrow { grid-template-columns: 64px 1fr auto; }
  .catrow .cpr { grid-column: 2; justify-self: start; } .catrow .cimg { width: 64px; height: 64px; } }

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
.pinfo .pricefx { font-family: var(--sans); font-size: 12px; letter-spacing: 0.05em;
  color: var(--muted); margin-top: 5px; font-variant-numeric: tabular-nums; }
.pinfo .pricefxnote { font-family: var(--sans); font-size: 9.5px; letter-spacing: 0.04em;
  color: var(--muted); opacity: 0.75; margin-top: 3px; }
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
.reco h2::before { content: ""; display: block; width: 40px; height: 1px;
  background: var(--gold); margin: 0 auto 14px; }

/* ---- PDP 説明文 ---- */
.pdesc { font-family: var(--serif); font-size: 13px; letter-spacing: 0.05em;
  line-height: 2.05; margin-bottom: 16px; }

/* ---- PDPスティッキーバー ---- */
.stickybar { position: fixed; top: 0; left: 0; right: 0; z-index: 60;
  background: rgba(254,254,254,0.96); backdrop-filter: blur(6px);
  border-bottom: 1px solid var(--hairline);
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 18px; transform: translateY(-110%); transition: transform 0.35s ease; }
.stickybar.show { transform: translateY(0); }
.stickybar .snm { font-family: var(--display); font-size: 13px; font-weight: 600;
  letter-spacing: 0.06em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.stickybar .spr { font-family: var(--sans); font-size: 12.5px; letter-spacing: 0.04em;
  font-variant-numeric: tabular-nums; white-space: nowrap; }
.stickybar .scta { flex: 0 0 auto; font-family: var(--sans); font-size: 10.5px;
  letter-spacing: 0.2em; padding: 9px 18px; background: var(--emerald-deep); color: #fff; }
.stickybar .scta:hover { background: var(--emerald); }

/* ---- ライトボックス ---- */
.pdp .tile { cursor: zoom-in; }
.lightbox { position: fixed; inset: 0; z-index: 100; background: rgba(254,254,254,0.97);
  display: none; align-items: center; justify-content: center; cursor: zoom-out; }
.lightbox.on { display: flex; }
.lightbox img { max-width: 94vw; max-height: 92vh; object-fit: contain; }
.lightbox .lbx { position: absolute; top: 16px; right: 22px; font-family: var(--sans);
  font-size: 22px; color: var(--muted); cursor: pointer; }

/* ---- 最近見たアイテム ---- */
.recent { max-width: 1380px; margin: 0 auto; padding: 0 20px 56px; display: none; }
.recent.on { display: block; }
.recent h2 { font-family: var(--display); font-size: 16px; font-weight: 600;
  letter-spacing: 0.16em; text-align: center; margin-bottom: 20px; }
.recent h2::before { content: ""; display: block; width: 40px; height: 1px;
  background: var(--gold); margin: 0 auto 12px; }
.recentrow { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(150px, 190px);
  gap: 16px; overflow-x: auto; scrollbar-width: none; justify-content: safe center; }
.recentrow::-webkit-scrollbar { display: none; }
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
window.greenFav = {
  key: "green-fav",
  get: function () { try { return JSON.parse(localStorage.getItem(this.key) || "[]"); } catch (e) { return []; } },
  set: function (a) { try { localStorage.setItem(this.key, JSON.stringify(a)); } catch (e) {} this.badge(); },
  has: function (c) { return this.get().indexOf(c) >= 0; },
  toggle: function (c) { var a = this.get(); var i = a.indexOf(c); if (i >= 0) a.splice(i, 1); else a.unshift(c); this.set(a); },
  badge: function () { var el = document.getElementById("catcount"); if (el) { var n = this.get().length; el.textContent = n > 0 ? "(" + n + ")" : ""; } }
};
document.addEventListener("DOMContentLoaded", function () { window.greenFav.badge(); });
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
    return f"""<div class="annbar" {tri("annBar")}>{UI["annBar"]["ja"]}</div>
<div class="topbar">
  <div class="tl">
    <a href="mailto:info@cumulus2026.com" {tri("contact")}>お問い合わせ</a>
    <a class="catlink" href="{p}catalog.html"><span {tri("catalog")}>カタログ</span><span id="catcount"></span></a>
  </div>
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
            "pr": p["price"], "rng": bool(p.get("price_max")),
            "g": p["group"], "gem": p["gem"], "new": p["new"], "high": p["high"],
            "b": p.get("badge"),
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
  <p class="accent" id="introAccent" aria-hidden="true">Jewellery</p>
  <h1 id="introH">{UI["introTitle"]["ja"]}</h1>
  <p class="lead" id="introLead">{UI["introLead"]["ja"]}</p>
</section>
<div class="chipswrap"><div class="chips">{chips_html}</div></div>
<p class="count" id="count"></p>
<div class="grid" id="grid"></div>
<div class="pager" id="pager"></div>
"""
    doc += shop_section(0)
    doc += FOOTER
    intros = {"all": {"h": UI["introTitle"], "l": UI["introLead"]}}
    intros.update(CAT_INTROS)
    doc += "<script>var PRODUCTS = %s;\nvar INTROS = %s;\nvar FX = %s;</script>" % (
        json.dumps(items, ensure_ascii=False, separators=(",", ":")),
        json.dumps(intros, ensure_ascii=False, separators=(",", ":")),
        json.dumps(FX))
    doc += """<script>
(function () {
  var PAGE = 24, page = 1, cat = "all", filter = "all";
  var grid = document.getElementById("grid"), count = document.getElementById("count"),
      pager = document.getElementById("pager");
  var BDG = {"new": {ja: "新作", en: "New", zh: "新品"},
             "popular": {ja: "人気", en: "Popular", zh: "热卖"},
             "classic": {ja: "定番", en: "Classic", zh: "经典"}};
  var FMT = {ja: "{total} 点中 {from}–{to} 点を表示中", en: "Showing {from}–{to} of {total}", zh: "显示 {from}–{to} / {total} 件"};
  function match(p) {
    if (cat !== "all" && p.g !== cat) return false;
    if (filter === "all") return true;
    if (filter === "new") return p.new;
    if (filter === "high") return p.high;
    return p.gem === filter;
  }
  function sig3(x) {
    if (x <= 0) return 0;
    var d = Math.pow(10, Math.max(0, Math.floor(Math.log10(x)) - 2));
    return Math.round(x / d) * d;
  }
  function fxLine(jpy, rng) {
    var t = rng ? "〜" : "";
    return "≈ CNY " + sig3(jpy * FX.cny).toLocaleString() + t +
           " · USD " + sig3(jpy * FX.usd).toLocaleString() + t;
  }
  function toTop() {
    window.scrollTo({top: document.querySelector(".chipswrap").offsetTop - 60, behavior: "smooth"});
  }
  function updateIntro() {
    var l = window.GREEN_LANG || "ja";
    var d = INTROS[cat] || INTROS.all;
    document.getElementById("introAccent").textContent = d.h.en;
    document.getElementById("introH").innerHTML = d.h[l];
    document.getElementById("introLead").innerHTML = d.l[l];
  }
  function render() {
    var l = window.GREEN_LANG || "ja";
    var list = PRODUCTS.filter(match);
    var pages = Math.max(1, Math.ceil(list.length / PAGE));
    if (page > pages) page = pages;
    var from = (page - 1) * PAGE;
    var vis = list.slice(from, from + PAGE);
    var fav = window.greenFav.get();
    grid.innerHTML = vis.map(function (p) {
      var b = p.b ? '<span class="badge ' + p.b + '">' + BDG[p.b][l] + "</span>" : "";
      var on = fav.indexOf(p.c) >= 0;
      return '<a class="card" href="products/' + encodeURIComponent(p.c) + '.html">' +
        '<div class="tile">' + b +
        '<button class="fav' + (on ? " on" : "") + '" data-c="' + p.c + '" aria-label="catalogue">' + (on ? "♥" : "♡") + "</button>" +
        '<img src="img/products/t/' + encodeURIComponent(p.c) + '.jpg" alt="' + p.n[l] + '" loading="lazy"></div>' +
        '<p class="nm">' + p.n[l] + '</p><p class="sp">' + p.s[l] + '</p><p class="pr">' + p.p + "</p>" +
        (p.pr ? '<p class="prfx">' + fxLine(p.pr, p.rng) + "</p>" : "") + "</a>";
    }).join("");
    count.textContent = list.length ? FMT[l].replace("{from}", from + 1).replace("{to}", from + vis.length).replace("{total}", list.length)
                                    : FMT[l].replace("{from}", 0).replace("{to}", 0).replace("{total}", 0);
    var ph = "";
    if (pages > 1) {
      ph += '<button data-pg="prev"' + (page === 1 ? " disabled" : "") + '>‹</button>';
      for (var i = 1; i <= pages; i++) ph += '<button data-pg="' + i + '"' + (i === page ? ' class="on"' : "") + ">" + i + "</button>";
      ph += '<button data-pg="next"' + (page === pages ? " disabled" : "") + '>›</button>';
    }
    pager.innerHTML = ph;
    pager.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-pg");
        if (v === "prev") page--; else if (v === "next") page++; else page = parseInt(v, 10);
        render();
        toTop();
      });
    });
    grid.querySelectorAll(".fav").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        window.greenFav.toggle(b.getAttribute("data-c"));
        var on = b.classList.toggle("on");
        b.textContent = on ? "♥" : "♡";
      });
    });
  }
  document.querySelectorAll("#mainnav button").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll("#mainnav button").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      cat = b.getAttribute("data-g");
      if (history.replaceState) history.replaceState(null, "", cat === "all" ? "index.html" : "#" + cat);
      page = 1;
      updateIntro();
      render();
      window.scrollTo({top: 0, behavior: "smooth"});
    });
  });
  document.querySelectorAll(".chip").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("on"); });
      b.classList.add("on");
      filter = b.getAttribute("data-f");
      page = 1;
      render();
      toTop();
    });
  });
  var h = (location.hash || "").replace("#", "");
  if (["ring", "earrings", "pendant", "necklace", "bracelet"].indexOf(h) >= 0) {
    cat = h;
    document.querySelectorAll("#mainnav button").forEach(function (x) {
      x.classList.toggle("on", x.getAttribute("data-g") === h);
    });
  }
  window.onLangChange = function () { updateIntro(); render(); };
  document.addEventListener("DOMContentLoaded", function () { updateIntro(); render(); });
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

DESC_OPEN = {
  "pendant":  {"ja": "胸もとに、{g}の光を添える一点。", "en": "A point of {g} light at the chest.", "zh": "为胸前添一点{g}之光。"},
  "necklace": {"ja": "首もとに沿う、{g}の連なり。", "en": "A strand of {g} along the neckline.", "zh": "沿颈而下的{g}串连。"},
  "earrings": {"ja": "耳もとで、動きとともに輝く{g}。", "en": "{g} that catches the light with every movement.", "zh": "随动作闪耀于耳畔的{g}。"},
  "ring":     {"ja": "指もとに、{g}の存在感を。", "en": "The presence of {g} upon the hand.", "zh": "指间尽显{g}的存在感。"},
  "bracelet": {"ja": "腕もとに、{g}の光を。", "en": "{g} light at the wrist.", "zh": "为腕间添上{g}之光。"},
  "other":    {"ja": "{g}のジュエリー。", "en": "{g} jewellery.", "zh": "{g}珠宝。"},
}

def desc_texts(p):
    gem = p.get("gem_names") or {"ja": p["names"]["ja"], "en": p["names"]["en"], "zh": p["names"]["zh"]}
    op = DESC_OPEN.get(p["group"], DESC_OPEN["other"])
    mm = [x for x in p.get("sizes", []) if x.endswith("mm")]
    ln = [x for x in p.get("sizes", []) if x.endswith("cm")]
    out = {}
    for l in ("ja", "en", "zh"):
        t = op[l].format(g=gem[l])
        if l == "ja":
            f = "地金は" + p["mat"] if p["mat"] else ""
            if p["ct"]: f += "、総カラット%sct" % p["ct"]
            if mm: f += "、サイズ%s" % mm[0]
            if ln: f += "、長さ%s" % ln[0]
            if f: t += " " + f + "。"
            if p["stock"] == 1: t += "在庫一点限りです。"
        elif l == "en":
            f = ("Crafted in %s" % p["mat"]) if p["mat"] else ""
            if p["ct"]: f += ", %sct total" % p["ct"]
            if mm: f += ", %s" % mm[0]
            if ln: f += ", length %s" % ln[0]
            if f: t += " " + f + "."
            if p["stock"] == 1: t += " One piece available."
        else:
            f = ("材质为" + p["mat"]) if p["mat"] else ""
            if p["ct"]: f += "，总重%s克拉" % p["ct"]
            if mm: f += "，尺寸%s" % mm[0]
            if ln: f += "，长度%s" % ln[0]
            if f: t += f + "。"
            if p["stock"] == 1: t += "仅此一件。"
        out[l] = t
    return out

def fx_block(p):
    if not p["price"]:
        return ""
    line = fx_line(p["price"], bool(p.get("price_max")))
    return '<p class="pricefx">%s</p>' % line

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
    bk = p.get("badge")
    badge = f'<span class="badge {bk}" {tri(bk)}>{UI[bk]["ja"]}</span>' if bk else ""
    ct_row = ""
    if p["ct"]:
        ct_row = f'<tr><th {tri("carat")}>{UI["carat"]["ja"]}</th><td>{p["ct"]}ct</td></tr>'
    gem_row = ""
    if p.get("gem_names"):
        gem_row = f'<tr><th {tri("gemRow")}>{UI["gemRow"]["ja"]}</th><td {tri_txt(p["gem_names"])}>{p["gem_names"]["ja"]}</td></tr>'
    size_row = ""
    sz = ", ".join(p.get("sizes", []))
    if sz:
        size_row = f'<tr><th {tri("sizeRow")}>{UI["sizeRow"]["ja"]}</th><td>{sz}</td></tr>'
    desc = desc_texts(p)
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
    {fx_block(p)}
    <a class="cta" href="mailto:info@cumulus2026.com{subject}" {tri("inquire")}>{UI["inquire"]["ja"]}</a>
    <button class="favbtn" id="favbtn">♡ カタログに追加</button>
    <p class="ctanote" {tri("inquireNote")}>{UI["inquireNote"]["ja"]}</p>
    <div class="acc">
      <details open>
        <summary {tri("specH")}>{UI["specH"]["ja"]}</summary>
        <div class="accbody">
          <p class="pdesc" {tri_txt(desc)}>{desc["ja"]}</p>
          <table class="spectable">
            <tr><th {tri("ref")}>{UI["ref"]["ja"]}</th><td>{code}</td></tr>
            <tr><th {tri("type")}>{UI["type"]["ja"]}</th><td {tri_txt(tyl)}>{tyl["ja"]}</td></tr>
            <tr><th {tri("mat")}>{UI["mat"]["ja"]}</th><td>{html.escape(p["mat"])}</td></tr>
            {gem_row}
            {ct_row}
            {size_row}
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
        qbk = q.get("badge")
        qb = f'<span class="badge {qbk}" {tri(qbk)}>{UI[qbk]["ja"]}</span>' if qbk else ""
        doc += (f'<a class="card" href="{q["code"]}.html"><div class="tile">{qb}'
                f'<img src="../img/products/t/{q["code"]}.jpg" alt="{html.escape(q["names"]["ja"])}" loading="lazy"></div>'
                f'<p class="nm" {tri_txt(q["names"])}>{q["names"]["ja"]}</p>'
                f'<p class="sp" {tri_txt(q["spec"])}>{q["spec"]["ja"]}</p>'
                f'<p class="pr">{price_disp(q)}</p></a>\n')
    doc += "</div>\n</section>\n"
    doc += f"""<section class="recent" id="recent">
  <h2 {tri("recent")}>{UI["recent"]["ja"]}</h2>
  <div class="recentrow" id="recentrow"></div>
</section>
"""
    doc += FOOTER
    me = {"c": code, "n": p["names"], "s": p["spec"], "p": price_disp(p),
          "t": f"../img/products/t/{code}.jpg", "h": f"{code}.html"}
    doc += f"""<div class="stickybar" id="stickybar">
  <p class="snm" {tri_txt(p["names"])}>{p["names"]["ja"]}</p>
  <p class="spr">{price_disp(p)}</p>
  <a class="scta" href="mailto:info@cumulus2026.com{subject}" {tri("inquire")}>{UI["inquire"]["ja"]}</a>
</div>
<div class="lightbox" id="lightbox"><span class="lbx">×</span><img src="../img/products/{code}.jpg" alt=""></div>
"""
    doc += "<script>var ME = %s;</script>" % json.dumps(me, ensure_ascii=False, separators=(",", ":"))
    doc += """<script>
(function () {
  var sb = document.getElementById("stickybar");
  window.addEventListener("scroll", function () {
    sb.classList.toggle("show", window.scrollY > 520);
  }, {passive: true});
  var lb = document.getElementById("lightbox");
  var tileImg = document.querySelector(".pdp .tile img");
  if (tileImg) tileImg.addEventListener("click", function () { lb.classList.add("on"); });
  lb.addEventListener("click", function () { lb.classList.remove("on"); });
  var fb = document.getElementById("favbtn");
  var FT = {add: {ja: "♡ カタログに追加", en: "♡ Add to catalogue", zh: "♡ 加入目录"},
            has: {ja: "♥ カタログに追加済み", en: "♥ In catalogue", zh: "♥ 已加入目录"}};
  var fbr = function () {
    var l = window.GREEN_LANG || "ja";
    fb.textContent = window.greenFav.has(ME.c) ? FT.has[l] : FT.add[l];
  };
  fb.addEventListener("click", function () { window.greenFav.toggle(ME.c); fbr(); });
  document.addEventListener("DOMContentLoaded", fbr);
  var prevF = window.onLangChange;
  window.onLangChange = function () { if (prevF) prevF(); fbr(); };
  fbr();
  var KEY = "green-recent";
  try {
    var arr = JSON.parse(localStorage.getItem(KEY) || "[]");
    arr = arr.filter(function (x) { return x.c !== ME.c; });
    var show = arr.slice(0, 6);
    arr.unshift(ME);
    localStorage.setItem(KEY, JSON.stringify(arr.slice(0, 9)));
    if (show.length) {
      var row = document.getElementById("recentrow");
      var render = function () {
        var l = window.GREEN_LANG || "ja";
        row.innerHTML = show.map(function (x) {
          return '<a class="card" href="' + x.h + '"><div class="tile"><img src="' + x.t + '" loading="lazy" alt=""></div>' +
            '<p class="nm">' + x.n[l] + '</p><p class="pr">' + x.p + "</p></a>";
        }).join("");
      };
      render();
      var prev = window.onLangChange;
      window.onLangChange = function () { if (prev) prev(); render(); fbr(); };
      document.getElementById("recent").classList.add("on");
    }
  } catch (e) {}
})();
</script>
"""
    doc += BEACON + "\n</body>\n</html>\n"
    open(os.path.join(ROOT, "products", f"{code}.html"), "w").write(doc)

def build_catalog_page():
    items = []
    for p in PS:
        items.append({"c": p["code"], "n": p["names"], "s": p["spec"], "p": price_disp(p),
                      "pr": p["price"], "b": p.get("badge")})
    doc = head("カタログ | GReEN", "気になる商品を集めて、まとめてお問い合わせ。", 0)
    doc += topbars(0)
    doc += f"""<section class="intro">
  <p class="accent" aria-hidden="true">Catalogue</p>
  <h1 {tri("catalog")}>{UI["catalog"]["ja"]}</h1>
  <p class="lead" {tri("catLead")}>{UI["catLead"]["ja"]}</p>
</section>
<div class="catwrap">
  <div id="catlist"></div>
  <div class="catsum" id="catsum" style="display:none"></div>
  <a class="catcta" id="catmail" href="#" style="display:none" {tri("catMail")}>{UI["catMail"]["ja"]}</a>
  <p class="catempty" id="catempty" {tri("catEmpty")}>{UI["catEmpty"]["ja"]}</p>
</div>
"""
    doc += FOOTER
    doc += "<script>var PRODUCTS = %s;\nvar FX = %s;</script>" % (
        json.dumps(items, ensure_ascii=False, separators=(",", ":")), json.dumps(FX))
    doc += """<script>
(function () {
  var SUM = {ja: "{n}点 ・ 合計 {sum}", en: "{n} items · Total {sum}", zh: "{n}件 ・ 合计 {sum}"};
  var SUBJ = {ja: "カタログお問い合わせ（{n}点）", en: "Catalogue enquiry ({n} items)", zh: "目录咨询（{n}件）"};
  var byCode = {};
  PRODUCTS.forEach(function (p) { byCode[p.c] = p; });
  function sig3(x) {
    if (x <= 0) return 0;
    var d = Math.pow(10, Math.max(0, Math.floor(Math.log10(x)) - 2));
    return Math.round(x / d) * d;
  }
  function render() {
    var l = window.GREEN_LANG || "ja";
    var codes = window.greenFav.get().filter(function (c) { return byCode[c]; });
    var list = codes.map(function (c) { return byCode[c]; });
    var el = document.getElementById("catlist"), sum = document.getElementById("catsum"),
        mail = document.getElementById("catmail"), emp = document.getElementById("catempty");
    if (!list.length) {
      el.innerHTML = ""; sum.style.display = "none"; mail.style.display = "none"; emp.style.display = "";
      return;
    }
    emp.style.display = "none"; sum.style.display = ""; mail.style.display = "";
    el.innerHTML = list.map(function (p) {
      return '<div class="catrow"><a class="cimg" href="products/' + encodeURIComponent(p.c) + '.html">' +
        '<img src="img/products/t/' + encodeURIComponent(p.c) + '.jpg" alt=""></a>' +
        '<div><a href="products/' + encodeURIComponent(p.c) + '.html"><p class="cnm">' + p.n[l] + '</p>' +
        '<p class="csp">REF. ' + p.c + " ｜ " + p.s[l] + '</p></a></div>' +
        '<p class="cpr">' + p.p + '</p>' +
        '<button class="crm" data-c="' + p.c + '" aria-label="remove">×</button></div>';
    }).join("");
    var total = list.reduce(function (a, p) { return a + (p.pr || 0); }, 0);
    var yen = "¥ " + total.toLocaleString();
    sum.innerHTML = SUM[l].replace("{n}", list.length).replace("{sum}", yen) +
      '<span class="cfx">≈ CNY ' + sig3(total * FX.cny).toLocaleString() +
      " · USD " + sig3(total * FX.usd).toLocaleString() + "</span>";
    var lines = list.map(function (p, i) {
      return (i + 1) + ". " + p.c + " " + p.n[l] + " " + p.p;
    });
    mail.href = "mailto:info@cumulus2026.com?subject=" +
      encodeURIComponent(SUBJ[l].replace("{n}", list.length)) +
      "&body=" + encodeURIComponent(lines.join("\\n") + "\\n\\n");
    el.querySelectorAll(".crm").forEach(function (b) {
      b.addEventListener("click", function () {
        window.greenFav.toggle(b.getAttribute("data-c"));
        render();
      });
    });
  }
  window.onLangChange = render;
  document.addEventListener("DOMContentLoaded", render);
})();
</script>
"""
    doc += BEACON + "\n</body>\n</html>\n"
    open(os.path.join(ROOT, "catalog.html"), "w").write(doc)

def main():
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "products"), exist_ok=True)
    open(os.path.join(ROOT, "assets", "site.css"), "w").write(CSS)
    open(os.path.join(ROOT, "assets", "site.js"), "w").write(JS)
    build_index()
    build_catalog_page()
    for p in PS:
        build_pdp(p)
    print(f"built index + {len(PS)} product pages")

if __name__ == "__main__":
    main()

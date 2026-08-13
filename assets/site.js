
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


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

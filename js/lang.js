/* ============================================================
   Abdulaziz Awal — language switcher
   Rewrites every [data-i18n] / [data-i18n-html] node from the
   table in js/i18n.js and flips the document to RTL for Arabic.
   ============================================================ */
(function () {
  "use strict";

  var root = document.documentElement;
  var dict = window.AAWAL_I18N || {};
  var STORE = "aawal.locale";
  var LANGS = ["en", "ar", "de"];

  var titles = {
    en: "Abdulaziz Awal — Junior Software Developer & Graphic Designer",
    ar: "عبدالعزيز عوض — مطوّر برمجيات ومصمّم جرافيك",
    de: "Abdulaziz Awal — Softwareentwickler & Grafikdesigner"
  };

  /* entity-safe: dictionary values keep &amp; and &copy; readable */
  var decoder = document.createElement("textarea");
  function decode(value) {
    decoder.innerHTML = value;
    return decoder.value;
  }

  function apply(locale) {
    if (LANGS.indexOf(locale) === -1) locale = "en";
    var t = dict[locale] || dict.en;

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (t[key] != null) el.textContent = decode(t[key]);
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-html");
      if (t[key] != null) el.innerHTML = t[key];
    });

    root.lang = locale;
    root.dir = locale === "ar" ? "rtl" : "ltr";
    document.title = titles[locale] || titles.en;

    var cur = document.querySelector(".nav-lang-cur");
    if (cur) cur.textContent = locale.toUpperCase();
    document.querySelectorAll(".nav-lang-menu [data-locale]").forEach(function (b) {
      b.setAttribute("aria-current", b.getAttribute("data-locale") === locale ? "true" : "false");
    });

    try { localStorage.setItem(STORE, locale); } catch (e) { /* private mode */ }
    if (window.AAWAL_startTyping) window.AAWAL_startTyping(locale);
  }

  window.AAWAL_applyLocale = apply;

  /* ---------- menu ---------- */
  var wrap = document.querySelector(".nav-lang");
  if (wrap) {
    var btn = wrap.querySelector(".nav-lang-btn");
    function setOpen(open) {
      wrap.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      setOpen(!wrap.classList.contains("open"));
    });
    wrap.querySelectorAll("[data-locale]").forEach(function (item) {
      item.addEventListener("click", function () {
        apply(item.getAttribute("data-locale"));
        setOpen(false);
      });
    });
    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  /* ---------- boot ---------- */
  var saved = null;
  try { saved = localStorage.getItem(STORE); } catch (e) { /* ignore */ }
  var param = null;
  try { param = new URLSearchParams(window.location.search).get("lang"); } catch (e) { /* ignore */ }
  var boot = (param && LANGS.indexOf(param) !== -1) ? param : saved;
  if (boot && boot !== "en") apply(boot);
  else if (window.AAWAL_startTyping) window.AAWAL_startTyping("en");
})();

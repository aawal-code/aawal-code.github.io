/* ============================================================
   Projects carousel: drag, arrows, keyboard, snap, RTL-aware.
   Works without it too: the rail is a plain horizontal scroller.
   ============================================================ */
(function () {
  "use strict";
  var rail = document.getElementById("projRail");
  if (!rail) return;
  var slides = Array.prototype.slice.call(rail.querySelectorAll(".proj-slide"));
  var prevBtn = document.querySelector('.proj-arrow[data-proj-dir="prev"]');
  var nextBtn = document.querySelector('.proj-arrow[data-proj-dir="next"]');
  var idxEl = document.getElementById("projIdx");
  if (!slides.length) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  function rtl() { return getComputedStyle(rail).direction === "rtl"; }
  function pad(dir) {
    var cs = getComputedStyle(rail);
    return parseFloat(dir === "rtl" ? cs.paddingRight : cs.paddingLeft) || 0;
  }
  function targetFor(i) {
    var r = rail.getBoundingClientRect(), s = slides[i].getBoundingClientRect();
    /* RTL scrolls toward negative scrollLeft, so align on the right edge there */
    if (rtl()) return rail.scrollLeft + (s.right - r.right) + pad("rtl");
    return rail.scrollLeft + (s.left - r.left) - pad("ltr");
  }
  function maxScroll() { return Math.max(0, rail.scrollWidth - rail.clientWidth); }
  function nearest() {
    var pos = Math.abs(rail.scrollLeft), max = maxScroll();
    if (pos <= 2) return 0;
    if (pos >= max - 2) return slides.length - 1;
    var best = 0, bestD = Infinity;
    for (var i = 0; i < slides.length; i++) {
      var d = Math.abs(targetFor(i) - rail.scrollLeft);
      if (d < bestD) { bestD = d; best = i; }
    }
    return best;
  }
  function pad2(n) { return n < 10 ? "0" + n : "" + n; }
  function sync() {
    var i = nearest();
    if (idxEl) idxEl.textContent = pad2(i + 1);
    if (prevBtn) prevBtn.disabled = i <= 0;
    if (nextBtn) nextBtn.disabled = i >= slides.length - 1;
  }
  function goTo(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    rail.scrollTo({ left: targetFor(i), behavior: reduce.matches ? "auto" : "smooth" });
  }

  if (prevBtn) prevBtn.addEventListener("click", function () { goTo(nearest() - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { goTo(nearest() + 1); });

  /* keyboard: arrows follow the reading direction */
  rail.addEventListener("keydown", function (e) {
    var back = rtl() ? "ArrowRight" : "ArrowLeft";
    var fwd = rtl() ? "ArrowLeft" : "ArrowRight";
    if (e.key === back) { e.preventDefault(); goTo(nearest() - 1); }
    else if (e.key === fwd) { e.preventDefault(); goTo(nearest() + 1); }
    else if (e.key === "Home") { e.preventDefault(); goTo(0); }
    else if (e.key === "End") { e.preventDefault(); goTo(slides.length - 1); }
  });

  /* pointer drag */
  var down = false, startX = 0, startScroll = 0, moved = 0, suppressClick = false;
  rail.addEventListener("pointerdown", function (e) {
    if (e.button !== 0 && e.pointerType === "mouse") return;
    down = true; moved = 0; startX = e.clientX; startScroll = rail.scrollLeft;
    rail.classList.add("is-dragging");
    if (rail.setPointerCapture) { try { rail.setPointerCapture(e.pointerId); } catch (err) {} }
  });
  rail.addEventListener("pointermove", function (e) {
    if (!down) return;
    var dx = e.clientX - startX;
    moved = Math.max(moved, Math.abs(dx));
    rail.scrollLeft = startScroll - (rtl() ? -dx : dx);
    if (moved > 6) e.preventDefault();
  });
  function endDrag() {
    if (!down) return;
    down = false;
    rail.classList.remove("is-dragging");
    suppressClick = moved > 8;
    goTo(nearest());
  }
  rail.addEventListener("pointerup", endDrag);
  rail.addEventListener("pointercancel", endDrag);
  rail.addEventListener("pointerleave", endDrag);
  rail.addEventListener("click", function (e) {
    if (suppressClick) { e.preventDefault(); e.stopPropagation(); suppressClick = false; }
  }, true);

  var raf = 0;
  rail.addEventListener("scroll", function () {
    if (raf) return;
    raf = requestAnimationFrame(function () { raf = 0; sync(); });
  }, { passive: true });
  window.addEventListener("resize", sync);

  /* the switcher re-renders text; keep the counter honest after it */
  window.AAWAL_syncCarousel = function () { sync(); };
  sync();
})();

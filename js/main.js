/* ============================================================
   Abdulaziz Awal — portfolio interactions
   ============================================================ */
(function () {
  "use strict";

  /* ---------- typed role line ---------- */
  var roles = [
    "Junior Software Developer",
    "Graphic Designer",
    "Full-Stack Web Developer",
    "React Native Developer"
  ];
  var typedEl = document.getElementById("typed");
  var roleIndex = 0, charIndex = 0, deleting = false;

  function tick() {
    var word = roles[roleIndex];
    if (!deleting) {
      charIndex++;
      typedEl.textContent = word.slice(0, charIndex);
      if (charIndex === word.length) {
        deleting = true;
        setTimeout(tick, 1800);
        return;
      }
      setTimeout(tick, 55 + Math.random() * 45);
    } else {
      charIndex--;
      typedEl.textContent = word.slice(0, charIndex);
      if (charIndex === 0) {
        deleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        setTimeout(tick, 350);
        return;
      }
      setTimeout(tick, 28);
    }
  }
  if (typedEl) setTimeout(tick, 900);

  /* ---------- nav background on scroll ---------- */
  var nav = document.getElementById("nav");
  function onScroll() {
    if (window.scrollY > 30) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- custom cursor ---------- */
  var dot = document.querySelector(".cursor-dot");
  var ring = document.querySelector(".cursor-ring");
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (fine && dot && ring) {
    var mx = -100, my = -100, rx = -100, ry = -100;
    document.addEventListener("mousemove", function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.left = mx + "px";
      dot.style.top = my + "px";
    });
    (function loop() {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      ring.style.left = rx + "px";
      ring.style.top = ry + "px";
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll("[data-hover]").forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("is-hover"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("is-hover"); });
    });
  }

  /* ---------- hero glow follows pointer ---------- */
  var hero = document.querySelector(".hero");
  var glow = document.querySelector(".hero-glow");
  if (hero && glow && fine) {
    hero.addEventListener("mousemove", function (e) {
      var r = hero.getBoundingClientRect();
      var x = ((e.clientX - r.left) / r.width) * 100;
      var y = ((e.clientY - r.top) / r.height) * 100;
      glow.style.left = x + "%";
      glow.style.top = y + "%";
    });
  }

  /* ---------- work card spotlight ---------- */
  document.querySelectorAll(".work-card").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });
})();

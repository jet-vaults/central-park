/* Central Park Elad — page behaviour (no dependencies) */
(function () {
  "use strict";

  var html = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var menu = document.getElementById("menu");

  /* ---------- hero entrance: wait for the hero image, then start ---------- */
  function loaded() {
    html.classList.add("is-loaded");
  }
  var heroImg = document.querySelector(".hero__media img");
  if (heroImg && !heroImg.complete) {
    heroImg.addEventListener("load", loaded, { once: true });
    heroImg.addEventListener("error", loaded, { once: true });
    setTimeout(loaded, 2500); /* never hold the page hostage */
  } else {
    requestAnimationFrame(loaded);
  }

  /* ---------- header state ---------- */
  function onScrollHeader() {
    header.classList.toggle("is-scrolled", window.scrollY > 40);
  }
  onScrollHeader();
  window.addEventListener("scroll", onScrollHeader, { passive: true });

  /* ---------- mobile menu ---------- */
  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    menu.classList.toggle("is-open", open);
    document.body.classList.toggle("menu-open", open);
    if (open) {
      var first = menu.querySelector("a");
      if (first) first.focus();
    }
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 1024px)").addEventListener("change", function (e) {
      if (e.matches) setMenu(false);
    });
  }

  /* ---------- staggered delays for grouped reveals ---------- */
  document.querySelectorAll("[data-stagger]").forEach(function (group) {
    var step = parseInt(group.getAttribute("data-stagger"), 10) || 90;
    var items = group.querySelectorAll(":scope > .reveal, :scope > * > .reveal, :scope .stagger-item");
    items.forEach(function (el, i) {
      el.style.setProperty("--d", i * step + "ms");
    });
  });

  /* ---------- scroll reveals ---------- */
  var targets = document.querySelectorAll(".reveal, .mask, .rings[data-observe], [data-observe]");
  if ("IntersectionObserver" in window && !reduce.matches) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.18, rootMargin: "0px 0px -8% 0px" }
    );
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("is-in"); });
  }

  /* ---------- gentle parallax on full-bleed bands (desktop only) ---------- */
  var bands = Array.prototype.slice.call(document.querySelectorAll(".parallax img"));
  var wide = window.matchMedia("(min-width: 1024px)");
  var ticking = false;

  function parallax() {
    ticking = false;
    if (reduce.matches || !wide.matches) {
      bands.forEach(function (img) { img.style.removeProperty("--py"); });
      return;
    }
    var vh = window.innerHeight;
    bands.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var progress = (r.top + r.height / 2 - vh / 2) / vh; /* -1 … 1 */
      var travel = r.height * 0.06;
      img.style.setProperty("--py", (-progress * travel).toFixed(1) + "px");
    });
  }
  function requestParallax() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(parallax);
    }
  }
  if (bands.length) {
    requestParallax();
    window.addEventListener("scroll", requestParallax, { passive: true });
    window.addEventListener("resize", requestParallax);
  }

  /* ---------- current section in nav ---------- */
  var navLinks = document.querySelectorAll(".nav a[href^='#']");
  var sections = Array.prototype.map.call(navLinks, function (a) {
    return document.querySelector(a.getAttribute("href"));
  });
  if ("IntersectionObserver" in window && sections.every(Boolean)) {
    var current = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          navLinks.forEach(function (a) {
            a.classList.toggle("is-active", a.getAttribute("href") === "#" + entry.target.id);
          });
        });
      },
      { rootMargin: "-45% 0px -50% 0px" }
    );
    sections.forEach(function (s) { current.observe(s); });
  }
})();

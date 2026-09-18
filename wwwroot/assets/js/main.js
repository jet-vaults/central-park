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
  var targets = document.querySelectorAll(".reveal, .fade, .rings, [data-observe]");
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
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
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
      var travel = r.height * 0.03;
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

/* ---------- site-plan magnifier + modals + gallery ---------- */
(function () {
  "use strict";
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");

  var map = document.querySelector(".map");
  if (map && fine.matches) {
    var img = map.querySelector("img");
    var lens = map.querySelector(".map__lens");
    var ZOOM = 3, LENS = 200;
    function move(e) {
      var r = img.getBoundingClientRect(), wr = map.getBoundingClientRect();
      var x = e.clientX - r.left, y = e.clientY - r.top;
      x = Math.max(LENS / 2, Math.min(x, r.width - LENS / 2));
      y = Math.max(LENS / 2, Math.min(y, r.height - LENS / 2));
      lens.style.left = (x - LENS / 2 + r.left - wr.left) + "px";
      lens.style.top = (y - LENS / 2 + r.top - wr.top) + "px";
      lens.style.backgroundImage = "url(" + (map.querySelector(".plan").getAttribute("data-lens-src") || img.currentSrc) + ")";
      lens.style.backgroundSize = (r.width * ZOOM) + "px " + (r.height * ZOOM) + "px";
      lens.style.backgroundPosition = (-(x * ZOOM - LENS / 2)) + "px " + (-(y * ZOOM - LENS / 2)) + "px";
    }
    map.addEventListener("mouseenter", function () { lens.style.display = "block"; });
    map.addEventListener("mouseleave", function () { lens.style.display = "none"; });
    map.addEventListener("mousemove", move);
  }

  document.querySelectorAll("[data-open]").forEach(function (b) {
    b.addEventListener("click", function () {
      var d = document.getElementById(b.getAttribute("data-open"));
      if (d && d.showModal) d.showModal();
    });
  });
  document.querySelectorAll("dialog.modal").forEach(function (d) {
    d.querySelectorAll("[data-close]").forEach(function (c) { c.addEventListener("click", function () { d.close(); }); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
  });

  var items = Array.prototype.slice.call(document.querySelectorAll(".gallery__item"));
  var gm = document.getElementById("gallery-modal");
  if (items.length && gm && gm.showModal) {
    var gimg = gm.querySelector("img"), cur = 0;
    function show(i) {
      cur = (i + items.length) % items.length;
      gimg.src = items[cur].getAttribute("data-full");
      gimg.alt = items[cur].getAttribute("data-alt") || "";
    }
    items.forEach(function (it, i) {
      it.addEventListener("click", function () { show(i); gm.showModal(); });
    });
    gm.querySelector("[data-prev]").addEventListener("click", function () { show(cur - 1); });
    gm.querySelector("[data-next]").addEventListener("click", function () { show(cur + 1); });
    gm.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") show(cur - 1);   /* RTL: right arrow = previous */
      if (e.key === "ArrowLeft") show(cur + 1);
    });
  }
})();

/* ---------- gallery carousel ---------- */
(function () {
  "use strict";
  var c = document.querySelector("[data-carousel]");
  if (!c) return;
  var track = c.querySelector(".carousel__track");
  var slides = Array.prototype.slice.call(track.children);
  var dots = document.querySelector(".carousel__dots");
  function perView() { return Math.max(1, Math.round(track.clientWidth / slides[0].getBoundingClientRect().width)); }
  function pages() { return Math.ceil(slides.length / perView()); }
  function current() { return Math.round(Math.abs(track.scrollLeft) / track.clientWidth); }
  function go(page) {
    var n = pages(); page = (page + n) % n;
    var x = page * track.clientWidth;
    track.scrollTo({ left: getComputedStyle(track).direction === "rtl" ? -x : x, behavior: "smooth" });
  }
  function buildDots() {
    dots.innerHTML = "";
    for (var i = 0; i < pages(); i++) { dots.appendChild(document.createElement("li")); }
    paint();
  }
  function paint() {
    var cur = current();
    Array.prototype.forEach.call(dots.children, function (d, i) { d.classList.toggle("is-active", i === cur); });
  }
  c.querySelector("[data-carousel-prev]").addEventListener("click", function () { go(current() - 1); });
  c.querySelector("[data-carousel-next]").addEventListener("click", function () { go(current() + 1); });
  track.addEventListener("scroll", function () { requestAnimationFrame(paint); }, { passive: true });
  window.addEventListener("resize", buildDots);
  buildDots();
})();

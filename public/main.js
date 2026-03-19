// Capabilities: progressive enhancement — add class so CSS activates tab behavior
const capSection = document.getElementById("capabilities");
if (capSection) capSection.classList.add("js-tabs-enhanced");

// Sticky nav: transparent on hero, blurred light on scroll
const nav = document.getElementById("nav");
window.addEventListener(
  "scroll",
  () => {
    nav.classList.toggle("scrolled", window.scrollY > 20);
  },
  {passive: true}
);

// Fade-in on scroll (staggered for grid children)
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      el.classList.add("visible");
      // Stagger sibling cards inside a bento grid
      const grid = el.closest(".bento-grid");
      if (grid) {
        grid.querySelectorAll(".fade-in:not(.visible)").forEach((card, i) => {
          card.style.transitionDelay = `${(i + 1) * 60}ms`;
          card.classList.add("visible");
        });
      }
      io.unobserve(el);
    });
  },
  {threshold: 0.1, rootMargin: "0px 0px -40px 0px"}
);
document.querySelectorAll(".fade-in").forEach((el) => io.observe(el));

// Pipeline track animation
const track = document.getElementById("pipeline-track");
if (track) {
  const pipelineObs = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        setTimeout(() => track.classList.add("animated"), 300);
        pipelineObs.disconnect();
      }
    },
    {threshold: 0.3}
  );
  pipelineObs.observe(track.closest(".pipeline"));
}

// Tab switching with keyboard support and roving tabindex
const tabBtns = document.querySelectorAll(".tab-btn");

function activateTab(btn) {
  tabBtns.forEach((b) => {
    b.classList.remove("active");
    b.setAttribute("aria-selected", "false");
    b.setAttribute("tabindex", "-1");
  });
  document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
  btn.classList.add("active");
  btn.setAttribute("aria-selected", "true");
  btn.setAttribute("tabindex", "0");
  document.getElementById(btn.getAttribute("aria-controls")).classList.add("active");
}

tabBtns.forEach((btn, idx) => {
  const arr = Array.from(tabBtns);
  btn.addEventListener("click", () => activateTab(btn));
  btn.addEventListener("keydown", (e) => {
    let target = null;
    if (e.key === "ArrowRight") {
      target = arr[(idx + 1) % arr.length];
      e.preventDefault();
    }
    if (e.key === "ArrowLeft") {
      target = arr[(idx - 1 + arr.length) % arr.length];
      e.preventDefault();
    }
    if (e.key === "Home") {
      target = arr[0];
      e.preventDefault();
    }
    if (e.key === "End") {
      target = arr[arr.length - 1];
      e.preventDefault();
    }
    if (target) {
      activateTab(target);
      target.focus();
    }
  });
});

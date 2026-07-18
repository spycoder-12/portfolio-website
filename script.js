// ---- API config ----
    // Point this at your local dev server while testing, then swap to your
    // deployed backend URL (e.g. "https://your-api.onrender.com") when you go live.
    const API_BASE = "http://127.0.0.1:8000";

    // ---- Fallback placeholder photos ----
    // Used only if the API can't be reached, so the page never looks broken
    // while the backend is down or you haven't uploaded real photos yet.
    const fallbackPhotos = [
      { cat: "weddings", seed: "wed-01", ratio: "800/1000", fno: "04A", exp: "f/1.8 · 1/200 · 35mm" },
      { cat: "portraits", seed: "port-01", ratio: "800/1000", fno: "11B", exp: "f/2.0 · 1/320 · 85mm" },
      { cat: "landscapes", seed: "land-01", ratio: "800/560", fno: "02C", exp: "f/8 · 1/60 · 24mm" },
      { cat: "weddings", seed: "wed-02", ratio: "800/1100", fno: "04B", exp: "f/2.2 · 1/160 · 50mm" },
      { cat: "events", seed: "evt-01", ratio: "800/560", fno: "18A", exp: "f/2.8 · 1/125 · 35mm" },
      { cat: "products", seed: "prod-01", ratio: "800/900", fno: "21A", exp: "f/5.6 · 1/80 · 100mm" },
    ];

    function renderGallery(photos, { isFallback = false } = {}) {
      const gallery = document.getElementById("gallery");
      gallery.innerHTML = "";

      if (!photos.length) {
        gallery.innerHTML =
          '<p class="mono" style="opacity:.6;padding:2rem 0;">No photos uploaded yet — add some via the admin panel.</p>';
        return;
      }

      photos.forEach((p) => {
        const div = document.createElement("div");
        div.className = "frame";
        div.dataset.cat = p.cat;

        // Real API photos have image_path/caption; fallback items use seed/ratio.
        const imgSrc = isFallback
          ? `https://picsum.photos/seed/${p.seed}/${p.ratio}`
          : `${API_BASE}/uploads/${p.image_path}`;
        const fno = isFallback ? p.fno : p.frame_no || "";
        const exp = isFallback ? p.exp : p.exposure || "";
        const caption = isFallback ? "" : p.caption || "";

        div.innerHTML = `
        <span class="frame-cat mono">${p.cat}</span>
        <img loading="lazy" src="${imgSrc}" alt="${caption || p.cat + ' photograph'}">
        <div class="frame-info">
          <span class="fno mono">${fno ? "NO. " + fno : ""}</span>
          <span class="fexp mono">${exp}</span>
        </div>`;
        div.addEventListener("click", () =>
          openLightbox(div.querySelector("img").src, [fno && `Frame ${fno}`, exp].filter(Boolean).join(" — ")),
        );
        gallery.appendChild(div);
      });
    }

    async function loadGallery() {
      try {
        const res = await fetch(`${API_BASE}/photos`);
        if (!res.ok) throw new Error(`API returned ${res.status}`);
        const data = await res.json();
        renderGallery(data, { isFallback: false });
      } catch (err) {
        console.warn("Could not load photos from API, showing placeholders:", err);
        renderGallery(fallbackPhotos, { isFallback: true });
      }
    }

    loadGallery();

    // ---- Filters ----
    document.getElementById("filters").addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;
      document
        .querySelectorAll(".filter-btn")
        .forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const cat = btn.dataset.cat;
      document.querySelectorAll(".frame").forEach((f) => {
        f.classList.toggle("hide", cat !== "all" && f.dataset.cat !== cat);
      });
    });

    // ---- Lightbox ----
    const lightbox = document.getElementById("lightbox");
    const lbImg = document.getElementById("lbImg");
    const lbCap = document.getElementById("lbCap");
    function openLightbox(src, cap) {
      lbImg.src = src;
      lbCap.textContent = cap;
      lightbox.classList.add("open");
    }
    document
      .getElementById("lbClose")
      .addEventListener("click", () => lightbox.classList.remove("open"));
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) lightbox.classList.remove("open");
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") lightbox.classList.remove("open");
    });

    // ---- Nav scroll state + roll counter ----
    const nav = document.getElementById("nav");
    const rollCounter = document.getElementById("rollCounter");
    const sections = document.querySelectorAll("section, header.hero");
    window.addEventListener("scroll", () => {
      nav.classList.toggle("scrolled", window.scrollY > 60);
      let idx = 1;
      sections.forEach((s, i) => {
        if (window.scrollY + window.innerHeight / 2 > s.offsetTop)
          idx = i + 1;
      });
      rollCounter.textContent =
        String(idx).padStart(2, "0") +
        " / " +
        String(sections.length).padStart(2, "0");
    });

    // ---- Reveal on scroll ----
    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) en.target.classList.add("in");
        });
      },
      { threshold: 0.12 },
    );
    document.querySelectorAll(".reveal").forEach((el) => obs.observe(el));

    // ---- Contact form ----
    async function handleSubmit(e) {
      e.preventDefault();
      const form = e.target;
      const btn = form.querySelector(".send-btn");
      const status = document.getElementById("formStatus");
      const originalBtnText = btn.textContent;

      const payload = {
        name: document.getElementById("fname").value.trim(),
        email: document.getElementById("femail").value.trim(),
        message: document.getElementById("fmsg").value.trim(),
        event_date: document.getElementById("fdate").value.trim() || null,
        website: document.getElementById("fwebsite").value, // honeypot, left empty by real users
      };

      btn.disabled = true;
      btn.textContent = "Sending...";
      status.textContent = "";

      try {
        const res = await fetch(`${API_BASE}/contact`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!res.ok) {
          const err = await res.json().catch(() => ({}));
          throw new Error(err.detail || `Request failed (${res.status})`);
        }

        btn.textContent = "Sent — Thank You";
        btn.style.background = "var(--paper)";
        status.textContent = "";
        setTimeout(() => {
          form.reset();
          btn.textContent = originalBtnText;
          btn.style.background = "";
          btn.disabled = false;
        }, 2200);
      } catch (err) {
        console.error("Contact form submission failed:", err);
        btn.textContent = originalBtnText;
        btn.disabled = false;
        status.textContent = "Something went wrong sending that — please try again or reach out directly.";
        status.style.color = "var(--rust)";
      }
    }

    // ---- Mobile nav (simple: burger scrolls reveal a stacked menu) ----
    const burger = document.getElementById("burger");
    const navLinks = document.querySelector(".nav-links");
    burger.addEventListener("click", () => {
      const open = navLinks.style.display === "flex";
      navLinks.style.display = open ? "none" : "flex";
      navLinks.style.position = "fixed";
      navLinks.style.top = "0";
      navLinks.style.left = "0";
      navLinks.style.right = "0";
      navLinks.style.background = "var(--ink)";
      navLinks.style.flexDirection = "column";
      navLinks.style.padding = "5rem 2rem 2rem";
      navLinks.style.gap = "1.6rem";
      navLinks.style.borderBottom = "1px solid var(--line)";
    });
    navLinks.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        if (window.innerWidth <= 860) navLinks.style.display = "none";
      }),
    );



# Lumice Destination Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the current Lumice visual design while adding a two-project gateway, a proposed Brian Head overview, and a paused Finland page at `/fn/`.

**Architecture:** Keep the project dependency-free and compatible with GitHub Pages. Each public route is a directly loadable HTML file, while shared visual tokens, ambient effects, accessibility behavior, and responsive rules live in `assets/site.css` and `assets/ambient.js`; Finland-specific translations remain isolated to `fn/finland.js`.

**Tech Stack:** Semantic HTML5, CSS, browser JavaScript, Python 3 standard-library contract tests, GitHub Pages.

## Global Constraints

- Preserve the live site's dark arctic palette, Playfair Display and Inter typography, full-bleed imagery, snowfall, aurora lighting, scroll reveals, and restrained glass treatments.
- Use ordinary anchor links so all navigation works without JavaScript.
- The Brian Head project must always be described as proposed; do not imply approval, construction, or a confirmed opening date.
- The Finland concept must be labeled paused; remove `Coming Soon`, `Winter 2026–2027`, email signup, and fabricated statistics.
- Do not claim Brian Head is the highest ski resort in the western United States. The supported claim is `Utah's highest base elevation`.
- Keep the site dependency-free and directly deployable to GitHub Pages.
- Support mobile layouts, keyboard focus, semantic landmarks, descriptive alt text, and `prefers-reduced-motion`.
- Decorative effects may fail without hiding content or navigation.

---

## File Map

- `index.html` — minimal Lumice gateway with two equal project links.
- `brian-head/index.html` — proposed Brian Head project overview.
- `fn/index.html` — relocated and corrected Finland concept page.
- `fn/finland.js` — Finland translations and language-menu behavior.
- `assets/site.css` — shared design tokens, layout primitives, effects, focus states, breakpoints, and reduced-motion rules.
- `assets/ambient.js` — optional snowfall, parallax, and reveal behavior guarded against missing elements and reduced-motion preferences.
- `assets/brian-head-concept.webp` — optimized AI concept rendering used on the gateway and Brian Head page.
- `IMG_1054.PNG`, `IMG_1055.PNG` — existing Finland images retained without modification.
- `tests/test_site.py` — dependency-free route, copy, accessibility, and asset contract tests.

---

### Task 1: Shared Visual and Ambient Foundation

**Files:**
- Create: `assets/site.css`
- Create: `assets/ambient.js`
- Create: `tests/test_site.py`

**Interfaces:**
- Consumes: Existing CSS and JavaScript behavior in `index.html`.
- Produces: CSS classes `.aurora`, `.site-header`, `.logo`, `.hero`, `.status`, `.project-link`, `.reveal`, and shared `assets/ambient.js` behavior for all routes.

- [ ] **Step 1: Write failing shared-asset tests**

Create `tests/test_site.py` with standard-library helpers and the first test class:

```python
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class SharedAssetTests(unittest.TestCase):
    def test_shared_assets_exist_and_cover_accessibility(self):
        css = read("assets/site.css")
        js = read("assets/ambient.js")

        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("--night:", css)
        self.assertIn("matchMedia('(prefers-reduced-motion: reduce)')", js)
        self.assertIn("document.getElementById('snowCanvas')", js)
        self.assertIn("if (!canvas", js)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test and verify the missing assets fail**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: ERROR because `assets/site.css` does not exist.

- [ ] **Step 3: Extract the shared visual system**

Create `assets/site.css`. Preserve the current values while introducing reusable tokens and accessibility rules:

```css
:root {
  --night: #030810;
  --ice: #7ec8e3;
  --text: #e0e8f0;
  --muted: rgba(168, 212, 240, 0.56);
  --line: rgba(126, 200, 227, 0.14);
  --glass: rgba(3, 8, 16, 0.56);
  --display: "Playfair Display", serif;
  --body: "Inter", sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { min-height: 100vh; overflow-x: hidden; background: var(--night); color: var(--text); font-family: var(--body); }
a { color: inherit; }
:focus-visible { outline: 2px solid var(--ice); outline-offset: 4px; }
#snowCanvas { position: fixed; inset: 0; z-index: 10; pointer-events: none; }
.aurora { position: fixed; inset: -50%; z-index: 1; pointer-events: none; opacity: .12; background: radial-gradient(ellipse at 20% 50%, rgba(72,209,204,.4), transparent 50%), radial-gradient(ellipse at 80% 50%, rgba(100,149,237,.3), transparent 50%); animation: auroraShift 20s ease-in-out infinite alternate; }
.site-header { position: fixed; top: 0; left: 0; right: 0; z-index: 100; display: flex; align-items: center; justify-content: space-between; padding: 22px clamp(20px, 4vw, 56px); background: linear-gradient(to bottom, rgba(3,8,16,.72), transparent); }
.site-header__brand { font-family: var(--display); letter-spacing: .32em; text-decoration: none; }
.site-header__home { font-size: .7rem; letter-spacing: .16em; text-decoration: none; text-transform: uppercase; color: var(--muted); }
.hero { position: relative; min-height: 100svh; display: grid; place-items: center; overflow: hidden; text-align: center; }
.hero__background { position: absolute; inset: 0; width: 100%; height: 115%; object-fit: cover; filter: brightness(.48) saturate(1.15) contrast(1.05); }
.hero::after { content: ""; position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(3,8,16,.18), rgba(3,8,16,.1) 42%, var(--night)); }
.hero__content { position: relative; z-index: 5; width: min(860px, calc(100% - 40px)); }
.logo { padding-left: .35em; font-family: var(--display); font-size: clamp(3.5rem, 10vw, 8rem); font-weight: 400; letter-spacing: .35em; color: rgba(210,230,248,.96); text-shadow: 0 0 60px rgba(126,200,227,.25); }
.tagline { margin-top: 12px; font-size: clamp(.72rem, 2vw, 1rem); font-weight: 300; letter-spacing: .42em; text-transform: uppercase; color: rgba(168,212,240,.68); }
.status { display: inline-flex; margin-top: 30px; padding: 9px 14px; border: 1px solid var(--line); border-radius: 6px; background: var(--glass); color: rgba(220,238,248,.88); font-size: .68rem; letter-spacing: .16em; text-transform: uppercase; backdrop-filter: blur(16px); }
.project-link { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; padding: 0 24px; border: 1px solid rgba(126,200,227,.24); border-radius: 8px; background: rgba(126,200,227,.14); color: rgba(230,244,252,.96); font-size: .72rem; letter-spacing: .16em; text-decoration: none; text-transform: uppercase; backdrop-filter: blur(16px); transition: background .3s, border-color .3s, transform .3s; }
.project-link:hover { transform: translateY(-2px); border-color: rgba(126,200,227,.45); background: rgba(126,200,227,.24); }
.reveal { opacity: 0; transform: translateY(36px); transition: opacity .8s, transform .8s; }
.reveal.visible { opacity: 1; transform: none; }

@keyframes auroraShift { to { transform: translate(3%, -2%) rotate(1deg) scale(1.03); } }

@media (max-width: 640px) {
  .site-header { padding: 18px 20px; }
  .logo { font-size: clamp(3rem, 17vw, 5rem); letter-spacing: .22em; padding-left: .22em; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .aurora, #snowCanvas { display: none; }
  .reveal { opacity: 1; transform: none; transition: none; }
  *, *::before, *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; }
}
```

- [ ] **Step 4: Extract guarded ambient behavior**

Create `assets/ambient.js` with current-site snowfall aesthetics, safe element checks, and reduced-motion handling:

```javascript
(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const canvas = document.getElementById('snowCanvas');

  if (!canvas || reducedMotion.matches) return;

  const context = canvas.getContext('2d');
  if (!context) return;

  const flakes = [];
  const resize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  resize();
  window.addEventListener('resize', resize, { passive: true });

  for (let index = 0; index < 90; index += 1) {
    flakes.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 2.2 + .5,
      speed: Math.random() * .6 + .2,
      drift: (Math.random() - .5) * .25,
      opacity: Math.random() * .45 + .16,
    });
  }

  const draw = () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (const flake of flakes) {
      context.beginPath();
      context.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
      context.fillStyle = `rgba(220, 235, 248, ${flake.opacity})`;
      context.fill();
      flake.x += flake.drift;
      flake.y += flake.speed;
      if (flake.y > canvas.height + 8) { flake.y = -8; flake.x = Math.random() * canvas.width; }
      if (flake.x > canvas.width + 8) flake.x = -8;
      if (flake.x < -8) flake.x = canvas.width + 8;
    }
    window.requestAnimationFrame(draw);
  };

  draw();
})();

(() => {
  const heroBackground = document.querySelector('[data-parallax]');
  if (heroBackground && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.addEventListener('scroll', () => {
      if (window.scrollY < window.innerHeight * 1.2) {
        heroBackground.style.transform = `translateY(${window.scrollY * .28}px)`;
      }
    }, { passive: true });
  }

  const reveals = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    reveals.forEach((element) => element.classList.add('visible'));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: .12 });
  reveals.forEach((element) => observer.observe(element));
})();
```

- [ ] **Step 5: Run the shared-asset tests**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: PASS for `SharedAssetTests`.

- [ ] **Step 6: Commit the shared foundation**

```bash
git add assets/site.css assets/ambient.js tests/test_site.py
git commit -m "refactor: add shared Lumice visual foundation"
```

---

### Task 2: Relocate and Correct the Finland Concept

**Files:**
- Create: `fn/index.html`
- Create: `fn/finland.js`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: `assets/site.css`, `assets/ambient.js`, `IMG_1054.PNG`, and `IMG_1055.PNG`.
- Produces: A directly loadable `/fn/` page and a Finland-only `setLang(lang: string): void` function.

- [ ] **Step 1: Add failing Finland contract tests**

Append to `tests/test_site.py`:

```python
class FinlandPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read("fn/index.html")
        cls.script = read("fn/finland.js")

    def test_finland_is_paused_and_not_marketed_as_opening(self):
        self.assertIn("Concept currently paused", self.html)
        for forbidden in ("Coming Soon", "Winter 2026", "Notify Me", "5,000", "Immersive Halls"):
            self.assertNotIn(forbidden, self.html)

    def test_finland_keeps_existing_language_support(self):
        for language in ("en", "fi", "sv", "de", "fr", "ja", "zh", "ru"):
            self.assertRegex(self.script, rf"\b{language}:\s*\{{")

    def test_finland_uses_shared_assets_and_navigation(self):
        self.assertIn('href="../assets/site.css"', self.html)
        self.assertIn('src="../assets/ambient.js"', self.html)
        self.assertIn('href="../"', self.html)
        self.assertIn('src="../IMG_1055.PNG"', self.html)
        self.assertIn('src="../IMG_1054.PNG"', self.html)
```

- [ ] **Step 2: Run the Finland tests and verify the missing route fails**

Run: `python3 -m unittest tests.test_site.FinlandPageTests -v`

Expected: ERROR because `fn/index.html` does not exist.

- [ ] **Step 3: Create the paused Finland page from the existing live page**

Move the current Finland semantic content into `fn/index.html`, use the shared header and effect assets, and preserve its two existing images. The hero must contain this exact status treatment:

```html
<header class="site-header">
  <a class="site-header__brand" href="../" aria-label="Lumice home">LUMICE</a>
  <a class="site-header__home" href="../">All projects</a>
</header>
<div class="aurora" aria-hidden="true"></div>
<canvas id="snowCanvas" aria-hidden="true"></canvas>
<main>
  <section class="hero" id="hero">
    <img class="hero__background" data-parallax src="../IMG_1055.PNG"
         alt="Concept rendering of luminous ice structures beneath the northern lights in Finland">
    <div class="hero__content">
      <h1 class="logo">LUMICE</h1>
      <p class="tagline" data-i18n="tagline">A Finnish Ice Experience</p>
      <p class="status" data-i18n="status">Concept currently paused</p>
    </div>
  </section>
</main>
```

Keep the current about copy, four concept features, gallery, footer, language dropdown, and scroll reveal. Remove the signup form, counter/statistics section, opening season, toast, and counter JavaScript completely.

- [ ] **Step 4: Isolate translations in `fn/finland.js`**

Move the current eight translation objects out of the old inline script. Add `status` to each language object; English must be `Concept currently paused`. Update text through `[data-i18n]` attributes and keep the dropdown behavior local to the Finland page:

```javascript
const translations = {
  en: { tagline: 'A Finnish Ice Experience', status: 'Concept currently paused' },
  fi: { tagline: 'Suomalainen jääelämys', status: 'Konsepti on tällä hetkellä tauolla' },
  sv: { tagline: 'En finsk isupplevelse', status: 'Konceptet är för närvarande pausat' },
  de: { tagline: 'Ein finnisches Eis-Erlebnis', status: 'Konzept derzeit pausiert' },
  fr: { tagline: 'Une expérience glacée finlandaise', status: 'Concept actuellement en pause' },
  ja: { tagline: 'フィンランドの氷の体験', status: '現在休止中のコンセプト' },
  zh: { tagline: '芬兰冰雪体验', status: '项目概念目前暂停' },
  ru: { tagline: 'Финский ледяной опыт', status: 'Концепция временно приостановлена' },
};

function setLang(lang) {
  const selected = translations[lang] || translations.en;
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.dataset.i18n;
    if (selected[key]) element.textContent = selected[key];
  });
  document.querySelectorAll('[data-lang]').forEach((button) => {
    button.classList.toggle('active', button.dataset.lang === lang);
  });
  try { localStorage.setItem('lumice-lang', lang); } catch (_) {}
}
```

Preserve the full existing translated about and feature strings rather than reducing translations to only the two keys shown in this structural example.

- [ ] **Step 5: Run Finland and full contract tests**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: all current tests PASS.

- [ ] **Step 6: Commit the Finland route**

```bash
git add fn/index.html fn/finland.js tests/test_site.py
git commit -m "feat: move Finland concept to paused route"
```

---

### Task 3: Build the Minimal Lumice Gateway

**Files:**
- Modify: `index.html`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: `assets/site.css`, `assets/ambient.js`, and later `assets/brian-head-concept.webp`.
- Produces: Root links `/brian-head/` and `/fn/`, each with visible text `Explore Project`.

- [ ] **Step 1: Add failing gateway contract tests**

Append to `tests/test_site.py`:

```python
class GatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read("index.html")

    def test_gateway_has_equal_project_links(self):
        self.assertIn('href="brian-head/"', self.html)
        self.assertIn('href="fn/"', self.html)
        self.assertEqual(self.html.count("Explore Project"), 2)
        self.assertIn("Brian Head", self.html)
        self.assertIn("Finland", self.html)

    def test_gateway_stays_neutral(self):
        self.assertNotIn("Coming Soon", self.html)
        self.assertNotIn("Concept currently paused", self.html)
        self.assertNotIn("Proposed for Brian Head", self.html)
        self.assertNotIn("signup-form", self.html)

    def test_gateway_uses_shared_assets(self):
        self.assertIn('href="assets/site.css"', self.html)
        self.assertIn('src="assets/ambient.js"', self.html)
        self.assertIn('src="assets/brian-head-concept.webp"', self.html)
```

- [ ] **Step 2: Run the gateway tests and verify the old Finland root fails**

Run: `python3 -m unittest tests.test_site.GatewayTests -v`

Expected: FAIL because the current root page has no Brian Head or Finland project links.

- [ ] **Step 3: Replace the root page with a minimal gateway**

Use the current site's font imports, full-screen hero, aurora, and snow. Keep content deliberately short:

```html
<main>
  <section class="hero gateway">
    <img class="hero__background" data-parallax src="assets/brian-head-concept.webp"
         alt="Concept rendering of a snowy mountain landscape illuminated at twilight">
    <div class="hero__content">
      <h1 class="logo">LUMICE</h1>
      <p class="tagline">Winter experiences shaped by ice, light, and place</p>
      <div class="gateway__projects" aria-label="Lumice projects">
        <article class="gateway__project">
          <p class="gateway__location">Southern Utah</p>
          <h2>Brian Head</h2>
          <a class="project-link" href="brian-head/">Explore Project</a>
        </article>
        <article class="gateway__project">
          <p class="gateway__location">Finnish Lapland</p>
          <h2>Finland</h2>
          <a class="project-link" href="fn/">Explore Project</a>
        </article>
      </div>
    </div>
  </section>
</main>
```

Add gateway-specific layout rules to `assets/site.css`: two equal translucent project panels on desktop, one-column stacking below 640px, and identical button declarations for both links.

- [ ] **Step 4: Run gateway tests**

Run: `python3 -m unittest tests.test_site.GatewayTests -v`

Expected: PASS even though the image file and Brian Head route are supplied by the next task; the string-level contract is now correct.

- [ ] **Step 5: Commit the gateway**

```bash
git add index.html assets/site.css tests/test_site.py
git commit -m "feat: add Lumice project gateway"
```

---

### Task 4: Generate the Brian Head Concept Image and Page

**Files:**
- Create: `assets/brian-head-concept.webp`
- Create: `brian-head/index.html`
- Modify: `assets/site.css`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: shared CSS/JS and the official Brian Head factual boundary defined in the design spec.
- Produces: a proposed Brian Head overview at `/brian-head/` and the shared gateway/Brian Head hero asset.

- [ ] **Step 1: Add failing Brian Head contract tests**

Append to `tests/test_site.py`:

```python
class BrianHeadPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read("brian-head/index.html")

    def test_page_is_unambiguously_proposed(self):
        self.assertIn("Proposed for Brian Head, Utah", self.html)
        self.assertGreaterEqual(self.html.lower().count("proposed"), 2)
        for forbidden in ("Coming Soon", "Winter 2026", "highest ski resort in the west", "5,000", "12 immersive"):
            self.assertNotIn(forbidden.lower(), self.html.lower())

    def test_page_uses_supported_brian_head_language(self):
        self.assertIn("Utah’s highest base elevation", self.html)
        self.assertIn("Southern Utah", self.html)
        self.assertIn("could include", self.html)

    def test_page_links_home_and_labels_concept_art(self):
        self.assertIn('href="../"', self.html)
        self.assertIn('src="../assets/brian-head-concept.webp"', self.html)
        self.assertRegex(self.html, r'alt="[^"]*[Cc]oncept rendering[^"]*"')

    def test_concept_image_is_web_optimized(self):
        image = ROOT / "assets/brian-head-concept.webp"
        self.assertTrue(image.exists())
        self.assertLess(image.stat().st_size, 1_500_000)
```

- [ ] **Step 2: Run the Brian Head tests and verify the route is missing**

Run: `python3 -m unittest tests.test_site.BrianHeadPageTests -v`

Expected: ERROR because `brian-head/index.html` does not exist.

- [ ] **Step 3: Generate the Brian Head concept art**

Use the `imagegen` skill with this production prompt:

```text
Create a wide 16:9 cinematic concept rendering for the Lumice website. Scene: a snowy high-elevation mountain setting inspired by Brian Head, Southern Utah, at deep blue twilight. In the middle distance, a tasteful temporary ice-and-light experience with sculptural frozen arches and softly illuminated ice walls; the attraction should feel plausible, elegant, family-friendly, and seasonal rather than like a fantasy castle. Surrounding terrain should evoke Brian Head's conifer-covered slopes and distant warm-toned Southern Utah cliffs, with heavy natural snow and subtle falling flakes. Dark navy, pale ice blue, and restrained warm amber lighting. Leave calm negative space near the center-left for white website typography. Photorealistic architectural visualization, atmospheric concept art, no logos, no text, no crowds, no ski lift branding, no northern lights. This is explicitly a proposal visualization, not documentation of an existing attraction.
```

Save the generated source outside the repository, visually inspect it, then convert it to `assets/brian-head-concept.webp` at quality 82 and a maximum width of 2400 pixels using the available image conversion runtime. Verify the final file is below 1.5 MB.

- [ ] **Step 4: Create the Brian Head page using the live Finland structure**

The hero and first overview section must use this copy:

```html
<section class="hero">
  <img class="hero__background" data-parallax src="../assets/brian-head-concept.webp"
       alt="Concept rendering of a proposed illuminated ice experience in the snowy mountains near Brian Head, Utah">
  <div class="hero__content">
    <h1 class="logo">LUMICE</h1>
    <p class="tagline">A Southern Utah Winter Experience</p>
    <p class="status">Proposed for Brian Head, Utah</p>
  </div>
</section>

<section class="about">
  <div class="about__content">
    <p class="about__label reveal">A proposed experience shaped by ice and altitude</p>
    <h2 class="about__heading reveal">Winter light in the mountains of Southern Utah</h2>
    <p class="about__text reveal">
      Lumice is exploring a seasonal ice-and-light experience for Brian Head, home to Utah’s highest base elevation and a winter landscape unlike anywhere else in the region.
    </p>
    <p class="about__text reveal">
      The proposed experience could include sculptural ice architecture, illuminated pathways, gathering spaces, and moments designed around the mountain setting. The concept is in development and subject to local review, site planning, and seasonal conditions.
    </p>
  </div>
</section>
```

Use four concept features labeled `Ice Architecture`, `Mountain Light`, `Seasonal Gathering`, and `Southern Utah Setting`. Every description uses conditional language. Add a source link in the footer to Brian Head Resort's official about page for the elevation statement.

- [ ] **Step 5: Run Brian Head and full contract tests**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit the Brian Head experience**

```bash
git add assets/brian-head-concept.webp assets/site.css brian-head/index.html tests/test_site.py
git commit -m "feat: add proposed Brian Head experience"
```

---

### Task 5: Browser Verification and Final Quality Pass

**Files:**
- Modify if required: `index.html`
- Modify if required: `brian-head/index.html`
- Modify if required: `fn/index.html`
- Modify if required: `fn/finland.js`
- Modify if required: `assets/site.css`
- Modify if required: `assets/ambient.js`
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: all public routes and shared assets from Tasks 1–4.
- Produces: verified desktop/mobile pages and a final regression test suite.

- [ ] **Step 1: Add the complete route and semantics test**

Append to `tests/test_site.py`:

```python
class WholeSiteTests(unittest.TestCase):
    def test_each_route_has_core_document_semantics(self):
        for route in ("index.html", "brian-head/index.html", "fn/index.html"):
            html = read(route)
            with self.subTest(route=route):
                self.assertRegex(html, r"<!DOCTYPE html>")
                self.assertIn('<meta name="viewport"', html)
                self.assertRegex(html, r"<title>[^<]+</title>")
                self.assertIn("<main", html)
                self.assertIn("</main>", html)
                self.assertNotRegex(html, r'href="javascript:')

    def test_decorative_canvas_is_hidden_from_assistive_technology(self):
        for route in ("index.html", "brian-head/index.html", "fn/index.html"):
            self.assertIn('id="snowCanvas" aria-hidden="true"', read(route))
```

- [ ] **Step 2: Run all contract tests before browser inspection**

Run: `python3 -m unittest tests/test_site.py -v`

Expected: all tests PASS.

- [ ] **Step 3: Serve all routes locally**

Run: `python3 -m http.server 4173 --bind 127.0.0.1`

Open and inspect:

- `http://127.0.0.1:4173/`
- `http://127.0.0.1:4173/brian-head/`
- `http://127.0.0.1:4173/fn/`

- [ ] **Step 4: Verify desktop behavior in the browser**

At a desktop viewport, confirm:

- Both gateway project entries have equal visual weight and identical `Explore Project` controls.
- The Brian Head page says `Proposed for Brian Head, Utah` above the fold.
- The Finland page says `Concept currently paused` above the fold.
- Snow, aurora, parallax, and reveal behavior resemble the original live page.
- All forward and back navigation links resolve without 404s.
- Finland's eight language options update the visible translated content.
- Browser console has no uncaught JavaScript errors.

- [ ] **Step 5: Verify mobile and reduced-motion behavior**

At 390 × 844, confirm no horizontal overflow, no clipped LUMICE letters, readable overlay text, stacked project links, and tap targets at least 44 pixels high. Emulate reduced motion and confirm snowfall, aurora animation, parallax, and reveal transitions are disabled while all content stays visible.

- [ ] **Step 6: Fix only issues discovered by verification**

For each discovered defect, add a focused assertion to `tests/test_site.py` when the behavior is statically testable, verify it fails, patch the smallest relevant file, and rerun the full suite. Do not add new content or redesign elements during this step.

- [ ] **Step 7: Run final verification**

Run:

```bash
python3 -m unittest tests/test_site.py -v
git diff --check
git status --short
```

Expected: all tests PASS, `git diff --check` prints nothing, and only intended implementation files are modified.

- [ ] **Step 8: Commit verified site**

```bash
git add index.html brian-head/index.html fn/index.html fn/finland.js assets/site.css assets/ambient.js assets/brian-head-concept.webp tests/test_site.py
git commit -m "test: verify Lumice destination site"
```

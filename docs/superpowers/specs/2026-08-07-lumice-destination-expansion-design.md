# Lumice Destination Expansion Design

Date: 2026-08-07

## Objective

Extend the current Lumice website without redesigning it. The finished static site will give public officials a credible overview of the Lumice concept, a proposed Brian Head project, and the paused Finland concept.

The existing live site's dark arctic palette, Playfair Display and Inter typography, full-bleed imagery, snowfall, aurora lighting, scroll reveals, and restrained glass treatments remain the visual source of truth.

## Public Routes

### `/`

The new root page is a short gateway rather than a full project page.

- Full-screen winter background using the current site's image treatment.
- Existing LUMICE wordmark treatment.
- Short parent-brand description: Lumice creates seasonal experiences from ice, light, and place.
- Two equal project links: `Brian Head` and `Finland`.
- Both links use the same neutral call to action: `Explore Project`.
- Brian Head links to `/brian-head/`; Finland links to `/fn/`.
- The gateway does not present either project as confirmed or currently operating.

### `/brian-head/`

This page adapts the existing Finland page structure and interaction model.

- Hero: `LUMICE` with the tagline `A Southern Utah Winter Experience`.
- Visible status: `Proposed for Brian Head, Utah`.
- The page describes an envisioned seasonal experience combining ice architecture, light, and Brian Head's mountain landscape.
- Supporting copy may accurately describe Brian Head Resort as having Utah's highest base elevation. It must not claim the resort is the highest in the western United States.
- The experience remains conceptual. Copy must use language such as `proposed`, `envisioned`, and `could include` rather than presenting features, dates, scale, partners, or approvals as confirmed.
- No fabricated counts for ice tonnage, halls, attendance, operating days, or dates.
- A navigation link returns to the Lumice gateway.

The page may reference Brian Head's high-elevation Southern Utah setting, winter snow, mountain views, and nearby red-rock landscape. The factual basis is Brian Head Resort's official description of Utah's highest base elevation and a resort range starting near 9,600 feet and rising to nearly 11,000 feet.

## `/fn/`

The current Finland page moves here with minimal structural change.

- Preserve its current images, translations, snowfall, aurora, parallax, scroll reveals, and overall layout.
- Add a clear `Concept currently paused` status near the hero content.
- Remove or replace `Coming Soon`, `Winter 2026–2027`, and the email notification form so the page does not imply an active opening plan.
- Remove the fabricated statistics section.
- Keep the page available from the root gateway but do not promote it as an active development.
- Add a navigation link back to the Lumice gateway.

## Visual Assets

- Reuse the current Finland imagery only on `/fn/`.
- Create one new wide AI concept image for Brian Head that shows a plausible illuminated ice experience within a snowy Southern Utah mountain setting.
- The Brian Head image must be atmospheric concept art, not a false documentary photograph of an existing attraction.
- Reuse a mountain-focused crop of the Brian Head concept image on the root gateway to keep the asset set small and align with the client's requested Southern Utah winter backdrop.
- Optimize all images for web delivery and provide descriptive alt text that identifies conceptual renderings where appropriate.

## Shared Implementation

The site remains dependency-free static HTML, CSS, and JavaScript for GitHub Pages.

- Shared colors, typography, focus styles, motion rules, snowfall behavior, and navigation styling live in shared assets rather than being copied across three large standalone files.
- Each route remains directly loadable and works without client-side routing.
- Project links are ordinary anchor links and remain usable without JavaScript.
- Decorative scripts fail quietly; all core content and navigation remain visible if JavaScript is disabled.
- The existing language selector is retained on the Finland page. The root and Brian Head pages are English-only for this version.

## Responsive and Accessibility Requirements

- Support desktop and mobile layouts without horizontal overflow.
- Maintain readable text contrast over imagery.
- Provide visible keyboard focus for every interactive element.
- Respect `prefers-reduced-motion` by disabling snowfall animation, parallax, and nonessential reveal motion.
- Use semantic headings, landmarks, links, and button types.
- Decorative canvas and overlays are hidden from assistive technology.

## Verification

- Load `/`, `/brian-head/`, and `/fn/` directly through a local static server.
- Confirm both gateway links and both back links resolve correctly.
- Confirm the Finland language selector still works after relocation.
- Confirm no active-opening language remains on the paused Finland page.
- Confirm every Brian Head status statement says the project is proposed.
- Check desktop and narrow mobile screenshots for readability and layout integrity.
- Check keyboard navigation, reduced-motion behavior, missing-image fallbacks, and JavaScript-disabled navigation.
- Validate that no unsupported counts, dates, partnerships, approvals, or superlative resort claims appear.

## Out of Scope

- Reservations, ticketing, payments, email signup, or a content-management system.
- Confirmed opening dates or construction specifications.
- Additional destination pages.
- A new brand identity or a redesign of the existing visual language.

# Dare Ministries website

A redesign of [dareministries.com](https://www.dareministries.com): a fast, static site with no CMS, hosted on GitHub Pages.

## Pages

| Path | Page |
|---|---|
| `/` | Home |
| `/about/` | Story, mission & vision, beliefs, team |
| `/ministries/` | All ministries |
| `/ministries/conferences/` | Conference timeline, 2015 onward |
| `/ministries/college/` | College Bible study |
| `/ministries/worship/` | Worship collective & internship |
| `/ministries/podcast/` | Yet I Will Rejoice |
| `/ministries/uganda/` | Uganda youth conference + sponsor calculator |
| `/resources/` | Study library, Truth in Two, apologetics, blog, newsletter archive, care |
| `/give/` | Giving funds |
| `/connect/` | Contact form, emails, map |
| `/privacy/` | Privacy policy |

## Editing

Page content lives in `src/pages/*.html`; the shared header and footer live in `src/layout.html`.
After editing, rebuild the HTML:

```sh
python3 tools/build.py
```

Then commit both `src/` and the generated folders. Pushing to `main` deploys automatically (see `.github/workflows/pages.yml`). During deploy, photos still hosted on the old WordPress site are downloaded into the published site by `tools/localize_images.py`.

Styles: `assets/css/style.css` (colors and fonts are CSS variables at the top). Interactions: `assets/js/main.js` (no dependencies).

Forms and giving hand off to Breeze ChMS (`dareministries.breezechms.com`). The contact form opens the visitor's email app, since a static site has no server.

## Research

`docs/SITE_INVENTORY.md` is the audit of the old site this redesign is based on.

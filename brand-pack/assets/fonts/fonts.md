# Mitra fonts

Two Google Fonts. Both free to use. No license fees, no self-hosting required.

## DM Sans (primary)

- **Specimen:** https://fonts.google.com/specimen/DM+Sans
- **Weights:** 400, 600, 700, 800

Use for headings, the wordmark, marketing display copy, buttons, labels, and most body text.

## Inter (secondary)

- **Specimen:** https://fonts.google.com/specimen/Inter
- **Weights:** 400, 500, 600, 700

Use for body text on product surfaces where Inter's denser glyph reads better at small sizes. Fallback for system UI.

## Loading on a web page

Single Google Fonts request that fetches both:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## CSS font stacks

```css
/* Brand display */
font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Secondary body */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

## For print / design tools

Download both font families from Google Fonts. Install into Figma, Adobe Creative Cloud, Canva, or whatever tool the marketer uses.

In Figma, both are available out of the box without installation if the Google Fonts plugin is enabled.

In Canva, both are available in the font picker without upload.

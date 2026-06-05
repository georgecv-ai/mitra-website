# Typography

Two Google Fonts. Both loaded site-wide.

## Primary: DM Sans

- All headings (h1 through h6)
- The "Mitra" wordmark
- Marketing display copy
- Buttons and labels
- Most body text on marketing pages

Weights in use: 400, 600, 700, 800.

DM Sans gives Mitra a calm, geometric, modern feel. It reads as confident without feeling corporate.

## Secondary: Inter

- Body text on product surfaces where Inter's denser glyph reads more cleanly at small sizes
- Fallback for system UI where DM Sans is unavailable

Weights in use: 400, 500, 600, 700.

## Loading

Both fonts come from Google Fonts. The site's `_layout.html` loads them in a single request:

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Marketers building external materials should use the same URL or download the fonts directly from [fonts.google.com/specimen/DM+Sans](https://fonts.google.com/specimen/DM+Sans) and [fonts.google.com/specimen/Inter](https://fonts.google.com/specimen/Inter).

## Type scale

A loose scale used across the marketing site. Not a strict design system, but the values that recur:

| Use | Size | Weight | Line height |
|---|---|---|---|
| Hero headline (display) | 1.95rem to 2.25rem (clamp scales by viewport) | 800 | 1.4 |
| Section heading (h2) | 1.7rem | 800 | 1.55 |
| Sub-heading (h3) | 1.45rem | 700 | 1.5 |
| Body text | 1rem | 400 | 1.7 |
| Buttons / pills | 0.9rem to 1.05rem | 700 | tight |
| Eyebrow labels | 0.7rem | 700 | letter-spaced (.14em), uppercase |
| Footnote / fine print | 0.85rem | 400 | 1.5 |

## Rules

- **Sentence case for headings.** No title case.
- **Italics for emphasis inside body copy** are fine. Italics for ornamental purposes (e.g., the "+ whatever yours loves" pill on the pain landing) are also fine when intentional.
- **All caps only on eyebrow labels** (the small letter-spaced labels above headlines), never on body copy or buttons.
- **Wordmark "Mitra" is always DM Sans 800** — never substitute a script font, never letterspace it, never set in another color besides teal `#2A9D8F` or white on a dark teal background.

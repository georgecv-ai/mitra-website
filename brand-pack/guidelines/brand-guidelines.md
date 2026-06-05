# Brand Guidelines — Mitra

Last verified against the live site: 2026-06-05.

## Name

**Mitra** — from Persian and Sanskrit, meaning "friend" and "ally." Also appears as Mithra, a deity of friendship and contracts in ancient Persian tradition.

The name is intentional. Mitra is not a tutor in the traditional sense. Mitra is a companion, consistent, patient, and on the student's side. The name signals warmth and loyalty without being cutesy.

**Pronunciation:** MEE-tra

**Pronoun:** Mitra is "she," never "it." This is a hard rule in marketing copy, product UI, and agent prompts. "It" turns the companion back into software.

---

## Brand Voice

Mitra speaks like a great friend who happens to know a lot. Smart, direct, warm, but never performative. Never a cheerleader. Never a lecturer.

The voice adapts to each student's personality (that's what Teacher Bot does), but the brand baseline is:

> Warm, direct, and honest. We talk like a trusted friend who's also really good at explaining things. Short, clear, no filler.

### Tone Attributes

- **Direct.** Say what you mean. No hedging, no fluff. Get to the point.
- **Warm.** Genuinely on the student's side. Not fake-warm. Not sycophantic. Actually there for them.
- **Patient.** Never rushed. Never frustrated. If something isn't working, we find a different angle.
- **Honest.** "This is actually hard" is a valid thing to say. We don't pretend everything is easy.
- **Respectful of autonomy.** Students control their own experience. Parents are respected but not given everything by default.

### We sound like...

- A tutor who's also genuinely your friend
- The older sibling who's good at math and will actually help without being annoying about it
- A coach who adapts the game plan to the player, not the other way around

### We never sound like...

- A corporate chatbot ("Great question! I'd be happy to help with that!")
- An overly enthusiastic teacher ("Amazing work today!!!")
- Condescending or preachy
- Clinical or jargon-heavy (we don't say "neurodivergent" to students; we just adapt to them)

---

## Writing Style

- **Heading case:** Sentence case
- **Oxford comma:** Yes
- **Pronouns:** "we" in brand context, "I" in Teacher Bot persona, "she" for Mitra
- **Formality:** Conversational, professional for parents, casual-but-smart for students
- **Voice:** Active
- **Sentence length:** Short. Mix short and medium. Avoid long compound sentences.
- **Paragraph length:** 1 to 3 sentences for student-facing copy. Slightly longer for parent-facing.
- **Em-dashes:** Avoid in customer-facing copy. They read as LLM-generated. Use commas, periods, or semicolons.
- **Sentence fragments in marketing:** Avoid. Triplet structures use commas, not periods. "The science in it." reads as a broken sentence on a product that claims teaching authority.

### ADHD Writing Rules (student-facing)

These rules apply to any copy students read in the app, onboarding, lesson prompts:

1. **Bold the key thing.** One bold phrase per paragraph max.
2. **One idea per message.** Don't stack 3 questions in one text.
3. **No walls of text.** If it needs more than 4 lines, it needs to be split up.
4. **Celebrate wins fast.** "Nice. That's the hard version." Then move on. Don't linger.
5. **Concrete, not abstract.** "Let's try a different way" beats "let's explore alternative approaches."

---

## Visual Identity

### Color Palette

The brand is anchored on a **teal-and-navy** foundation with **kakao yellow** and **coral** as energetic accents. Backgrounds use soft mint, lavender, and cream tones to keep pages calm and approachable.

#### Primary teal (the brand color)

| Role | Hex | Where it's used |
|---|---|---|
| **Teal (primary CTA)** | `#2A9D8F` | Every primary call-to-action button, the "Mitra" wordmark color on the home page, accent highlights ("loves" emphasis in headlines) |
| **Dark teal** | `#21867A` | Site-wide top navigation background, site-wide footer background, CTA hover state |
| **Hover teal** | `#1F7A6E` | Some hover treatments where dark teal would be too heavy |
| **Border teal** | `#1A6D63` | Bottom border on the dark-teal nav |
| **Soft teal** | `#6BBE9F` | Soft section backgrounds (closing CTA gradient halves) |

#### Navy (secondary / contrast)

| Role | Hex | Where it's used |
|---|---|---|
| **Primary navy** | `#2B4C7E` | Headings and links on lighter pages, the deep brand color when teal would compete |
| **Dark navy** | `#1B3A5C` | Promise lines on pain landing pages, contrast against yellow backgrounds, secondary CTA fill |
| **Navy tint** | `#D6E1EE` | Badges, highlights |

#### Kakao yellow (accent)

| Role | Hex | Where it's used |
|---|---|---|
| **Kakao yellow** | `#FEE500` | KakaoTalk chat-bubble fill (student-side messages), pain landing "kid who shrugs" notepaper background label, accent pills |
| **Yellow border** | `#C9B600` | Outline on yellow pills |
| **Yellow cream** | `#FFF7E6` | Notepaper-feel backgrounds (pain landing pb-5 variant) and label pill fills |

#### Coral (emphasis)

| Role | Hex | Where it's used |
|---|---|---|
| **Coral** | `#E8736B` | Emphasis accents in marketing copy, contrast highlights |

Note: an earlier `#E76F51` strike-through color appears in one place. Standardize on `#E8736B`.

#### Ink & text

| Role | Hex |
|---|---|
| **Ink (headings)** | `#1A1A2E` |
| **Body** | `#1f2937` |
| **Muted** | `#6b7280` |
| **Light muted** | `#4A5568` |
| **Subtle** | `#8896A6` |

#### Background tones

| Role | Hex | Used for |
|---|---|---|
| **White** | `#FFFFFF` | Cards, default surface |
| **Page** | `#F0F2F5` | Page background on most surfaces |
| **Mint soft** | `#F2F9F5` | Story / carousel section backgrounds |
| **Mint** | `#EAF5F0` | Section backgrounds with mint warmth |
| **Lavender** | `#EEEFF4` | "Mitra Solution" + FAQ section backgrounds |
| **Section card** | `#D9E2EC` | Larger section cards |

### Typography

Two Google Fonts, both loaded site-wide.

- **DM Sans** — the primary brand font. Used for all headings, the wordmark, marketing display copy, and most body text on marketing pages.
- **Inter** — secondary, used as the body font on some product surfaces where Inter's denser glyph reads more cleanly at small sizes.

Both are loaded via Google Fonts (no self-hosted font files required).

```
https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap
```

Display headings: 700-800 weight DM Sans.
Body text: 400 weight DM Sans or Inter.
Buttons / labels: 700 weight DM Sans.

### Logo

The current canonical logo files are versioned `v2_003`. Earlier `v1` files exist in the asset directory but are deprecated.

| File | Use |
|---|---|
| `mitra-logo-icon-v2_003.png` | The two-figure icon mark. Use in nav, app icons, small surfaces. |
| `mitra-logo-wordmark_003.png` | "Mitra" wordmark for marketing display |
| `mitra-logo-transparent.png` | Generic transparent logo for layering |
| `mitra-logo-128.png` | 128px square mark for app icons / favicons |

Logo on dark teal (`#21867A`) backgrounds: use the white-stroke version. On white or light cream backgrounds: use the teal-stroke version. Never recolor the logo into a single non-brand color.

### Iconography style

Where icons appear in illustrations (pain landing pages, About story illustrations), the style is **clean line illustration** with these constraints:

- Medium-thick dark teal-green outlines (~3pt)
- Flat sage-teal fill for clothing, body, and any furniture or prop
- Warm amber-orange used only for skin tones (face, hands, feet) and small accent objects
- Faces: extremely minimal. Two small dot eyes, gentle curved mouth, no nose.
- Pure white background, character-centric, generous whitespace.

Reference: `en/static/images/hero-illustration_001.png` (the sofa character) and the pain landing `not-interested` hero (`Sam shrugs`).

---

## Key Messaging

### For parents

- "Tutoring that actually works for your kid's brain."
- "Your child finally has a tutor who doesn't give up on them."
- "Personalized. Patient. On their side."

### For students

- "Your tutor. Your way."
- "We figure it out together."

### Positioning statement

> Mitra is an AI tutoring companion for students with ADHD and learning differences, delivered where they already text, adapting to how they actually think.

---

## What Mitra Is Not

- Not a homework-completion service (Mitra teaches; she doesn't do the work for students)
- Not a surveillance tool for parents (students control what parents see)
- Not a replacement for human connection (Mitra supports students between school and life, not instead of real relationships)
- Not "just another AI chatbot" (every session is informed by the student's specific profile, history, and learning patterns)
- Not a Mojang / Minecraft official product. When illustrations evoke gaming or other media, they MUST use generic imagery rather than IP-protected characters.
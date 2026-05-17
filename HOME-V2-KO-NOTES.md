# home-v2 (Korean) — Build Notes

Prototype Korean landing page. Source design: `tutor/docs/MITRA web v1.2.pdf`.
Page: `src/ko/home-v2.html` + `src/ko/home-v2.head.html` → route `/ko/home-v2`.

This log tracks everything that still needs the founder's input. Two lists:
**placeholders** (missing content/assets) and **choices** (decisions Praxis made
that George should confirm or override).

---

## Placeholders — need content or assets

| # | Where | What's needed |
|---|-------|---------------|
| P1 | Hero, Closing | App-screen mockup images. Currently dashed placeholder boxes. Export from Canva as PNG. |
| P2 | §2 미트라가 전합니다 | "POP UP 배너" card — the Canva said "connect with case study video recording + QR display." Content not finalized. What is this card meant to be? |
| P3 | §2 성장 대시보드 | Growth-dashboard screen mockup image. Placeholder box. Export from Canva. |
| P4 | §4 카톡 | Photo of a student with an iPad. Placeholder box. Export from Canva. |
| P5 | §4 카톡 | KakaoTalk channel QR. Placeholder box. NOTE: a QR may already exist at `static/images/KT/mitra-kakaotalk-qr.png` — confirm and wire it if so. |
| P7 | Header / Footer | "톡상담" button (from the Canva header) — needs the real KakaoTalk channel URL. Not yet wired; current page uses the site's standard nav/footer from the layout. |

*Resolved: ~~P6 comparison table~~ — reused the legacy `src/ko/index.html` table (2026-05-17).*

## Choices — Praxis decided, confirm or override

| # | Where | Choice made | Why |
|---|-------|-------------|-----|
| C1 | §8 FAQ | Selected 4 Q&As: ChatGPT 차이 / 무료 체험 / 과목 / 목표 전달. **Pricing Q omitted.** | Most powerful for a parent deciding to sign up; kept conversion-first and quiet on price (same call as the English page). George said these may change later. |
| C2 | §5 서연이 | Used the Seoyeon **Day 2** loneliness exchange from `tutor/docs/marketing/personas/seoyeon.md` (5 chat bubbles). | Day 2 is the tightest capture of the "혼자 있는 시간이 버거운" framing the section headline names. Other days available if you want a different excerpt. |
| C3 | §2 link cards | "작동 원리 보기" → `/ko/principles.html`; "부모님께 보기" → `/ko/for-parents.html`. | Best-fit existing Korean pages. Confirm targets. |
| C4 | CTAs | All CTAs (`7일 체험 신청하기`, `미트라와 채팅 시작하기`) point to `/ko/free-trial.html`. | Free-trial is the conversion page, same as the English prototype. "채팅 시작" could instead point at enroll or the KakaoTalk channel — confirm. |
| C5 | Copy | Cleaned obvious PDF-extraction artifacts to correct Korean: "성장하가는"→"성장해가는", "아0패드"→"아이패드", "락습"→"학습", "지치지않는"→"지치지 않는", "부모님으로"→"부모님으로부터". Copy otherwise verbatim from the Canva. | Extraction garbles, not real copy. Confirm none were intentional. |
| C6 | Palette | Green-forward palette (Mitra teal `#2A9D8F`, mint sections) matching the Canva, not the English page's navy/indigo. | The Canva design is green-forward; matched it. |

---

*Updated: 2026-05-17. Remove items as they are resolved.*

# Slides

Projector deck for the EIEF / Luiss workshop: fourteen ideas in four slots, all shown
on one example, the synthetic Card–Krueger panel (`examples/card-krueger-toy/`).

Each idea has the same frames: a plain-words definition, an everyday comparison, a
Card–Krueger example, and a "your turn" exercise. The clock is in
[`SCHEDULE.md`](../SCHEDULE.md).

| File | Use |
| --- | --- |
| [`workshop/workshop_slides.tex`](workshop/workshop_slides.tex) | **Main** Beamer source (title, idea map, then `slot1`–`slot4.tex`). |
| [`workshop/workshop_slides.pdf`](workshop/workshop_slides.pdf) | Built PDF for the projector (57 pages). |
| [`option_b_four_slots.md`](option_b_four_slots.md) | **Marp** copy of the same 57 slides. Use it if TeX is unavailable. |
| [`workshop/demo_map.md`](workshop/demo_map.md) | Each idea → its slides, demo and exercise files. |
| [`shared/beamer_preamble.tex`](shared/beamer_preamble.tex) | Theme and macros. |

| Slot | Clock (Rome) | Ideas |
| --- | --- | --- |
| 1 | Thu 26 Nov 2026 09:00–11:00 | C1 Agent vs chatbot · C2 Version control · C3 `AGENTS.md` · C4 To-do lists |
| 2 | Thu 11:00–12:00 + Fri 27 Nov 2026 09:30–10:15 | C5 Skills · C6 Create a Skill · C7 Sub-agent vs Skill · C8 Rule of thumb |
| 3 | Fri 10:15–12:00 | C9 Using sub-agents · C10 Orchestrating and swarms · C11 Issue-board swarm (launch) |
| 4 | Fri 14:00–16:30 | C11 review · C12 Goals · C13 Acceptance criteria · C14 Verification · Capstone · close |

## Presenting

Open `slides/workshop/workshop_slides.pdf` on the projector. To rebuild:

```bash
cd slides/workshop
latexmk -pdf -interaction=nonstopmode workshop_slides.tex
latexmk -c
```

You need TeX Live or MacTeX with Beamer, `booktabs`, `listings` and TikZ.

Fallback: preview [`option_b_four_slots.md`](option_b_four_slots.md) in VS Code / Cursor,
or export it with `marp option_b_four_slots.md`. Marp shows the two small diagrams
(C10 writer/checker, C14 fail–fix loop) as one line of text; the words match.

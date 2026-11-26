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
| 1 | Thu 26 Nov 2026 09:00–11:00 | Agent vs chatbot · Version control · `AGENTS.md` · To-do lists |
| 2 | Thu 11:00–12:00 + Fri 27 Nov 2026 09:30–10:15 | Skills · Create a Skill · Sub-agent vs Skill · Rule of thumb |
| 3 | Fri 10:15–12:00 | Using sub-agents · Orchestrating and swarms · Issue-board swarm (launch) |
| 4 | Fri 14:00–16:30 | Review · Goals · Acceptance criteria · Verification · Capstone · close |

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
(writer/checker, fail–fix loop) as one line of text; the words match.

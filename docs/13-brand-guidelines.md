# Aikya AI Brand Guidelines

Status: Foundation baseline

## Brand core

**Name:** Aikya AI  
**Meaning:** Unity; different languages brought into one understanding.  
**Primary tagline:** One World. One Understanding.  
**Brand statement:** Aikya is a bridge between languages, people, and knowledge.

## Mission and personality

Aikya makes information understandable regardless of language while respecting structure and privacy. The brand should feel intelligent, human, calm, trustworthy, accessible, and global-not futuristic for its own sake.

## Voice and tone

- Use plain, direct language and explain technical limitations honestly.
- Prefer “translate and understand” over inflated claims such as “perfect AI translation.”
- Be reassuring around privacy without making unearned compliance claims.
- Error messages state what happened, whether data is safe, and what the user can do next.
- Do not shame users for language, grammar, file quality, plan limits, or mistakes.
- Use sentence case for headings and controls.

Examples:

- Preferred: “Some text may not fit the original layout. Review the highlighted pages before export.”
- Avoid: “AI failed to generate perfect output.”
- Preferred: “This document will be sent to the selected translation provider.”
- Avoid: “100% private and secure” unless the exact claim is independently established.

## Naming system

Use Aikya AI for the company/platform and concise capability names when product breadth requires them:

- Aikya Translate
- Aikya Docs
- Aikya Vision
- Aikya Voice
- Aikya API
- Aikya Enterprise

Do not expose internal service names or provider brands as product architecture.

## Visual foundation

| Role | Token | Starting value | Intended use |
|---|---|---|---|
| Primary | Indigo 700 | `#4338CA` | primary action, brand anchors |
| Secondary | Sky 500 | `#0EA5E9` | progress and informational accents |
| Accent | Amber 500 | `#F59E0B` | sparing highlights, not body text on white |
| Success | Emerald 600 | `#059669` | completed states |
| Warning | Amber 700 | `#B45309` | review-needed states |
| Danger | Red 600 | `#DC2626` | destructive/error states |
| Neutral | Slate scale | design tokens | surfaces, borders, text |

These are seed colors, not an accessible palette by themselves. Every foreground/background pair must pass the WCAG contrast target. Status never relies on color alone.

## Typography

Choose a UI family with strong Latin and Devanagari support, then use script-aware fallbacks for Arabic, CJK, and other writing systems. The product may not claim font preservation when licensing or glyph coverage requires substitution. Maintain comfortable reading width, 16 px minimum body text target, and a consistent type scale.

## Logo direction

The mark should express connection or convergence without using flags, stereotyped scripts, speech-bubble clutter, or generic robot imagery. It must work as a single-color icon at browser-extension and favicon sizes. Final logo work requires trademark review and accessibility tests; no production logo is approved by this document.

## Imagery and motion

Show real multilingual work and document structure rather than abstract AI brains. Animations clarify state transitions and progress; respect `prefers-reduced-motion`. Never imply processing has finished through decorative motion before durable completion.

## Product copy conventions

- Languages use native name plus localized name where helpful.
- Display source, target, provider/privacy mode, retention, and quality warnings consistently.
- Use “source document” and “translated document,” not “input/output” in user copy.
- Destructive actions name the affected resource and retention consequence.
- AI actions are verbs-Explain, Summarize, Rewrite-and are visually distinct from Translate.

## Required review before launch

- Name, domain, and trademark availability.
- Logo/icon originality and licensing.
- Color/typography accessibility across light/dark themes.
- Localization and cultural review for initial markets.
- Product/marketing claims against actual benchmarks, provider terms, and security evidence.

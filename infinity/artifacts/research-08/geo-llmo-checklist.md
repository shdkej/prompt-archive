# GEO/LLMO Implementation Checklist

- intent: research-08
- date: 2026-05-23
- scope: Virtue, Knowledge Lab, Infinity
- constraint: research and implementation candidates only; no public site changes, deployments, or external sends

## Executive Takeaway

GEO/LLMO work should start with crawlability and source clarity, not with speculative "AI SEO" hacks. The high-confidence foundation is:

1. Make public pages fetchable without client-only rendering.
2. Publish clear `robots.txt` and `sitemap.xml`.
3. Add structured metadata/schema for entity, author, and canonical identity.
4. Add a conservative `/llms.txt` as a curated map, while treating it as voluntary and not guaranteed.
5. Validate from bot-like fetches and server logs before interpreting AI-answer visibility.

`llms.txt` is useful as a controlled reading map, especially for Knowledge Lab and Infinity docs, but it is not a replacement for normal SEO, robots policy, sitemaps, structured data, or human-visible source quality.

## Source Baseline

- `llms.txt` was proposed by Jeremy Howard on 2024-09-03 as a Markdown file at `/llms.txt` to help LLMs use websites at inference time. The proposal defines a required H1, optional blockquote summary, explanatory content, H2 sections, and Markdown link lists. Source: https://llmstxt.org/
- The neutral reference audited in 2026-05 positions `llms.txt` as voluntary, client-side, inference-oriented curation; it does not replace `robots.txt` or `sitemap.xml`. Source: https://llmtxt.info/
- OpenAI separates search and training crawlers: allow `OAI-SearchBot` for ChatGPT search visibility; disallowing `GPTBot` indicates content should not be used for foundation-model training. `ChatGPT-User` is user-triggered and robots rules may not apply. Source: https://developers.openai.com/api/docs/bots
- Google `Google-Extended` is a robots token, not a separate HTTP user agent. It controls use for Gemini model training and Gemini/Vertex grounding, and does not affect Google Search inclusion or ranking. Source: https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
- Google robots handling still matters: `robots.txt` must be top-level plain text; `Sitemap:` entries are supported; disallowed pages can still be indexed as URLs without snippets, so use indexing controls separately when needed. Source: https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- Anthropic documents `ClaudeBot` robots controls, supports non-standard `Crawl-delay`, and recommends robots rules over IP blocking for opt-out. Source: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Google structured data should follow Google Search Central behavior for Search eligibility, even when using schema.org vocabulary. Required/recommended fields should be accurate and tested with Rich Results Test. Source: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data

## Priority Checklist

### P0 - Crawl and Render Access

- Verify public pages return meaningful HTML to a simple HTTP fetch, not only a JavaScript shell.
- Confirm `robots.txt` is reachable at the production root for each public host.
- Confirm CDN/security settings do not silently block desired AI/search bots despite permissive `robots.txt`.
- Keep login-only, private, staging, admin, and internal routes disallowed or unavailable.
- For sites intended to appear in AI answers, allow search/answer crawlers separately from training crawlers where providers support that distinction.

Recommended robots stance for public marketing/docs pages:

```txt
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Allow: /

User-agent: ClaudeBot
Allow: /
Crawl-delay: 1

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Adjust `GPTBot`, `Google-Extended`, and `ClaudeBot` based on content-licensing preference. Search visibility and training permission are not the same policy decision.

### P1 - Sitemap, Canonical, and Metadata

- Publish a sitemap containing only canonical public URLs.
- Add canonical URLs on every public page.
- Add stable title/description metadata that names the product/site and the page purpose.
- Add Open Graph/Twitter metadata for share previews.
- Avoid duplicate URLs for the same page state; redirect or canonicalize variants.
- Include `lastmod` in sitemaps for docs/wiki pages where freshness matters.

### P1 - Structured Data and Trust Signals

- Add `WebSite`/`Organization` or `Person` schema where there is a stable public entity.
- For docs/wiki content, use `Article`, `TechArticle`, or `WebPage` only where the visible page actually supports those claims.
- Include visible author/source/date/update information for public editorial or research pages.
- Link to source documents, GitHub repos, changelogs, and contact/about pages from crawlable pages.
- Do not add fake ratings, fake author credentials, or schema that is not visible or supported on the page.

### P1 - `/llms.txt`

- Publish `/llms.txt` as a concise map of the highest-value public pages.
- Keep it short enough to be useful in a context window; link to canonical pages or Markdown versions.
- Use absolute HTTPS URLs.
- Include sections such as `Docs`, `Product`, `Research`, `Changelog`, and `Optional`.
- Put secondary or large context in `## Optional`.
- Validate the format with a parser or validator before deployment.
- Treat `/llms-full.txt` or expanded context files as optional and only for stable docs, not frequently changing app state.

Starter template:

```md
# Site Name

> One-sentence source-of-truth description: what this site is, who it serves, and what its public pages can be cited for.

## Core

- [Overview](https://example.com/): Product/site overview and primary canonical entry point.
- [Docs](https://example.com/docs/): Public documentation index.

## Trust

- [About](https://example.com/about/): Ownership, contact, and source context.
- [Changelog](https://example.com/changelog/): Public update history.

## Optional

- [Archive](https://example.com/archive/): Lower-priority historical material.
```

### P2 - LLM Answer Visibility

- Create pages that answer entity-level questions directly: what it is, who it is for, how it works, constraints, pricing/status if public, and source links.
- Prefer stable, linkable explanatory pages over only app screens.
- Use clear headings and short answer-like paragraphs on public docs.
- Make important claims citeable: link to evidence, changelogs, docs, or source code.
- Track whether answers cite the canonical page, an outdated third-party page, or no source.
- Do not infer product-market or conversion success from AI visibility alone.

## Engine-Specific Notes

| Surface | What to configure | Main caution |
| --- | --- | --- |
| ChatGPT Search | `OAI-SearchBot` allow, fetchable HTML, canonical URLs, sitemap | `GPTBot` training permission is separate from `OAI-SearchBot`; user-triggered `ChatGPT-User` may not follow robots in the same way. |
| OpenAI training | `GPTBot` allow/disallow | Allow only if training use is acceptable for that content. |
| Google Search/AI surfaces | normal Googlebot crawlability, sitemap, structured data, canonical; `Google-Extended` policy | `Google-Extended` does not control normal Google Search ranking/inclusion. |
| Gemini/Vertex grounding/training | `Google-Extended` allow/disallow | It is a robots token; logs may show normal Google crawlers rather than a separate Google-Extended UA. |
| Claude | `ClaudeBot` robots rule and optional `Crawl-delay` | IP blocking can interfere with opt-out detection. |
| Perplexity and other answer engines | public crawlability, sitemap, structured pages, citations | Bot behavior is less uniformly documented; verify with logs and do not rely only on robots declarations. |

## Project Application

### Virtue

Current local signal: `src/app/layout.tsx` has basic title/description metadata, but no `robots.txt` or `sitemap` file was found in the shallow app scan.

Recommended sequence:

1. Add production `robots.txt` with explicit policy for OAI-SearchBot, GPTBot, Google-Extended, ClaudeBot, and sitemap location.
2. Add sitemap generation for public routes: `/`, `/add`, `/deeds`, `/dex`, `/me` only if these are intended to be public and meaningful without user state. If app routes are user-state screens, create separate public explanation pages instead.
3. Improve metadata with canonical site URL, Open Graph, and a product-level description in Korean and/or English.
4. Add an about/source page explaining Virtue's premise, status, and boundaries. This is more useful to answer engines than private app screens.
5. Add `/llms.txt` only after public canonical pages exist; otherwise it will just point bots at thin app routes.

### Knowledge Lab

Current local signal: `agent-wiki` appears to be a docs/wiki Next/Fumadocs site with static output, but no shallow `robots.txt` or `sitemap` file was found.

Recommended sequence:

1. Add `robots.txt` and sitemap for public wiki/docs pages.
2. Generate `/llms.txt` from the docs index, with `## Docs`, `## Research`, `## Logs`, and `## Optional`.
3. Prefer Markdown or clean static HTML versions for each important doc.
4. Add author/source/update metadata to research pages.
5. Add `TechArticle` or `Article` schema only for pages with visible title, author/source, and dates.

Knowledge Lab is the best first target for `llms.txt` because the content is naturally documentation-like and source-citation oriented.

### Infinity

Current local signal: Infinity is currently represented inside `prompt-archive`; no public web surface was found in the shallow scan.

Recommended sequence:

1. Do not publish operational/private intent files directly.
2. If a public Infinity page exists later, publish only a curated public explainer and selected public archive pages.
3. Use `/llms.txt` to point to public concepts, architecture, and changelog, not live intent queues or reports that may include sensitive local context.
4. Keep `robots.txt` restrictive by default until there is an explicit public information architecture.

## Verification Gates Before Any Public Change

- `curl -I https://domain/robots.txt` returns 200 and `text/plain`.
- `curl https://domain/robots.txt` shows intended AI/search rules and `Sitemap:`.
- `curl https://domain/sitemap.xml` returns canonical production URLs.
- `curl https://domain/llms.txt` returns valid Markdown, absolute URLs, and no private/internal links.
- Fetch key pages with JavaScript disabled or a simple HTTP client and confirm meaningful title, heading, and body text are present.
- Run Google Rich Results Test for structured pages.
- Check server/CDN logs for 403/challenge responses to desired crawlers after rollout.
- Ask target answer engines neutral questions and record whether they cite the canonical page; repeat weekly, not immediately after deploy only.

## Candidate Work Items

| Priority | Project | Candidate | Permission | Local needed |
| --- | --- | --- | --- | --- |
| P0 | Knowledge Lab | Add `robots.txt`, sitemap, and `/llms.txt` generated from docs index | L1/L2 if push | yes |
| P0 | Virtue | Decide public vs app-state pages; add public explainer if needed | L1/L2 if push | yes |
| P1 | Virtue | Add robots/sitemap/canonical/OG metadata for production host | L1/L2 if push | yes |
| P1 | Knowledge Lab | Add visible source/update metadata to major docs pages | L1/L2 if push | yes |
| P2 | Infinity | Draft public-safe Infinity explainer and publication boundary | L0/L1 draft | maybe |
| P2 | All | Create monthly AI-answer visibility observation sheet | L1 docs only | yes |

## Non-Goals and Red Lines

- No public deployments from this research intent.
- No external outreach or submissions.
- No automated AI-answer scraping that violates provider terms.
- No training-crawler allow policy without content-owner decision.
- No publication of private Infinity intent/report content.
- No claims that `/llms.txt` guarantees answer-engine citation or ranking.

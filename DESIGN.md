# Sam Samuel Design

> This is the product design judgment layer.
> `BRAND.md` defines why Sam Samuel exists.
> `DESIGN_SYSTEM.md` defines how the interface is implemented.
> This document defines whether a product feels right before implementation details.

## Role

Sam Samuel design exists to make people start.

The product should not impress users with complexity. It should reduce the vague distance between "I want to make something" and "I can begin now." Good design here is not decorative minimalism. It is edited clarity: understanding a broad possibility space, then leaving only the parts that help the user move.

Use this document when judging:

- New app concepts
- Product flows and first screens
- Landing pages and onboarding
- Copy, empty states, and error messages
- App-making content for Threads or Instagram
- Whether a product still feels like Sam Samuel after features are added

## Source Documents

- `BRAND.md`: brand promise, tone, emotional promise, anti-positioning
- `DESIGN_SYSTEM.md`: tokens, components, accessibility, implementation rules
- `LLM.md`: maker identity, working philosophy, communication preference
- `WORLD_TRAVEL_PROJECT.md`: travel insight to app-making content loop

## Core Promise

Make producers.

That means the design should help a person:

1. See what matters.
2. Understand the next action.
3. Try without feeling judged.
4. Keep enough ownership to feel like the product is helping, not taking over.
5. Want to come back tomorrow.

The user already has the will to make something. Sam Samuel design adds a usable path.

## Design North Star

Warm clarity.

The product should feel like a slightly more experienced person sitting nearby. It can suggest, organize, and reduce noise, but it should not lecture. It should feel calm, capable, and human.

If a screen feels efficient but cold, it is drifting.
If a screen feels warm but unclear, it is unfinished.
If a screen feels simple because nothing is there, it is empty, not edited.

## Product Feeling

Sam Samuel products should feel like:

- A tool that waits with the user
- A workspace where making feels possible
- A quiet guide that knows the next step
- A place that is easy to reopen
- A product that helps the user produce their own output, not admire the tool

They should not feel like:

- A cold enterprise dashboard
- A feature catalog
- A trend-driven AI toy
- A teacher grading the user
- A blank minimalist page with no real help
- A generic SaaS page wearing warm colors

## Design Principles

### 1. Make The First Action Obvious

The first screen should answer one question quickly:

What can I do here right now?

The answer does not need to be loud, but it must be visible. If the user needs to read a paragraph before acting, the screen is carrying too much explanation.

Good:

- One clear primary action
- A short reason for that action
- A visible example, placeholder, or starting point

Avoid:

- Multiple equal CTAs
- Abstract welcome copy
- Empty states that only say nothing exists yet

### 2. Leave The User As The Main Character

The interface should make the user's content, intent, or decision the center.

AI, automation, and templates are support structures. They should not become the product's main performance. The user should feel, "This helped me make my thing," not "The tool made something instead of me."

Good:

- Show the user's material prominently
- Make edits reversible and understandable
- Explain suggestions through the user's goal

Avoid:

- Overly magical generation flows
- Hiding the reason behind suggestions
- Replacing the user's judgment with opaque automation

### 3. Edit From 100 To 10

Sam Samuel simplicity is not a lack of ideas. It is the result of filtering.

Before removing something, understand what it was trying to solve. Before adding something, ask whether it reduces confusion or merely increases capability.

The right 10% should feel strong enough to carry the product.

Good:

- Fewer controls with stronger defaults
- Progressive detail after the first action
- Feature depth hidden behind clear moments

Avoid:

- A thin MVP that has no guidance
- Settings exposed before the user has context
- Treating fewer UI elements as automatically better

### 4. Use Structure Before Explanation

Users should understand the screen from layout, hierarchy, and labels before long text explains it.

Copy can help, but copy should not rescue a confused structure.

Good:

- Group related things by proximity
- Give one element clear visual priority
- Use examples instead of instructions when possible

Avoid:

- Long instructional blocks
- Equal-weight cards everywhere
- Tooltips that carry core understanding

### 5. Make Warmth Functional

Warmth is not decoration. It should reduce tension.

Warm surfaces, rounded forms, soft motion, and friendly copy matter because they make the first try feel less risky. The user should feel invited, not processed.

Good:

- Soft but readable contrast
- Tactile buttons and inputs
- Empty states that offer a starting handle
- Error messages with a recovery path

Avoid:

- Pure white emptiness
- Pure black shadows
- Default cold-blue focus rings
- Formal system messages

### 6. Design For Return

The emotional promise is "계속 쓰고 싶다."

A good Sam Samuel product does not need to shock the user on first use. It should become comfortable enough to revisit. That means stable navigation, predictable rhythm, and a sense that yesterday's work still has a place.

Good:

- Clear continuity from previous work
- Calm visual rhythm
- Fast paths to repeated actions
- Small moments of progress

Avoid:

- One-time wow effects
- Constant layout novelty
- Hidden history
- Making repeat use feel like starting over

## Screen Judgment Tests

Use these tests before discussing colors or component details.

### 1. Five-Second Test

After five seconds, can the user answer:

- What is this screen for?
- What matters most here?
- What should I do next?

If not, fix hierarchy before styling.

### 2. Warmth Test

Does the screen feel like a person made it for another person?

Check:

- Copy tone
- Empty states
- Error states
- Waiting/loading states
- First-use experience

### 3. Editing Test

Is this the right 10 from 100?

If the screen is sparse, ask whether it is refined or just under-designed. If it is dense, ask whether every part earns its place.

### 4. Ownership Test

Does the user remain the maker?

The product can guide, automate, and suggest, but it should leave a visible place for user judgment.

### 5. Return Test

Would the user want to reopen this tomorrow?

Look for comfort, continuity, and low friction. A product that is impressive once but tiring later fails this test.

## Screen Rules

- One primary action per screen.
- Put the strongest value above the fold.
- Show "why" before "how."
- Let the user's content become the visual center.
- Reveal advanced controls after intent is clear.
- Prefer examples, previews, and defaults over abstract instructions.
- Use empty states as starting points, not dead ends.
- Keep repeated actions reachable.
- Do not make all cards, buttons, or sections equal weight.
- If visual hierarchy fails, other polish does not matter yet.

## Visual Direction

The visual signature is Warm Tool.

It should feel minimal, tactile, and calm. It can borrow from Braun's tool clarity, Kyobo's warm space, and Tsutaya's curated flow, but it should not become retro, bookstore-themed, or decorative.

### Fixed Direction

- Light mode is the default first impression.
- Pretendard is the default typeface.
- Shapes are soft, but not childish.
- Surfaces have depth, but not heavy shadows.
- Backgrounds are warm and slightly textured by tone, not pure white.
- Motion should feel like waiting with the user, not showing off.
- Accessibility is part of the brand promise.

### Avoid

- Pure `#FFFFFF` as the dominant feeling
- Pure `#000000` shadows or dark mode
- Cold default blue as the main interaction color
- Purple-blue AI SaaS gradients as a default identity
- Excessive glassmorphism
- Decorative orbs and vague atmospheric backgrounds
- Over-rounded components that feel toy-like
- Dense enterprise table-first layouts unless the product truly needs them

## Copy And Tone

Sam Samuel copy uses soft Korean honorifics.

It should sound like a capable person nearby:

- "이렇게 해보세요."
- "여기부터 시작하면 돼요."
- "이 부분만 먼저 정리해볼까요?"
- "문제가 생겼어요. 다시 시도할 수 있게 정리해둘게요."

Avoid:

- "하십시오"
- "수행하세요"
- "오류가 발생했습니다"
- "사용자는 다음 절차를 따라야 합니다"
- Over-explaining obvious UI
- Teaching tone that makes the user feel behind

### Copy Rules

- Use short sentences.
- Lead with the reason before the action.
- Give one next handle at a time.
- Explain errors with cause and recovery.
- Prefer concrete words over abstract brand language.
- Remove filler before adding polish.

## App-Making Content Rule

For travel-era app building, design should also create shareable evidence.

The content loop is:

1. Travel observation or friction
2. Product insight
3. App change
4. Screen before/after or short demo
5. Next user reaction to check

This should not look like a developer diary. It should show a product growing from lived friction.

Good Threads/Instagram material:

- A photo of the real situation
- A short screen recording of the changed app
- One plain sentence: "이 장면 때문에 기능 하나를 고쳤습니다."
- A small before/after comparison

Avoid:

- Long technical changelogs
- Generic "building in public" posts
- Showing code when the user-facing judgment is the real story
- Travel photos disconnected from the product decision

## Product Review Checklist

Before shipping or sharing a Sam Samuel product surface, check:

- Is the first action visible within five seconds?
- Does the screen have one clear main character?
- Did we leave the right 10, not just remove things?
- Does the user's content or intent stay central?
- Can the user recover from an error without feeling blamed?
- Does the copy sound like a nearby senior, not a manual?
- Is warmth helping clarity instead of decorating confusion?
- Does the interface explain itself through structure?
- Would the user want to come back tomorrow?
- Does this still support "생산자를 만든다"?

## Relationship To Other Documents

Use the documents in this order:

1. `BRAND.md`: Why should this exist?
2. `DESIGN.md`: What should this feel like?
3. `DESIGN_SYSTEM.md`: How should it be built?

If `DESIGN_SYSTEM.md` gives a token rule but the product still feels cold, revisit `DESIGN.md`.
If `DESIGN.md` feels vague, revisit `BRAND.md`.
If both are clear, implement through `DESIGN_SYSTEM.md`.

## Final Standard

A Sam Samuel product should make the user think:

I can start now, and I want to come back tomorrow.

---
name: Photos Research
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dae0'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4fa'
  surface-container: '#ebeef4'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#dfe3e8'
  on-surface: '#181c20'
  on-surface-variant: '#414754'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f7'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#006e2c'
  on-secondary: '#ffffff'
  secondary-container: '#86f898'
  on-secondary-container: '#00722f'
  tertiary: '#b81d17'
  on-tertiary: '#ffffff'
  tertiary-container: '#dc392c'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#89fa9b'
  secondary-fixed-dim: '#6ddd81'
  on-secondary-fixed: '#002108'
  on-secondary-fixed-variant: '#005320'
  tertiary-fixed: '#ffdad5'
  tertiary-fixed-dim: '#ffb4a9'
  on-tertiary-fixed: '#410001'
  on-tertiary-fixed-variant: '#930004'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#dfe3e8'
typography:
  display-lg:
    fontFamily: Roboto Flex
    fontSize: 44px
    fontWeight: '500'
    lineHeight: 52px
    letterSpacing: -0.5px
  headline-lg:
    fontFamily: Roboto Flex
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
    letterSpacing: -0.25px
  headline-lg-mobile:
    fontFamily: Roboto Flex
    fontSize: 26px
    fontWeight: '500'
    lineHeight: 32px
  headline-md:
    fontFamily: Roboto Flex
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
  title-lg:
    fontFamily: Roboto Flex
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
  title-md:
    fontFamily: Roboto Flex
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 22px
  body-lg:
    fontFamily: Roboto Flex
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Roboto Flex
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Roboto Flex
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Roboto Flex
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.1px
  label-md:
    fontFamily: Roboto Flex
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.2px
  label-sm:
    fontFamily: Roboto Flex
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.3px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-tablet: 1.25rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 1.5rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style
The design system powers an evidence-based visual research explorer. It combines the rigorous clarity of scientific inquiry with the intuitive, human-centered warmth of modern consumer media tools. The emotional target is calm confidence, effortless recall, and exploratory delight.

The style is rooted in modern Material You / Material Design 3 principles: crisp whites, clean surface hierarchies, dynamic 4-color accent moments, and hyper-legible, utilitarian typography. Primary surfaces remain quiet to let visual evidence and research artifacts take center stage, while tactile, pill-shaped affordances provide familiar landmarks for navigation and discovery.

## Colors
The palette leverages a dominant primary blue for interactive surfaces alongside a calibrated four-color system for tagging, status, and analytical evidence categorization:

- **Dominant Interactive:** Primary Blue (`#1A73E8`) powers key actions, active states, focus rings, and selection indicators.
- **Accents:** 
  - Emerald Green (`#34A853`): Verified evidence, positive correlation, success metrics.
  - Coral Red (`#EA4335`): Critical alerts, conflicting findings, flagged media.
  - Amber Yellow (`#FBBC04`): Highlights, starred items, pending analysis, high-value annotations.
- **Surfaces & Neutrals:**
  - Base Canvas: Pure White (`#FFFFFF`).
  - Surface Low: `#F8F9FA` for page gutters, toolbars, and inactive segments.
  - Surface Container: `#F1F3F4` for nested groupings, search pills, and hover fields.
  - Structural Hairlines: `#DADCE0` for dividers and borders.
  - Text High Contrast: `#202124` for primary titles and critical body copy.
  - Text Medium Contrast: `#5F6368` for metadata, timestamps, and secondary captions.

## Typography
Typography uses Roboto Flex across all tiers to emulate the systematic clarity of modern device operating systems. 

- **Display & Headlines:** Used for overarching project titles and high-level query headers. Weights stay at regular-to-medium (400–500) to keep the voice academic and approachable rather than assertive.
- **Titles:** Serve as entry points for photo clusters, research notebooks, and album summaries.
- **Body:** Engineered for high legibility in dense artifact descriptions, optical character recognition (OCR) snippets, and citation metadata.
- **Labels:** Strictly Medium (500) weight, used in filter chips, pill actions, image tags, and confidence scores.

## Layout & Spacing
The layout follows a fluid-responsive model that prioritizes media-first research grids:

- **Desktop (1024px+):** 12-column adaptive fluid grid with a permanent left icon-rail (72px) or collapsible research sidebar (280px). Section margins expand to `margin-desktop` (32px), with `gutter-desktop` (24px).
- **Tablet (600px - 1023px):** 8-column layout. Margin shifts to `margin-tablet` (24px) with `gutter-tablet` (20px). Top pinned search container becomes standard.
- **Mobile (<600px):** 4-column layout. Margin scales to `margin` (16px), with `gutter` (16px). Bottom floating bar handles critical actions.

Media exploration canvases employ a dynamic masonry or structured square matrix with strict `space-sm` (8px) inter-item spacing to preserve visual continuity. Padding within text metadata panels defaults to `space-md` (16px).

## Elevation & Depth
Elevation is constructed via ambient, low-contrast shadows paired with deliberate tonal layering rather than harsh directional drops:

- **Flat/Resting:** Background elements and default album cards sit at Elevation 0, bounded by a 1px `#DADCE0` outline.
- **Level 1 (Card Hover & Toolbars):** 
  `box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15)`
  Used on hover states for album cards, pill filter rows on scroll, and persistent headers.
- **Level 2 (Floating Search & Action Bars):** 
  `box-shadow: 0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15)`
  Used for the primary omni-search input bar and floating selection toolbars.
- **Level 3 (Modals & Full Artifact Previews):** 
  `box-shadow: 0 2px 6px 2px rgba(60,64,67,0.15), 0 8px 24px 4px rgba(60,64,67,0.2)`
  Used for deep-dive evidence overlays and metadata inspector panels.

## Shapes
The system utilizes two primary geometric archetypes:

- **16px Rounded Rectangles (`rounded-lg`):** Reserved for photo cards, research albums, insight callouts, and multi-media asset containers.
- **Full Pill (`9999px`):** Used universally for search bars, interactive chips, primary buttons, floating bottom utility bars, and badge indicators. 

Form fields and dropdown surfaces use 8px rounded corners to maintain structural alignment with tabular research data.

## Components

### Omni-Search Bar
- **Geometry:** Height 48px, fully rounded pill (`24px` radius).
- **Surface:** `#FFFFFF` resting on `#F8F9FA` canvas with `Level 2` elevation or `#F1F3F4` resting on `#FFFFFF` canvas with zero shadow.
- **Details:** Leading Google-style search lens, centered query placeholder ("Search evidence, timestamps, faces, transcripts..."), trailing action cluster for voice input, image upload lens, and user profile avatar.

### Filter Chips
- **Geometry:** Height 32px, pill-shaped radius (`9999px`).
- **Unselected:** Transparent or `#FFFFFF` fill, 1px `#DADCE0` border, `#3C4043` label text.
- **Selected:** Light tint background (`#E8F0FE`), zero border, `#1A73E8` label text, leading checkmark icon (`18px`).

### Buttons
- **Primary:** Full pill radius, `#1A73E8` fill, `#FFFFFF` text, `label-lg` typography. No shadow at rest; elevates to `Level 1` on hover with a 4% white overlay.
- **Secondary (Tonal):** Full pill radius, `#E8F0FE` fill, `#1A73E8` text.
- **Outlined:** Full pill radius, 1px `#DADCE0` border, `#1A73E8` text.

### Research Cards & Album Collections
- **Geometry:** Fixed 16px corner radius (`rounded-lg`).
- **Surface:** Smooth 1px border (`#DADCE0`), `#FFFFFF` background.
- **Media Presentation:** 1:1 square or 16:10 preview thumbnail with rounded top corners or complete internal nesting with an 8px uniform inner margin. Hover triggers a smooth 200ms transition to `Level 1` shadow and a subtle zoom on the media cover.
- **Metadata:** Two-line truncation for album title (`title-md`), single-line date/count subtitle (`body-sm`, `#5F6368`).

### Floating Action Bar (FAB) & Bottom Shelf
- **FAB:** Pill-shaped expanded button (48px height) or 56px rounded-square (16px radius) with `#FFFFFF` or `#C2E7FF` surface, `#001D35` content, and `Level 2` elevation.
- **Contextual Selection Shelf:** Pinned to the bottom-center of the viewport, 52px height, pill-shaped, `#202124` dark background with white action icons for batch tagging, sharing, exporting, and categorizing selected artifacts.

### Inputs, Checkboxes & Radios
- **Inputs:** `#F1F3F4` fill, borderless at rest, 8px radius. Active focus transitions to `#FFFFFF` with a crisp 2px `#1A73E8` outline.
- **Checkboxes:** 18px rounded square (2px radius). Inactive: 2px `#5F6368` border. Active: Solid `#1A73E8` fill with white checkmark. In image cards, checkboxes float in the top-left corner on a circular frosted scrim.
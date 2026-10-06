---
name: Ambient Memory Canvas
colors:
  surface: '#f9f9ff'
  surface-dim: '#d7dae3'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3fc'
  surface-container: '#ebedf7'
  surface-container-high: '#e6e8f1'
  surface-container-highest: '#e0e2eb'
  on-surface: '#181c22'
  on-surface-variant: '#414754'
  inverse-surface: '#2d3037'
  inverse-on-surface: '#eef0fa'
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
  background: '#f9f9ff'
  on-background: '#181c22'
  surface-variant: '#e0e2eb'
typography:
  display-lg:
    fontFamily: Roboto Flex
    fontSize: 36px
    fontWeight: '400'
    lineHeight: 44px
  headline-lg:
    fontFamily: Roboto Flex
    fontSize: 28px
    fontWeight: '400'
    lineHeight: 36px
  headline-md:
    fontFamily: Roboto Flex
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
  headline-sm:
    fontFamily: Roboto Flex
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
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
  label-md:
    fontFamily: Roboto Flex
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Roboto Flex
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 0.125rem
  gutter-loose: 0.75rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

The design system establishes a human-centric, photo-first utility canvas inspired by Material Design 3 (Material You). It recedes intentionally into the background, allowing personal photography and video to command visual primacy while maintaining the signature, welcoming utility of Google’s visual language.

### Design Movement & Ethos
- **Material You / Adaptive Modernism**: Soft, organic surface layering, generous pill geometries, and tactile micro-interactions.
- **Visual Restraint**: Pure white and warm neutral surface layers frame vivid personal media. High-saturation color is restricted strictly to active selections, system status highlights, brand signifiers, and the Google 4-color pinwheel accents (Blue, Red, Yellow, Green).
- **Emotional Resonance**: Nostalgic, intelligent, trustworthy, and organized. The UI feels like an intelligent physical gallery album layered with ambient computer vision cues.

## Colors

The palette balances clinical clarity with joyful micro-accents. Surface colors utilize warm-tinted neutrals (`#F8F9FA` to `#E9ECEF`) to avoid optical sterility while framing content. 

### Palette Architecture
- **Primary (`#1a73e8`)**: Google Blue anchors key calls to action, selection states, multi-select check rings, and active navigation indicators.
- **Secondary (`#34a853`)**: Google Green serves transactional confirmation, backup status reassurance, and utility badges (e.g., storage saved, shared confirmation).
- **Tertiary (`#ea4335`)**: Google Red indicates destructive alerts, high-priority retention actions, and "Favorites" heart accents.
- **Accent Yellow (`#fbbc04`)**: Used selectively for contextual highlights, "Memories" badge headers, and search intelligence recommendations.
- **Surfaces**:
  - `surface`: `#FFFFFF` for primary content tiles and cards.
  - `surface-container-low`: `#F8F9FA` for overall canvas base.
  - `surface-container`: `#F1F3F4` for search bars and tonal chips.
  - `surface-container-high`: `#E8EAED` for inactive toggle track states and sheet dividers.
- **On-Surface**: `#1F1F1F` for primary headlines, `#444746` for secondary metadata, and `#74777F` for de-emphasized placeholders.

## Typography

The system uses `Roboto Flex` to capture the geometric friendliness and technical legibility typical of modern Android surfaces. 

### Structural Hierarchy
- **Memories & Year Headers**: Rendered in `headline-md` or `headline-sm` with a medium weight (`500`) to anchor chronological timeline transitions without overpowering photo thumbnails.
- **Search & Conversational Prompts**: Expressed in `body-lg` with a light-to-regular hand (`400`), mimicking an assistive, conversational dialogue.
- **Meta & Timestamps**: Displayed using `label-md` and `body-sm` in secondary text colors (`#444746`) directly below or subtly overlaid over media tiles.

## Layout & Spacing

Layout focuses on high photo density balanced with expansive utility zones.

### Grid & Density Rules
- **Photo Timeline Grid**: Dynamic grid adjusting from tight pinch-to-zoom 5-column views (`gutter: 0.125rem` / `2px` spacing, edge-to-edge full bleed) to comfortable 3-column day-by-day views, up to 1-column featured memory hero views.
- **Card Lists & Editorial Collections**: 1- or 2-column configurations utilizing `gutter-loose` (`0.75rem` / `12px`) and an outer `margin` (`1rem` / `16px`).
- **Screen Margins**: Global horizontal boundary margins sit at `1rem` (16px) on mobile viewports. On wide viewports, galleries max out inside responsive side-rails with fixed 24px margins.

## Elevation & Depth

The design system uses M3-style tonal elevation alongside soft, ambient drop shadows to communicate surface separation without visual weight.

### Tonal Elevation Levels
- **Level 0 (Flat Canvas)**: Timeline backgrounds and pinned headers sit directly on `#FFFFFF` or `#F8F9FA` with zero elevation.
- **Level 1 (Docked Controls & Search Bar)**: Floating floating search bar sits with a subtle drop shadow (`0px 2px 6px rgba(60, 64, 67, 0.15), 0px 1px 2px rgba(60, 64, 67, 0.30)`) on a `#FFFFFF` fill.
- **Level 2 (Memory Carousels & Highlight Cards)**: Featured memories hovering horizontally across the top fold receive light atmospheric separation (`0px 4px 12px rgba(0, 0, 0, 0.08)`).
- **Level 3 (Bottom Navigation Sheet & Floating Action Badges)**: Navigation bars use semi-translucent `#FFFFFF`/95% surface with a high-blur backdrop filter (`backdrop-blur: 16px`) and a fine `1px` inner highlight border of `rgba(255, 255, 255, 0.8)` over scrolling media.

## Shapes

The geometric signature combines sweeping curves and tactile pill forms.

### Shape Application
- **Photo & Album Cards**: Standard cards feature `1rem` (16px) corner radii, giving media tiles a gentle card aesthetic without clipping visual details.
- **Pill Primitives (Full Round / 9999px)**: Filter chips, search inputs, bottom-sheet drag handles, contextual action buttons, and pinned memory tags are pill-shaped.
- **Modal Sheets**: Upper corners of pull-up sheets, photo metadata overlays, and sharing trays use `1.5rem` (24px) border-radii.

## Components

### Floating Search Bar
- **Form Factor**: Elevated pill container (`height: 52px`, `border-radius: 9999px`, background: `#FFFFFF`, elevation level 1).
- **Elements**: 
  - Leading iconic Google 4-color pinwheel glyph or Google Assistant spark icon.
  - Conversational placeholder text: *"Try 'Sunset at Venice Beach last summer' or 'Dogs playing'"* in `body-md` (`#74777F`).
  - Trailing action stack containing the microphone (Voice Search) and Google Lens view-finder glyphs, separated by comfortable tap zones (`space-sm`).

### Tonal Pill Chips
- **Geometry**: Height 36px, `border-radius: 9999px`, padding `0 16px`.
- **States**:
  - Inactive: Background `#F1F3F4`, text `#1F1F1F`, no border.
  - Active: Background `#E8F0FE` (Google Blue tint), text `#1A73E8`, accented with a leading `18px` checkmark.

### Media Cards & Timeline Tiles
- **Standard Day Card**: Edge-to-edge seamless fit with 2px borders during tight grids; transitions to 16px rounded cards when highlighted or curated into an album feed.
- **Memory Card**: Aspect ratio 9:16 vertical capsule, `border-radius: 16px`, gradient scrim bottom (`rgba(0,0,0,0) 50%` to `rgba(0,0,0,0.7) 100%`), featuring title in `headline-sm` (`#FFFFFF`) and date in `label-sm` (`#FFFFFF/80%`).

### Interactive Floating Action Controls
- **Bottom Navigation**: Clean 3-to-4 tab dock (Photos, Memories, Library, Search) with pill-shaped active indicator capsules (`#D3E3FD` fill for active tab with `#041E49` icon glyph).
- **Multi-Selection Checkbox**: Circle indicator positioned at top-left of each photo card. Resting unselected state is an outline ring with white border; active selection is a solid `#1A73E8` disc with a crisp white checkmark.
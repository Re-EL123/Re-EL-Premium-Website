# Re-EL Official Website — Full Product & Design Specification

The official Re-EL website should be positioned as a **technology company website first**, rather than simply a freelance portfolio. The objective is to make Re-EL look capable of handling **business software, websites, automation, integrations, technical support and digital transformation projects** for companies.

The site should use the existing Re-EL identity: **deep navy, dark slate, yellow/gold, white/black**, with the scarab/sun concept representing technology, movement and transformation.


I would build it as a **high-performance interactive web experience**, but keep the animations purposeful rather than turning it into a heavy visual demo.

---

# 1. Core Website Positioning

### Brand

**Re-EL Branding & Technologies**

### Primary positioning

> **Technology that moves businesses forward.**

Alternative supporting statement:

> We design, build and support digital solutions that help businesses operate smarter, connect better and grow faster.

### Primary email

**[info@re-el.co.za](mailto:info@re-el.co.za)**

### Website

**[www.re-el.co.za](http://www.re-el.co.za)**

### Primary conversion

The website should continuously drive visitors toward:

**Request a Consultation**

rather than simply "Contact Us".

---

# 2. Recommended Technology Architecture

## Frontend

### Recommended

**React + Vite**

Structure:

```text
re-el-website/
│
├── public/
│   ├── assets/
│   │   ├── images/
│   │   ├── videos/
│   │   ├── icons/
│   │   ├── logos/
│   │   └── models/
│   │
│   ├── favicon.svg
│   └── manifest.webmanifest
│
├── src/
│   ├── components/
│   ├── sections/
│   ├── animations/
│   ├── data/
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   ├── App.jsx
│   └── main.jsx
│
├── index.html
├── package.json
└── vite.config.js
```

### Why React/Vite

It gives Re-EL room to grow beyond a static company website into:

* Client portal
* Project dashboards
* Service enquiry system
* Client onboarding
* Quote requests
* Blog/CMS
* Case-study system
* Authentication
* AI features

without rebuilding the frontend later.

---

# 3. Hosting Architecture

For Re-EL, I recommend:

```text
                    ┌──────────────────┐
                    │   re-el.co.za    │
                    └────────┬─────────┘
                             │
                     Cloudflare DNS
                             │
                     ┌───────▼───────┐
                     │   Frontend    │
                     │ React + Vite  │
                     │ GitHub Pages  │
                     └───────┬───────┘
                             │
                    HTTPS / API calls
                             │
                     ┌───────▼───────┐
                     │    Vercel     │
                     │ Serverless API│
                     └───────┬───────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
          MongoDB         Resend         WhatsApp
          Database         Email           CTA
```

This matches your preference for a low-cost architecture while allowing Re-EL to scale.

---

# 4. Frontend Framework & Libraries

## Core

| Technology     | Purpose             |
| -------------- | ------------------- |
| React          | UI architecture     |
| Vite           | Build system        |
| JavaScript/JSX | Development         |
| Tailwind CSS   | Utility styling     |
| CSS Variables  | Re-EL design system |
| Lucide React   | Icons               |

## Animation

### GSAP

Use GSAP as the primary animation engine.

GSAP is framework-agnostic and supports timelines, staggers and a large ecosystem of animation plugins. ([GSAP][1])

### GSAP ScrollTrigger

Use for:

* scroll reveals
* pinned sections
* horizontal scrolling
* scrub animations
* progress animations
* project transitions

ScrollTrigger specifically supports scrub, pinning, snapping and viewport-triggered animations. ([GSAP][2])

### Three.js

Use selectively for the hero/background experience.

Three.js provides a higher-level 3D layer over WebGL and handles scenes, cameras, lighting, materials and related 3D functionality. ([Three.js][3])

Do **not** make the entire website dependent on Three.js.

---

# 5. Design System

## Primary palette

```css
--re-navy: #21396A;
--re-slate: #3B424F;
--re-yellow: #F6C945;
--re-white: #FFFFFF;
--re-black: #080B12;
```

Additional atmospheric colours:

```css
--re-navy-dark: #0A1224;
--re-blue: #2F5EBB;
--re-glow: rgba(246,201,69,.35);
--re-white-soft: rgba(255,255,255,.72);
```

---

# 6. Visual Language

The design should combine:

### Corporate technology

with:

### Digital engineering

and:

### African-rooted brand identity.

Avoid making it look like a generic SaaS template.

The scarab should become a **visual brand system**, not simply a logo placed in the header.

Possible motifs:

* scarab geometry
* orbital paths
* sun arcs
* golden energy lines
* digital grids
* connected nodes
* circuit-like patterns
* geometric wings
* data streams

---

# 7. Typography

Recommended primary typeface:

**Inter**

or

**Manrope**

For large display typography:

**Space Grotesk**

Potential pairing:

```text
HEADINGS
Space Grotesk

BODY
Inter

TECHNICAL LABELS
JetBrains Mono
```

Use monospace sparingly for:

* technology labels
* system status
* project metadata
* code-inspired UI
* numbers

---

# 8. Navigation

Desktop:

```text
RE-EL

Services
Solutions
Work
About
Process
Contact

[ Start a Project ]
```

Sticky navigation.

When scrolling:

### Initial

Transparent / glass navigation.

### After scrolling

Dark translucent glass:

```text
backdrop-filter: blur(20px)
```

with a subtle gold bottom border/glow.

---

# 9. Mobile Navigation

Full-screen animated navigation.

Example:

```text
SERVICES
SOLUTIONS
WORK
ABOUT
PROCESS
CONTACT

──────────────

Let's build something.
info@re-el.co.za
```

Opening animation:

1. Menu button morphs into X.
2. Background expands.
3. Navigation items stagger upward.
4. Gold line travels across each item.
5. Scarab icon subtly rotates.

---

# 10. HERO SECTION

This should be the strongest section.

## Headline

> **Technology that moves businesses forward.**

Supporting copy:

> Re-EL designs, develops and supports digital solutions that transform ideas, processes and business operations into scalable technology.

CTA:

**Start a Project**

Secondary:

**Explore Our Work**

---

# 11. Hero Motion Graphics

This is where the site should feel premium.

### Background

Interactive animated digital environment.

Possible composition:

```text
              ✦       ·
       ·             ✦

          ╭─────────╮
       ╱              ╲
      │    RE-EL       │
      │    SYSTEM      │
       ╲              ╱
          ╰─────────╯

     ·       ◎       ·
         ╲       ╱
           ╲   ╱
             ●
```

Behind the hero:

* animated constellation
* particles
* orbital rings
* moving grid
* subtle data streams
* glowing nodes
* golden energy trails

---

# 12. Interactive Scarab

Create a stylised **3D/digital scarab**.

The scarab can:

* slowly rotate
* react to mouse movement
* change orientation based on cursor position
* emit subtle particles
* leave an orbital trail
* respond when the user hovers over CTA

On mobile:

Replace heavy 3D interaction with a lightweight animated SVG/canvas version.

---

# 13. Hero Text Animation

Headline should not simply fade in.

Use:

### Word reveal

```text
Technology
      ↓
that
      ↓
moves
      ↓
businesses
      ↓
forward.
```

Animation:

* opacity
* y-position
* blur
* slight rotation
* stagger

Then continuously animate one word:

**Technology**

**Innovation**

**Automation**

**Development**

**Transformation**

Example:

> We build technology that **[moves / connects / automates / transforms]** businesses.

---

# 14. Live Cursor System

Desktop only.

Cursor consists of:

### Outer ring

Slow follow.

### Inner dot

Immediate follow.

### Hover state

When entering:

* buttons
* cards
* project thumbnails
* links

the cursor transforms.

For example:

```text
       VIEW
       PROJECT
```

inside the cursor.

On mobile:

Disable completely.

---

# 15. HERO STATUS BAR

Small technical dashboard near bottom of hero:

```text
RE-EL TECHNOLOGY SYSTEM
────────────────────────

● ONLINE

SOFTWARE
WEB
AUTOMATION
INTEGRATION
SUPPORT
```

The ONLINE indicator pulses subtly.

---

# 16. SECTION — "WHAT WE BUILD"

Headline:

> **From idea to infrastructure.**

Three major categories.

### Software

* Web applications
* Business systems
* Custom platforms
* APIs
* Databases
* Automation

### Digital

* Corporate websites
* Landing pages
* E-commerce
* UI/UX
* Branding
* Digital experiences

### Technology Support

* Maintenance
* Bug fixing
* Technical support
* System optimisation
* Integrations
* Cloud support

---

# 17. Services Interactive Grid

Instead of ordinary cards, create an interactive technology grid.

Example:

```text
┌──────────────────┬──────────────────┐
│ SOFTWARE         │ WEB DEVELOPMENT  │
│                  │                  │
│ 01               │ 02               │
├──────────────────┼──────────────────┤
│ AUTOMATION       │ API & INTEGRATION│
│                  │                  │
│ 03               │ 04               │
├──────────────────┼──────────────────┤
│ TECH SUPPORT     │ UI / UX          │
│                  │                  │
│ 05               │ 06               │
└──────────────────┴──────────────────┘
```

Hover:

* card expands
* background changes
* icon animates
* description appears
* gold accent travels along border

---

# 18. SECTION — TECHNOLOGY STACK

Make this visually impressive.

Instead of a basic logo list:

```text
JAVA
JAVASCRIPT
REACT
NODE
SPRING
MONGODB
POSTGRESQL
GIT
CLOUD
APIs
```

Create an animated **technology constellation**.

Nodes connected with animated lines.

Central node:

> RE-EL ENGINE

Connected to:

```text
Frontend
Backend
Database
Cloud
APIs
Automation
AI
```

The lines slowly move.

---

# 19. SECTION — FEATURED WORK

This is extremely important for converting companies.

Featured projects:

### Clock-Kit

Workforce attendance and clocking platform.

### Re-V

CV generation and career technology platform.

### Chatre

AI-powered development/productivity platform.

### Re-EL WebStudio

Website creation platform.

Potential future projects can be added without redesigning the component.

---

# 20. Project Presentation

Don't use ordinary cards.

Use large horizontal case-study panels.

Example:

```text
01

CLOCK-KIT

Workforce Management Platform

[ LARGE PRODUCT VISUAL ]

Workforce
Attendance
Management

VIEW CASE STUDY →
```

As the user scrolls:

* image moves horizontally
* title remains pinned
* UI screenshots transition
* technology tags animate
* background changes subtly

GSAP ScrollTrigger is particularly suitable for this type of scroll-linked presentation. ([GSAP][2])

---

# 21. Case Study Pages

Each major project should eventually have:

```text
/project/clock-kit
/project/re-v
/project/chatre
```

Structure:

1. Hero
2. Problem
3. Solution
4. Architecture
5. Features
6. UI screenshots
7. Technologies
8. Development process
9. Results
10. CTA

This will make Re-EL look much more credible to corporate clients.

---

# 22. SECTION — HOW WE WORK

Create a large animated timeline.

```text
01
DISCOVER

02
PLAN

03
DESIGN

04
BUILD

05
TEST

06
DEPLOY

07
SUPPORT
```

As the visitor scrolls:

The timeline progressively illuminates.

A gold energy line travels through each stage.

---

# 23. SECTION — WHY RE-EL

Use six principles:

### Business First

Technology must solve an actual business problem.

### Built Around You

Solutions are designed around the client's workflow.

### Scalable

Build today with tomorrow in mind.

### Practical

Avoid unnecessary complexity.

### Support

Technology doesn't stop at deployment.

### Continuous Improvement

Systems can evolve as the business grows.

---

# 24. About Re-EL

Headline:

> **Technology. Creativity. Engineering.**

Content should establish that Re-EL combines:

* software engineering
* web development
* design
* automation
* technical support
* business understanding

with a distinctly South African technology-company identity.

---

# 25. Re-EL Brand Story

This is where the scarab becomes meaningful.

Possible concept:

> **The scarab represents movement, transformation and the continuous creation of value. Re-EL applies the same principle to technology — taking ideas, challenges and processes and turning them into useful digital systems.**

Visual:

A golden sun moves across the screen.

The scarab follows it.

Then the line transforms into:

```text
IDEA
 ↓
DESIGN
 ↓
CODE
 ↓
SYSTEM
 ↓
IMPACT
```

---

# 26. Live "Digital Engine" Section

One of the signature sections.

Title:

> **Behind every solution is an engine.**

Interactive visual showing:

```text
                    ┌────────────┐
                    │   CLIENT   │
                    └─────┬──────┘
                          ↓
                  ┌───────────────┐
                  │   DISCOVERY   │
                  └───────┬───────┘
                          ↓
       ┌──────────┬───────┴───────┬──────────┐
       ↓          ↓               ↓          ↓
    DESIGN      CODE          DATABASE     API
       │          │               │          │
       └──────────┴───────┬───────┴──────────┘
                          ↓
                    RE-EL ENGINE
                          ↓
                       IMPACT
```

Animated data particles travel through the architecture.

---

# 27. AI Section

Because AI is increasingly relevant to your work, include a dedicated capability:

## AI & Intelligent Automation

Services:

* AI integrations
* AI assistants
* workflow automation
* document processing
* intelligent search
* chatbot systems
* API-connected AI
* business process automation

Do not position Re-EL as merely an "AI company."

Position AI as **one capability inside the technology stack**.

---

# 28. Pricing

I would **not put the full rate card on the homepage**.

Instead:

> **Every project is different. We provide transparent estimates based on scope, complexity and requirements.**

CTA:

**Request a Quote**

You can optionally have:

```text
Starting from

Websites       R2,500+
Applications   R5,000+
Automation     R1,500+
Support        R2,500/month+
```

Then provide the detailed rate card after enquiry.

This makes the website feel more corporate.

---

# 29. Client CTA

Large section near the bottom:

> **Have a technology problem?**

> Let's turn it into a working solution.

Buttons:

**Start a Project**

**Email Re-EL**

Email:

**[info@re-el.co.za](mailto:info@re-el.co.za)**

---

# 30. Contact Section

Form:

```text
FULL NAME *
COMPANY
EMAIL *
PHONE
SERVICE *
BUDGET
PROJECT DESCRIPTION *
TIMELINE
```

Service dropdown:

```text
Software Development
Website Development
Web Application
E-Commerce
API Integration
Automation
AI Solutions
Technical Support
Maintenance
UI/UX
Other
```

CTA:

**Send Enquiry**

---

# 31. WhatsApp Integration

Floating WhatsApp button.

But rather than simply opening WhatsApp, dynamically create:

```text
Hi Re-EL, I would like to enquire about [SERVICE].
```

For example:

> Hi Re-EL, I would like to enquire about software development.

---

# 32. Email Integration

Use:

**[info@re-el.co.za](mailto:info@re-el.co.za)**

Backend:

### Resend

Frontend submits:

```text
POST /api/contact
```

Vercel function:

```text
/api/contact
```

Backend validates:

* name
* email
* message
* service
* spam protection

Then sends notification through Resend.

---

# 33. Anti-Spam

Include:

* honeypot
* rate limiting
* input validation
* origin validation
* CAPTCHA/Turnstile if necessary

Never expose the Resend API key in the frontend.

---

# 34. Footer

Large premium footer.

```text
RE-EL

Technology that moves businesses forward.

SERVICES
Software
Web
Automation
AI
Support

COMPANY
About
Work
Process
Contact

CONNECT
LinkedIn
GitHub
WhatsApp
Email

info@re-el.co.za

© 2026 Re-EL Branding & Technologies
```

---

# 35. Footer Animation

The footer should contain a giant:

> **RE-EL**

with a slow animated gold gradient.

When hovering:

```text
R E - E L
```

slightly separates and reconnects.

The scarab appears beneath the logo.

---

# 36. Loading Experience

Don't use a boring spinner.

Create a **Re-EL system boot sequence**.

Example:

```text
RE-EL
TECHNOLOGY SYSTEM

INITIALISING...

BRAND ............. OK
SYSTEM ............ OK
SERVICES .......... OK
NETWORK ........... OK

100%
```

Then transition into the homepage.

Important:

**Maximum duration ~1.5–2 seconds.**

Don't force returning visitors through a long loading animation.

---

# 37. Page Transition System

When navigating:

Current page:

```text
HOME
```

transition:

```text
golden horizontal energy line
          ↓
screen darkens
          ↓
new page appears
```

GSAP can handle these transitions while maintaining a lightweight implementation. ([GSAP][1])

---

# 38. Scroll Experience

Use:

### Lenis

for smooth scrolling where appropriate.

Then:

### GSAP ScrollTrigger

for scroll-linked effects.

Architecture:

```text
Lenis
  ↓
Native-like smooth scrolling
  ↓
GSAP
  ↓
ScrollTrigger
  ↓
Section animations
```

Avoid excessive scroll-jacking.

---

# 39. Motion System

Every animation should fall into one of five categories.

### 1. Entrance

Elements enter when becoming visible.

### 2. Interaction

Elements respond to hover/click.

### 3. Scroll

Objects react to scroll position.

### 4. Ambient

Background elements continuously move.

### 5. Transformation

Objects morph between states.

This keeps the website visually sophisticated without becoming chaotic.

---

# 40. Live Ambient Animation

Throughout the site:

* particles
* gradient movement
* orbital paths
* grid distortion
* subtle noise
* floating geometric objects
* animated lines
* pulsing nodes

But opacity should generally remain low.

The content must remain dominant.

---

# 41. Three.js Usage

Use Three.js primarily for:

### Hero

3D scarab / digital object.

### Technology section

Interactive 3D network.

### Optional CTA

3D orbital system.

Three.js requires a scene, camera and renderer, making it appropriate for these contained experiences rather than being used indiscriminately throughout the entire page. ([Three.js][4])

---

# 42. Performance Strategy

This is critical.

The website can look extremely advanced without becoming slow.

### Desktop

Full effects.

### Tablet

Reduced particles.

### Mobile

2D alternatives.

### Low-power devices

Disable:

* WebGL
* excessive particles
* heavy blur
* complex cursor effects

Use:

```javascript
prefers-reduced-motion
```

to respect accessibility preferences.

---

# 43. Image Strategy

Do not use generic stock images as the primary visual identity.

Create Re-EL-specific assets.

## Required assets

### Brand

* Re-EL logo SVG
* scarab SVG
* scarab 3D model
* favicon
* social preview image
* monochrome logo
* horizontal logo
* icon mark

### UI

* service icons
* technology icons
* CTA icons
* navigation icons

### Portfolio

Screenshots of:

* Clock-Kit
* Re-V
* Chatre
* Re-EL WebStudio
* Jalusi Flow, where appropriate and authorized

---

# 44. 3D Assets

Recommended:

```text
/scarab.glb
/scarab-gold.glb
/reel-orb.glb
/network-node.glb
```

Use `.glb` rather than unnecessarily large formats.

Three.js supports models/textures through the application's public asset structure. ([Three.js][5])

---

# 45. Video Assets

Optional hero background video:

```text
hero-tech-loop.webm
```

But the primary hero should not depend on video.

Use:

### WebM

first

### MP4

fallback

Keep videos short and compressed.

---

# 46. SEO

The site should target:

### Primary

**Re-EL Branding & Technologies**

### Secondary

* software development South Africa
* web development South Africa
* custom software development
* business automation South Africa
* website development
* API integration
* technical support
* web applications
* AI solutions
* software developer South Africa

---

# 47. SEO Pages

Create:

```text
/
 /services
 /services/software-development
 /services/web-development
 /services/automation
 /services/api-integrations
 /services/ai-solutions
 /services/technical-support
 /work
 /work/clock-kit
 /work/re-v
 /work/chatre
 /about
 /contact
```

This is much stronger for search visibility than having everything on one page.

---

# 48. Open Graph

When someone shares Re-EL:

```text
RE-EL Branding & Technologies

Technology that moves businesses forward.

[RE-EL branded visual]
```

Create a dedicated:

```text
og-image.jpg
```

at approximately:

```text
1200 × 630
```

---

# 49. Structured Data

Implement:

### Organization

```text
Re-EL Branding & Technologies
```

### LocalBusiness / Organization where appropriate

### WebSite

### Service

### CreativeWork / SoftwareApplication

for portfolio projects where applicable.

---

# 50. Accessibility

Required:

* semantic HTML
* keyboard navigation
* visible focus states
* alt text
* proper heading hierarchy
* accessible forms
* ARIA where necessary
* reduced-motion mode
* sufficient contrast
* no animation-only information

---

# 51. Analytics

Implement:

* Google Analytics 4
* Google Search Console
* Vercel Analytics if appropriate

Track:

```text
page_view
service_view
project_view
contact_started
contact_submitted
whatsapp_clicked
email_clicked
quote_requested
```

This lets you see which Re-EL services actually generate business.

---

# 52. Security

Frontend:

* no secrets
* CSP
* HTTPS
* secure headers

API:

* validation
* sanitisation
* rate limiting
* CORS restrictions
* environment variables

Environment:

```text
RESEND_API_KEY
MONGODB_URI
TURNSTILE_SECRET
```

if those services are implemented.

---

# 53. CMS / Content Architecture

Initially, don't build an expensive CMS.

Store structured content:

```javascript
services.js
projects.js
technologies.js
testimonials.js
```

Example:

```javascript
{
  id: "clock-kit",
  title: "Clock-Kit",
  category: "Workforce Technology",
  description: "...",
  technologies: [
    "JavaScript",
    "React",
    "Node.js",
    "MongoDB"
  ],
  url: "https://www.clock-kit.rf.gd/"
}
```

This makes portfolio updates easy.

---

# 54. Recommended Website Experience

The entire homepage should feel like:

```text
OPEN
 ↓
RE-EL SYSTEM BOOT
 ↓
HERO
 ↓
LIVE DIGITAL ENVIRONMENT
 ↓
WHAT WE BUILD
 ↓
SERVICES
 ↓
TECHNOLOGY ENGINE
 ↓
FEATURED WORK
 ↓
PROCESS
 ↓
ABOUT
 ↓
AI + AUTOMATION
 ↓
WHY RE-EL
 ↓
CONTACT
 ↓
RE-EL FOOTER
```

---

# 55. Signature Visual Moment

I recommend one memorable interaction that becomes uniquely associated with Re-EL.

When the user reaches the main CTA:

> **Let's build something.**

the screen subtly darkens.

A golden line begins travelling across the page.

It forms the outline of the **Re-EL scarab**.

The scarab rolls the golden line forward.

The line transforms into:

> **IDEA → TECHNOLOGY → IMPACT**

Then the CTA appears:

**START A PROJECT →**

This becomes the visual metaphor for the entire company.

---

# 56. Recommended Library Stack

Final stack:

```text
React
Vite
Tailwind CSS
GSAP
GSAP ScrollTrigger
Three.js
Lenis
Lucide React
React Hook Form
Zod
Resend
MongoDB
Vercel
Cloudflare
```

For animation, I would make **GSAP the primary system**, with Three.js used only where genuine 3D adds value. GSAP is specifically designed for performant browser animation and its ScrollTrigger system is well suited to the scroll-driven sections proposed here. ([GSAP][6])

---

# 57. Final Re-EL Website Identity

The finished website should communicate these five things within the first 10 seconds:

### 1. Re-EL is a technology company.

Not merely a freelancer.

### 2. Re-EL can build real software.

Clock-Kit, Re-V, Chatre and other products demonstrate this.

### 3. Re-EL understands business.

The website must focus on problems and outcomes rather than just programming languages.

### 4. Re-EL can support companies after deployment.

Maintenance, support, automation and integrations should be prominent.

### 5. Re-EL has a distinctive identity.

The **scarab + sun + technology + motion** concept should make the company memorable.

---

## Recommended homepage headline system

I would ultimately use:

> **WE BUILD TECHNOLOGY THAT MOVES BUSINESS.**

Then animate the supporting words:

> **Software. Web. Automation. AI. Integration. Support.**

And the primary CTA:

> **START A PROJECT →**

with:

**[info@re-el.co.za](mailto:info@re-el.co.za)**

as the persistent business contact.

This gives you a website that can serve both **corporate clients such as Jalusi** and smaller businesses, while also functioning as a strong public-facing portfolio for Re-EL.

[1]: https://gsap.com/docs/v3/Installation/?utm_source=chatgpt.com "Installation | GSAP | Docs & Learning"
[2]: https://gsap.com/docs/v3/Plugins/ScrollTrigger/?utm_source=chatgpt.com "ScrollTrigger | GSAP | Docs & Learning"
[3]: https://threejs.org/manual/pages/fundamentals.html?utm_source=chatgpt.com "Fundamentals"
[4]: https://threejs.org/manual/pages/creating-a-scene.html?utm_source=chatgpt.com "Creating a scene"
[5]: https://threejs.org/manual/pages/installation.html?utm_source=chatgpt.com "Installation"
[6]: https://gsap.com/docs/v3/?utm_source=chatgpt.com "docsHome | GSAP | Docs & Learning"

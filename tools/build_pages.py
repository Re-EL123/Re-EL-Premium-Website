#!/usr/bin/env python3
"""Build the secondary pages from index.html.

Every page shares the loader, nav, mobile menu, footer, cursor and script
tags that already exist on the homepage; this module slices that chrome out
of index.html rather than duplicating it, so a change to the header is
propagated to every page the next time you run it.

    python3 tools/build_pages.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.re-el.co.za"
SRC = (ROOT / "index.html").read_text(encoding="utf-8")


def between(a, b, src=SRC):
    i = src.index(a)
    return src[i:src.index(b, i)]


# --------------------------------------------------------------------------
# chrome lifted from index.html
# --------------------------------------------------------------------------
HEAD_BASE = SRC[:SRC.index("<title>")]
HEAD_ICONS = between("<!-- Icons / app -->", "<!-- Open Graph -->")
ASSETS = between("<!-- Fonts", "<!-- Structured data -->")
BODY_PRE = between("<body>", "<!-- ================= NAV ================= -->")
NAV = between("<!-- ================= NAV ================= -->", "<main id=\"home\">")
FOOTER = between("<!-- ================= FOOTER ================= -->", "<!-- Scripts -->")
SCRIPTS = between("<!-- Scripts -->", "</body>")


def localize(h):
    """Root-relative asset paths + section links that point at the homepage."""
    h = h.replace('href="assets/', 'href="/assets/')
    h = h.replace('src="assets/', 'src="/assets/')
    h = re.sub(r'href="#(?!main\b)', 'href="/#', h)
    # on a subpage the skip link must target this page's <main>
    h = h.replace('href="/#home">Skip to main content', 'href="#main">Skip to main content')
    return h


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def meta(name, content, prop=False):
    k = "property" if prop else "name"
    return f'<meta {k}="{name}" content="{esc(content)}" />'


def breadcrumb_ld(path, trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for pos, (name, href) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": pos, "name": name,
                      "item": SITE + href})
    return {
        "@type": "BreadcrumbList",
        "@id": f"{SITE}{path}#breadcrumb",
        "itemListElement": items,
    }


def crumbs(trail):
    """trail = [(label, href), ...] without Home."""
    out = ['<nav class="breadcrumb container" aria-label="Breadcrumb"><ol>']
    out.append('<li><a href="/">Home</a></li>')
    for i, (label, href) in enumerate(trail):
        last = i == len(trail) - 1
        if last:
            out.append(f'<li><span aria-current="page">{esc(label)}</span></li>')
        else:
            out.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    out.append("</ol></nav>")
    return "\n".join(out)


def cards(items):
    out = ['<div class="card-grid">']
    for kicker, title, text, href in items:
        out.append(
            f'  <a class="info-card" href="{href}" data-reveal data-hover>\n'
            f'    <span class="card-kicker">{esc(kicker)}</span>\n'
            f'    <h3>{esc(title)}</h3>\n'
            f'    <p>{esc(text)}</p>\n'
            f'    <span class="card-arrow">View &rarr;</span>\n'
            f'  </a>'
        )
    out.append("</div>")
    return "\n".join(out)


def page(path, title, description, body, ld_nodes, og_type="website"):
    """Assemble a complete HTML document."""
    canonical = SITE + path
    head = [
        HEAD_BASE,
        f"<title>{esc(title)}</title>",
        meta("description", description),
        meta("author", "Re-EL Branding & Technologies"),
        meta("robots", "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"),
        f'<link rel="canonical" href="{canonical}" />',
        meta("theme-color", "#080B12"),
        meta("color-scheme", "dark"),
        "",
        localize(HEAD_ICONS),
        "<!-- Open Graph -->",
        meta("og:type", og_type, prop=True),
        meta("og:locale", "en_ZA", prop=True),
        meta("og:site_name", "Re-EL Branding & Technologies", prop=True),
        meta("og:title", title, prop=True),
        meta("og:description", description, prop=True),
        meta("og:url", canonical, prop=True),
        meta("og:image", f"{SITE}/assets/img/og-image.png", prop=True),
        meta("og:image:type", "image/png", prop=True),
        meta("og:image:width", "1200", prop=True),
        meta("og:image:height", "630", prop=True),
        meta("og:image:alt", "Re-EL — technology that moves businesses forward.", prop=True),
        "",
        "<!-- Twitter -->",
        meta("twitter:card", "summary_large_image"),
        meta("twitter:title", title),
        meta("twitter:description", description),
        meta("twitter:image", f"{SITE}/assets/img/og-image.png"),
        meta("twitter:image:alt", "Re-EL — technology that moves businesses forward."),
        "",
        localize(ASSETS),
        "<!-- Structured data -->",
        '<script type="application/ld+json">',
        json.dumps({"@context": "https://schema.org", "@graph": ld_nodes},
                   ensure_ascii=False, indent=2),
        "</script>",
        "</head>",
    ]
    doc = [
        "\n".join(head),
        localize(BODY_PRE),
        localize(NAV),
        body,
        localize(FOOTER),
        localize(SCRIPTS),
        "</body>",
        "</html>",
        "",
    ]
    out = ROOT / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(doc), encoding="utf-8")
    return out


def service_icon(name):
    m = re.search(
        r'(<svg[^>]*>.*?</svg>)\s*<h3>' + re.escape(name) + r"</h3>",
        SRC, re.S)
    return m.group(1) if m else ""


def work_icon(marker):
    """SVG that opens the work-visual block containing `marker`."""
    i = SRC.index(marker)
    chunk = SRC[:i]
    start = chunk.rindex('<div class="work-visual')
    seg = SRC[start:i]
    m = re.search(r"(<svg[^>]*>.*?</svg>)", seg, re.S)
    return m.group(1) if m else ""


# --------------------------------------------------------------------------
# content
# --------------------------------------------------------------------------
SERVICES = [
    dict(
        slug="software-development", name="Software",
        title="Custom Software Development in South Africa | Re-EL",
        desc="Custom platforms, business systems and internal tools built around how your company actually works — designed, engineered and supported by Re-EL.",
        lead="Custom platforms, business systems and internal tools built around how your company actually works.",
        intro=[
            "Most businesses do not need another off-the-shelf product with a subscription attached. They need a system that matches the way their team already works — the same approvals, the same naming, the same exceptions — without forcing everyone to bend to somebody else's roadmap.",
            "Re-EL designs and builds that system end to end: the data model, the business logic, the interface and the deployment. You own the result.",
        ],
        includes=[
            ("Business systems", "Order, stock, job, case and reporting systems shaped around your existing process."),
            ("Internal tools", "Admin consoles, dashboards and operational tooling that replace spreadsheet chains."),
            ("Customer-facing platforms", "Portals, self-service areas and account experiences with authentication and roles."),
            ("Data & reporting", "Structured storage, audit trails and reporting views that answer real questions."),
        ],
        related_note="Scope, complexity and requirements drive the estimate — applications start at R5,000.",
    ),
    dict(
        slug="web-development", name="Web Development",
        title="Website & Web App Development South Africa | Re-EL",
        desc="Corporate websites, landing pages and web apps engineered for performance, accessibility and conversion by Re-EL.",
        lead="Corporate websites, landing pages and web apps engineered for performance and conversion.",
        intro=[
            "A website is usually the first thing a buyer checks before they contact you, and the slowest, least maintained thing in the business. We build sites that load quickly, read clearly and hold up — the technical foundations are the same ones we use for applications.",
            "Every build ships with semantic markup, real accessibility affordances, self-hosted assets and structured data, so the page works for people and for search engines.",
        ],
        includes=[
            ("Corporate websites", "Multi-section marketing sites with a CMS-ready structure and consistent design system."),
            ("Landing pages", "Focused single-purpose pages built to convert a specific campaign or offer."),
            ("Web applications", "Interactive, stateful products that behave like software rather than a brochure."),
            ("Performance & SEO", "Core Web Vitals, semantic headings, metadata and schema markup built in from the start."),
        ],
        related_note="Websites start at R2,500.",
    ),
    dict(
        slug="automation", name="Automation",
        title="Workflow Automation Services South Africa | Re-EL",
        desc="Remove repetitive manual work with workflow automation connected directly to your systems — built and maintained by Re-EL.",
        lead="Remove repetitive manual work with workflow automation connected directly to your systems.",
        intro=[
            "If a person is copying data between two tools, re-typing an email that follows the same template every week, or chasing an approval that lives in someone's inbox, that is a machine doing a human's job badly.",
            "We map the workflow first, then automate the parts that add no judgement. Where a human decision belongs, it stays with a human — the system just stops making them do the typing.",
        ],
        includes=[
            ("Process automation", "Scheduled and event-driven jobs that move data, generate documents and trigger hand-offs."),
            ("Approvals & notifications", "Routed approvals with a clear record of who acted, when and why."),
            ("Document generation", "Quotes, invoices, reports and CVs produced from structured input instead of copy-paste."),
            ("System-to-system sync", "Keeping records consistent across the tools you already pay for."),
        ],
        related_note="Automation projects start at R1,500.",
    ),
    dict(
        slug="api-integration", name="API & Integration",
        title="API & System Integration Services | Re-EL",
        desc="Connect payments, CRMs, databases and third-party services to the systems you run — integration work by Re-EL.",
        lead="Connect the tools you already use — payments, CRMs, databases and third-party services.",
        intro=[
            "Businesses rarely suffer from having too few tools. They suffer from the gap between them: the sale is in one system, the invoice in another, and the truth lives in somebody's memory.",
            "We close that gap. Re-EL builds the integrations, the webhooks and the glue code, with retries, logging and failure handling so that a broken third-party call does not quietly lose your data.",
        ],
        includes=[
            ("Payment integration", "Gateway integration for online payments and reconciliation against your own records."),
            ("CRM & marketing tools", "Two-way synchronisation so a lead entered once is correct everywhere."),
            ("Database integration", "Reporting and operational access to the data already sitting in your systems."),
            ("Third-party APIs", "Shipping, accounting, communications and any service with a documented API."),
        ],
        related_note="Integration work is quoted per connection — applications start at R5,000.",
    ),
    dict(
        slug="tech-support", name="Tech Support",
        title="Website & Software Maintenance South Africa | Re-EL",
        desc="Ongoing maintenance, bug fixing and optimisation for the software and websites you already run — support from Re-EL.",
        lead="Ongoing maintenance, bug fixing and optimisation — technology does not stop at deployment.",
        intro=[
            "Deployment is not the end of a project; it is the point at which the system starts taking real load from real users. Things drift — dependencies age, browsers change, content goes stale, and small bugs surface once a hundred people are using the thing.",
            "Our support engagement keeps the system healthy: monitoring, fixes, updates and incremental improvements on a predictable monthly basis.",
        ],
        includes=[
            ("Bug fixing", "Reproducing, diagnosing and resolving defects reported by your team or your customers."),
            ("Maintenance", "Dependency updates, security patches, browser compatibility and content changes."),
            ("Optimisation", "Performance, conversion and accessibility improvements measured against real usage."),
            ("Continuous improvement", "Small, regular releases so the product keeps moving instead of piling up."),
        ],
        related_note="Support starts at R2,500 per month.",
    ),
    dict(
        slug="ui-ux-design", name="UI / UX Design",
        title="UI & UX Design Services South Africa | Re-EL",
        desc="Interfaces designed around real users — clear, fast and trustworthy UI and UX design from Re-EL.",
        lead="Interfaces designed around real users, built to feel fast, clear and trustworthy.",
        intro=[
            "Design here is not decoration applied after the fact. Interface decisions decide whether a form gets completed, whether an operator finds the right record, and whether anyone trusts the numbers on the dashboard.",
            "We design in the browser as well as on the canvas, so what is approved is what ships — including the empty states, the error states and the keyboard behaviour nobody screenshots.",
        ],
        includes=[
            ("Interface design", "Component libraries, layout systems and visual language built from your brand, not a theme."),
            ("User experience", "Flows, information architecture and interaction models shaped around how the task is really done."),
            ("Prototyping", "Clickable, testable prototypes used to settle arguments before engineering starts."),
            ("Design systems", "Documented, reusable components so the tenth screen is consistent with the first."),
        ],
        related_note="Design is scoped together with the build — quote on request.",
    ),
]

WORK = [
    dict(
        slug="clock-kit", name="Clock-Kit", marker="work-clockkit-poster.jpg",
        title="Clock-Kit — Workforce Management Platform Case Study | Re-EL",
        desc="Clock-Kit is a workforce attendance and clocking platform built by Re-EL to simplify shift tracking and reporting for teams.",
        cat="Workforce Management Platform",
        summary="A workforce attendance and clocking platform built to simplify shift tracking and reporting for teams.",
        stack=["JavaScript", "React", "Node.js", "MongoDB"],
        live="https://www.clock-kit.rf.gd/",
        overview=[
            "Attendance data is only useful if it is complete, unambiguous and easy to report on. Clock-Kit exists to replace the informal systems — paper registers, group chats and spreadsheets — that quietly lose hours every pay cycle.",
            "The platform gives teams a clear record of who clocked in, who did not, and what happened on each shift, then turns that record into reporting that a manager can act on without exporting anything by hand.",
        ],
        built=[
            "Employee clock-in and clock-out flows with a clear, low-friction interface for staff on the floor.",
            "Shift and attendance records structured for reliable reporting rather than free-text notes.",
            "Reporting views that summarise attendance by period so managers do not rebuild the data themselves.",
            "An administrative area for managing the people, shifts and rules behind the records.",
        ],
    ),
    dict(
        slug="re-v", name="Re-V", marker="work-rev-poster.jpg",
        title="Re-V — CV & Career Technology Platform Case Study | Re-EL",
        desc="Re-V is a CV generation and career technology platform built by Re-EL to help job seekers build professional, structured CVs.",
        cat="CV & Career Technology Platform",
        summary="A CV generation and career technology platform helping job seekers build professional, structured CVs.",
        stack=["React", "Node.js", "PDF Engine"],
        live="",
        overview=[
            "A CV is a structured document that most people assemble in a word processor, one inconsistent template at a time. Re-V treats it as data: capture the content once, then render it properly every time.",
            "The platform guides the writer through the sections a recruiter actually reads and produces a clean, consistently formatted document instead of a layout the applicant had to fight with.",
        ],
        built=[
            "Guided CV capture that breaks an intimidating document into manageable, prompted sections.",
            "A structured content model so the same information renders correctly on screen and on paper.",
            "A PDF generation engine on the server that produces consistent, readable output for every entry.",
            "Editing and re-export flows so a CV can be tailored for a role without starting over.",
        ],
    ),
    dict(
        slug="chatre", name="Chatre", marker="work-chatre-poster.jpg",
        title="Chatre — AI Productivity Platform Case Study | Re-EL",
        desc="Chatre is an AI-powered development and productivity platform built by Re-EL to speed up technical workflows.",
        cat="AI Productivity Platform",
        summary="An AI-powered development and productivity platform designed to speed up technical workflows.",
        stack=["AI", "APIs", "Automation"],
        live="",
        overview=[
            "Technical teams lose time to the same shapes of work repeatedly: summarising, drafting, transforming output from one tool into input for another, and re-deriving things that could be generated.",
            "Chatre puts models behind those steps as a product surface, with the plumbing — API keys, rate limits, retries, output handling — solved once rather than in every project.",
        ],
        built=[
            "A conversational product surface for prompting, refining and reusing technical output.",
            "API integration layer that manages model access, throttling and failure handling in one place.",
            "Automation hooks that move results out of the chat and into the workflow they belong to.",
            "Structured output handling so responses can be used as input downstream instead of copy-pasted.",
        ],
    ),
    dict(
        slug="webstudio", name="Re-EL WebStudio", marker="work-webstudio-poster.jpg",
        title="Re-EL WebStudio — Website Creation Platform Case Study | Re-EL",
        desc="Re-EL WebStudio is an internal platform by Re-EL for designing and shipping client websites faster, without losing quality.",
        cat="Website Creation Platform",
        summary="An internal platform for designing and shipping client websites faster, without losing quality.",
        stack=["React", "Design Systems", "Automation"],
        live="",
        overview=[
            "Every client site starts from the same unglamorous foundation: navigation, headings, metadata, performance budgets, accessibility, deployment. Re-EL WebStudio is where that foundation lives so each project starts from it rather than rebuilding it.",
            "It is our own tooling — the platform behind how we deliver client work faster without cutting the checks that make the work good.",
        ],
        built=[
            "A reusable component and design-system layer so new sites inherit a consistent visual language.",
            "Templated page structures with the accessibility and semantic markup already in place.",
            "Automation around build, asset processing and deployment to remove the manual release step.",
            "A shared foundation for performance, metadata and structured data across every project.",
        ],
    ),
]

POSTS = [
    dict(
        slug="website-cost-south-africa",
        title="How much does a website cost in South Africa?",
        desc="A clear, grounded breakdown of what Re-EL projects actually cost — websites from R2,500, applications from R5,000, automation from R1,500 and support from R2,500/month.",
        date="2026-10-07",
        date_display="7 October 2026",
        reading="5 min read",
        body="""
<h2>The short answer</h2>
<p>Re-EL publishes starting prices because guessing is disrespectful to everyone involved:</p>
<ul>
  <li><strong>Websites — from R2,500.</strong> Corporate sites, landing pages and web apps engineered for performance and conversion.</li>
  <li><strong>Applications — from R5,000.</strong> Custom platforms, business systems and internal tools built around how your company actually works.</li>
  <li><strong>Automation — from R1,500.</strong> Workflow automation that removes repetitive manual work and connects directly to your systems.</li>
  <li><strong>Support — from R2,500/mo.</strong> Ongoing maintenance, bug fixing and optimisation after launch.</li>
</ul>
<p>Those are floors, not fixed menu prices. Every project is different, so every quote is built from scope, complexity and requirements rather than a generic one-size-fits-all package.</p>

<h2>What actually moves the number</h2>
<p>Three things, in rough order of impact.</p>
<h3>1. Scope</h3>
<p>The number of distinct screens, roles and integrations is the largest driver. A five-page corporate site and a customer portal with authentication, payments and reporting are not the same object, and no honest estimate treats them as one.</p>
<h3>2. Integration</h3>
<p>Connecting payments, a CRM, a database or any third-party service adds real engineering: authentication, error handling, retries, reconciliation. Each connection is quoted on its own so you can see where the money goes.</p>
<h3>3. Content and readiness</h3>
<p>Projects slow down when copy, photography and approvals arrive late. Having your content organised before the build starts is the cheapest saving available to you.</p>

<h2>What is not optional</h2>
<p>Some things are part of how Re-EL builds, not line items you have to argue for:</p>
<ul>
  <li>Self-hosted fonts and assets — no third-party requests slowing the page down or leaking your visitors' data.</li>
  <li>Semantic heading structure, alt text and keyboard-visible focus states.</li>
  <li>Core Web Vitals work: lazy media, sized image slots and minimal layout shift.</li>
  <li>Metadata, canonical URLs and structured data so search engines understand the page.</li>
</ul>

<h2>How to get an accurate number</h2>
<p>Send the enquiry form with as much of the following as you already know:</p>
<ul>
  <li>What problem the thing solves, in one sentence.</li>
  <li>Who uses it — customers, staff, or both.</li>
  <li>What it has to connect to.</li>
  <li>What happens today instead.</li>
  <li>When you need it by, if that date is real.</li>
</ul>
<p>That is enough for a scoping conversation and a dated schedule with the quote. <a href="/#contact">Start a project</a>, message Re-EL on <a href="https://wa.me/27813864024" target="_blank" rel="noopener">WhatsApp</a>, or read more on the <a href="/services/">services pages</a>.</p>
""",
    ),
]


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------
def build_service(s, all_services):
    path = f"/services/{s['slug']}/"
    trail = [("Services", "/services/"), (s["name"], path)]
    icons = service_icon(s["name"])

    incl = "\n".join(
        f"      <article class=\"info-card\" data-reveal>\n"
        f"        <span class=\"card-kicker\">{esc(k)}</span>\n"
        f"        <h3>{esc(k)}</h3>\n"
        f"        <p>{esc(v)}</p>\n"
        f"      </article>"
        for k, v in s["includes"])

    others = [(o["name"], o["lead"], f"/services/{o['slug']}/")
              for o in all_services if o["slug"] != s["slug"]]

    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal><span class="page-icon">{icons}</span> SERVICE</p>
    <h1 data-reveal>{esc(s['name'])}</h1>
    <p class="lead" data-reveal>{esc(s['lead'])}</p>
    <div class="hero-tags" data-reveal><span>Strategy</span><span>Design</span><span>Build</span><span>Support</span></div>
  </header>

  <section class="section section-dark">
    <div class="container prose">
      {''.join(f'<p data-reveal>{esc(p)}</p>' for p in s['intro'])}
      <h2 data-reveal>What this covers</h2>
      <div class="card-grid">{incl}
      </div>
      <p data-reveal><strong>{esc(s['related_note'])}</strong> <a href="/#pricing">See the full price list</a>, or <a href="/#contact">send an enquiry</a> for a scoped quote.</p>
      <h2 data-reveal>How Re-EL works</h2>
      <p data-reveal>Discovery first, then design, then build, then deploy — the same <a href="/#process">four-step process</a> runs on every engagement, with a dated schedule issued alongside the quote so you know what happens when.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow" data-reveal>OTHER CAPABILITIES</p>
      <h2 class="section-title" data-reveal>Keep exploring.</h2>
      {cards([("Service", n, t, h) for n, t, h in others])}
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Have a technology problem?</h2>
      <p data-reveal>Let's turn it into a working solution.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Start a Project</a>
        <a href="mailto:info@re-el.co.za" class="btn btn-ghost" data-hover>Email Re-EL</a>
      </div>
    </div>
  </section>
</main>"""

    ld = [
        breadcrumb_ld(path, trail),
        {
            "@type": "Service",
            "@id": f"{SITE}{path}#service",
            "name": s["name"],
            "serviceType": s["name"],
            "description": s["lead"],
            "provider": {"@id": SITE + "/#organization"},
        },
    ]
    return page(path, s["title"], s["desc"], body, ld)


def build_work(w, all_work):
    path = f"/work/{w['slug']}/"
    trail = [("Work", "/work/"), (w["name"], path)]
    icon = work_icon(w["marker"])

    tags = "".join(f"<span>{esc(t)}</span>" for t in w["stack"])
    built = "\n".join(f"        <li>{esc(b)}</li>" for b in w["built"])
    live = (f'\n            <a href="{w["live"]}" target="_blank" rel="noopener" class="work-link" data-hover>Visit the live product &rarr;</a>'
            if w["live"] else "")

    others = [(o["name"], o["summary"], f"/work/{o['slug']}/")
              for o in all_work if o["slug"] != w["slug"]]

    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal><span class="page-icon">{icon}</span> CASE STUDY</p>
    <h1 data-reveal>{esc(w['name'])}</h1>
    <p class="lead" data-reveal>{esc(w['summary'])}</p>
    <div class="hero-tags" data-reveal>{tags}</div>
  </header>

  <section class="section section-dark">
    <div class="container prose">
      <p class="card-kicker" data-reveal>{esc(w['cat'])}</p>
      {''.join(f'<p data-reveal>{esc(p)}</p>' for p in w['overview'])}
      <h2 data-reveal>What we built</h2>
      <ul data-reveal>{built}</ul>{live}
    </div>
  </section>

  <section class="section">
    <div class="container">
      <p class="eyebrow" data-reveal>MORE WORK</p>
      <h2 class="section-title" data-reveal>Real products. Real systems.</h2>
      {cards([("Case study", n, t, h) for n, t, h in others])}
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Want something built like this?</h2>
      <p data-reveal>Let's turn your problem into a working solution.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Discuss a build</a>
        <a href="/work/" class="btn btn-ghost" data-hover>All work</a>
      </div>
    </div>
  </section>
</main>"""

    ld = [
        breadcrumb_ld(path, trail),
        {
            "@type": "CreativeWork",
            "@id": f"{SITE}{path}#work",
            "name": w["name"],
            "description": w["summary"],
            "creator": {"@id": SITE + "/#organization"},
            "keywords": ", ".join(w["stack"]),
        },
    ]
    return page(path, w["title"], w["desc"], body, ld)


def build_work_index():
    path = "/work/"
    trail = [("Work", path)]
    rows = cards([("Case study", w["name"], w["summary"], f"/work/{w['slug']}/")
                  for w in WORK])
    heading = ('      <p class="eyebrow" data-reveal>PORTFOLIO</p>\n'
               '      <h2 class="section-title" data-reveal>Real products. Real systems.</h2>')

    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal>PORTFOLIO</p>
    <h1 data-reveal>Work</h1>
    <p class="lead" data-reveal>Real products. Real systems. Four builds that show how Re-EL scopes, engineers and ships technology.</p>
  </header>

  <section class="section section-dark">
    <div class="container">
      {heading}
      {rows}
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Have a technology problem?</h2>
      <p data-reveal>Let's turn it into a working solution.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Start a Project</a>
        <a href="/services/" class="btn btn-ghost" data-hover>See services</a>
      </div>
    </div>
  </section>
</main>"""

    ld = [
        breadcrumb_ld(path, trail),
        {"@type": "CollectionPage", "@id": f"{SITE}{path}#collection",
         "name": "Re-EL work", "isPartOf": {"@id": SITE + "/#website"}},
    ]
    return page(path, "Work — Re-EL case studies",
                "Four Re-EL builds: Clock-Kit, Re-V, Chatre and Re-EL WebStudio — real products and real systems.",
                body, ld)


def build_services_index():
    path = "/services/"
    trail = [("Services", path)]
    rows = cards([("Service", s["name"], s["lead"], f"/services/{s['slug']}/")
                  for s in SERVICES])
    heading = ('      <p class="eyebrow" data-reveal>CAPABILITIES</p>\n'
               '      <h2 class="section-title" data-reveal>A full technology engine, not a freelance gig.</h2>')
    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal>CAPABILITIES</p>
    <h1 data-reveal>Services</h1>
    <p class="lead" data-reveal>A full technology engine, not a freelance gig — six capabilities that cover strategy, design, build and the years afterwards.</p>
  </header>

  <section class="section section-dark">
    <div class="container">
      {heading}
      {rows}
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Not sure which one you need?</h2>
      <p data-reveal>Describe the problem and we will scope it.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Start a Project</a>
        <a href="/#pricing" class="btn btn-ghost" data-hover>See pricing</a>
      </div>
    </div>
  </section>
</main>"""
    ld = [
        breadcrumb_ld(path, trail),
        {"@type": "ItemList", "@id": f"{SITE}{path}#list",
         "name": "Re-EL services",
         "itemListElement": [{"@type": "ListItem", "position": i, "name": s["name"],
                              "url": SITE + f"/services/{s['slug']}/"}
                             for i, s in enumerate(SERVICES, 1)]},
    ]
    return page(path, "Services — Re-EL",
                "Software development, web development, automation, API integration, tech support and UI/UX design from Re-EL.",
                body, ld)


def build_insights_index():
    path = "/insights/"
    trail = [("Insights", path)]
    rows = []
    for p in POSTS:
        rows.append(
            f'      <a class="info-card" href="/insights/{p["slug"]}/" data-reveal data-hover>\n'
            f'        <span class="card-kicker">{esc(p["date_display"])} &middot; {esc(p["reading"])}</span>\n'
            f'        <h3>{esc(p["title"])}</h3>\n'
            f'        <p>{esc(p["desc"])}</p>\n'
            f'        <span class="card-arrow">Read &rarr;</span>\n'
            f'      </a>')
    heading = ('      <p class="eyebrow" data-reveal>LATEST</p>\n'
               '      <h2 class="section-title" data-reveal>Read before you buy.</h2>')

    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal>INSIGHTS</p>
    <h1 data-reveal>Notes on building technology</h1>
    <p class="lead" data-reveal>Practical writing on scope, cost and delivery from the Re-EL team — no fluff, no inflated claims.</p>
  </header>

  <section class="section section-dark">
    <div class="container">
      {heading}
      <div class="card-grid">
{chr(10).join(rows)}
      </div>
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Have a question we have not answered?</h2>
      <p data-reveal>Ask it directly.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Contact Re-EL</a>
        <a href="/#faq" class="btn btn-ghost" data-hover>Read the FAQ</a>
      </div>
    </div>
  </section>
</main>"""
    ld = [
        breadcrumb_ld(path, trail),
        {"@type": "Blog", "@id": f"{SITE}{path}#blog", "name": "Re-EL Insights",
         "publisher": {"@id": SITE + "/#organization"}},
    ]
    return page(path, "Insights — Re-EL",
                "Writing from Re-EL on website cost, scope, delivery and building technology in South Africa.",
                body, ld, og_type="website")


def build_post(p):
    path = f"/insights/{p['slug']}/"
    trail = [("Insights", "/insights/"), ("Article", path)]
    body = f"""<main id="main">
{crumbs(trail)}
  <header class="page-hero container">
    <p class="eyebrow" data-reveal>INSIGHTS</p>
    <h1 data-reveal>{esc(p['title'])}</h1>
    <p class="lead" data-reveal>{esc(p['desc'])}</p>
    <div class="hero-tags" data-reveal><span>{esc(p['date_display'])}</span><span>{esc(p['reading'])}</span></div>
  </header>

  <section class="section section-dark">
    <div class="container prose" data-reveal>
{p['body']}
    </div>
  </section>

  <section class="cta-section page-cta">
    <div class="container">
      <h2 data-reveal>Want a scoped number for your project?</h2>
      <p data-reveal>Send the brief and we will come back with a quote.</p>
      <div class="hero-cta" data-reveal>
        <a href="/#contact" class="btn btn-primary" data-hover>Start a Project</a>
        <a href="/#faq" class="btn btn-ghost" data-hover>Read the FAQ</a>
      </div>
    </div>
  </section>
</main>"""

    ld = [
        breadcrumb_ld(path, trail),
        {"@type": "WebPage", "@id": SITE + path, "name": p["title"],
         "isPartOf": {"@id": SITE + "/#website"}},
        {
            "@type": "Article",
            "@id": f"{SITE}{path}#article",
            "headline": p["title"],
            "description": p["desc"],
            "datePublished": p["date"],
            "dateModified": p["date"],
            "author": {"@type": "Organization", "name": "Re-EL Branding & Technologies",
                       "@id": SITE + "/#organization"},
            "publisher": {"@id": SITE + "/#organization"},
            "mainEntityOfPage": {"@id": SITE + path},
        },
    ]
    return page(path, p["title"] + " | Re-EL", p["desc"], body, ld, og_type="article")


def build_thank_you():
    path = "/thank-you.html"
    body = """<main id="main">
  <section class="section" style="padding-top:180px;">
    <div class="container prose" style="text-align:center; max-width:640px; margin:0 auto;">
      <p class="eyebrow" data-reveal>MESSAGE SENT</p>
      <h1 data-reveal style="margin-top:16px;">Thank you.</h1>
      <p data-reveal>Your enquiry is with Re-EL. We will reply to the address you provided, usually within one business day.</p>
      <p data-reveal>If it is urgent, message us on <a href="https://wa.me/27813864024" target="_blank" rel="noopener">WhatsApp</a> or email <a href="mailto:info@re-el.co.za">info@re-el.co.za</a>.</p>
      <div class="hero-cta" data-reveal style="justify-content:center;">
        <a href="/" class="btn btn-primary" data-hover>Back to home</a>
        <a href="/work/" class="btn btn-ghost" data-hover>See our work</a>
      </div>
    </div>
  </section>
</main>"""
    ld = [{"@type": "WebPage", "@id": SITE + path, "name": "Thank you",
           "isPartOf": {"@id": SITE + "/#website"}}]
    return page(path, "Thank you — Re-EL",
                "Your enquiry has been sent to Re-EL. We will reply to the address you provided, or you can reach us immediately on WhatsApp or by email.", body, ld)


def build_404():
    """404 must not be indexed, and should not depend on the homepage build."""
    path = "/404.html"
    body = """<main id="main">
  <section class="section" style="padding-top:180px;">
    <div class="container prose" style="text-align:center; max-width:640px; margin:0 auto;">
      <p class="eyebrow">404</p>
      <h1 style="margin-top:16px;">That page is not here.</h1>
      <p>The link may be old, or the address may have a typo. Everything Re-EL publishes is reachable from the homepage.</p>
      <div class="hero-cta" style="justify-content:center;">
        <a href="/" class="btn btn-primary">Back to home</a>
        <a href="/services/" class="btn btn-ghost">Browse services</a>
      </div>
    </div>
  </section>
</main>"""
    ld = [{"@type": "WebPage", "@id": SITE + path, "name": "Page not found"}]
    doc = page(path, "Page not found — Re-EL",
               "The page you were looking for does not exist on re-el.co.za. Head back to the homepage, or browse Re-EL services, work and insights.", body, ld)
    # rewrite robots for the error page
    t = doc.read_text(encoding="utf-8")
    t = t.replace('content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"',
                  'content="noindex, follow"', 1)
    doc.write_text(t, encoding="utf-8")
    return doc


def build_service_icon_map():
    """`<h3>Name</h3>` -> preceding inline SVG, shared by every service page."""
    return {m.group(2): m.group(1)
            for m in re.finditer(r"(<svg[^>]*>.*?</svg>)\s*<h3>([^<]+)</h3>", SRC, re.S)}



TODAY = "2026-10-07"


def build_sitemap():
    """Regenerate sitemap.xml from the page list. Utility pages are excluded."""
    urls = [(f"/", "1.0", "monthly", "2026-10-06"),
            ("/services/", "0.9", "monthly", TODAY),
            ("/work/", "0.9", "monthly", TODAY),
            ("/insights/", "0.8", "weekly", TODAY)]
    urls += [(f"/services/{x['slug']}/", "0.8", "monthly", TODAY) for x in SERVICES]
    urls += [(f"/work/{x['slug']}/", "0.7", "yearly", TODAY) for x in WORK]
    urls += [(f"/insights/{x['slug']}/", "0.6", "yearly", TODAY) for x in POSTS]

    rows = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, freq, mod in sorted(urls, key=lambda u: (u[0] != "/", u[0])):
        rows += ["  <url>",
                 f"    <loc>{SITE}{loc}</loc>",
                 f"    <lastmod>{mod}</lastmod>",
                 f"    <changefreq>{freq}</changefreq>",
                 f"    <priority>{prio}</priority>",
                 "  </url>"]
    rows.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(urls)



def main():
    build_service_icon_map()
    out = [build_services_index()]
    for s in SERVICES:
        out.append(build_service(s, SERVICES))
    out.append(build_work_index())
    for w in WORK:
        out.append(build_work(w, WORK))
    out.append(build_insights_index())
    for p in POSTS:
        out.append(build_post(p))
    out.append(build_thank_you())
    out.append(build_404())
    print(f"  wrote sitemap.xml ({build_sitemap()} urls)")
    for f in out:
        print("  wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

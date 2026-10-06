/* Re-EL — Main interaction & animation controller */
document.addEventListener('DOMContentLoaded', () => {
  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  if(window.lucide) lucide.createIcons();

  const yearEl = $('#year');
  if(yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- ENVIRONMENT CAPABILITY FLAGS ---------- */
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let reduced = motionQuery.matches;
  motionQuery.addEventListener('change', e => { reduced = e.matches; });

  const HAS_GSAP = typeof window.gsap !== 'undefined' && typeof window.ScrollTrigger !== 'undefined';
  const HAS_THREE = typeof window.THREE !== 'undefined';
  const canAnimate = HAS_GSAP && !reduced;

  /* Reveal observer is created up front: startExperience() can run during
     loader setup, well before initReveals() is defined. */
  const revealObserver = 'IntersectionObserver' in window
    ? new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if(!entry.isIntersecting) return;
          revealObserver.unobserve(entry.target);
          if(entry.target.__revealTween) entry.target.__revealTween.play();
        });
      }, { rootMargin:'0px 0px -10% 0px', threshold:0.1 })
    : { observe(el){ if(el.__revealTween) el.__revealTween.play(); }, unobserve(){} };

  if(HAS_GSAP) gsap.registerPlugin(ScrollTrigger);

  /* ---------- LOADER ---------- */
  const loader = $('#loader');
  const seen = sessionStorage.getItem('reel_loaded');
  let started = false;

  function startExperience(){
    if(started) return;
    started = true;
    initReveals();
    initTimelineFill();
  }

  function finishLoader(){
    loader.classList.add('hidden');
    startExperience();
    setTimeout(() => loader.remove(), 700);
  }

  if(!HAS_GSAP || reduced || seen){
    if(loader){ loader.style.display = 'none'; loader.remove(); }
    startExperience();
  } else {
    const lines = $$('.loader-line');
    const fill  = $('.loader-bar-fill');
    const pct   = $('.loader-percent');
    const tl = gsap.timeline({ onComplete: () => {
      sessionStorage.setItem('reel_loaded','1');
      finishLoader();
    }});
    tl.to(lines, { opacity:1, y:0, stagger:0.15, duration:0.3 })
      .to({ val:0 }, {
        val:100, duration:1,
        onUpdate(){
          const v = Math.round(this.targets()[0].val);
          if(fill) fill.style.width = v + '%';
          if(pct) pct.textContent = v + '%';
        }
      }, 0.3)
      .to({}, { duration:0.3 });
  }

  /* ---------- LENIS SMOOTH SCROLL ---------- */
  if(canAnimate && window.innerWidth > 768 && typeof window.Lenis !== 'undefined'){
    const lenis = new Lenis({ duration:1.1, smoothWheel:true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(time => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  /* ---------- REFRESH TRIGGERS ONCE WEBFONTS SETTLE ---------- */
  if(HAS_GSAP && document.fonts && document.fonts.ready){
    document.fonts.ready.then(() => ScrollTrigger.refresh());
  }
  window.addEventListener('load', () => { if(HAS_GSAP) ScrollTrigger.refresh(); });

  /* ---------- NAV: SCROLLED STATE (rAF-throttled) ---------- */
  const nav = $('#siteNav');
  let navTicking = false;
  const syncNav = () => {
    navTicking = true;
    requestAnimationFrame(() => {
      if(nav) nav.classList.toggle('scrolled', window.scrollY > 40);
      navTicking = false;
    });
  };
  window.addEventListener('scroll', syncNav, { passive:true });
  syncNav();

  /* ---------- NAV: SCROLL SPY ---------- */
  const navLinks = $$('.nav-links a');
  const spyTargets = navLinks
    .map(a => ({ link:a, section:$(a.getAttribute('href')) }))
    .filter(s => s.section);

  if(spyTargets.length && 'IntersectionObserver' in window){
    const hero = $('.hero');
    const clearActive = () => navLinks.forEach(l => l.classList.remove('is-active'));
    const setActive = section => {
      navLinks.forEach(l => l.classList.toggle('is-active', l.getAttribute('href') === `#${section.id}`));
    };
    const spy = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if(!e.isIntersecting) return;
        // At the hero there is no matching nav link, so clear rather than
        // leaving whatever was last highlighted stuck on screen.
        if(e.target === hero) clearActive();
        else setActive(e.target);
      });
    }, { rootMargin:'-45% 0px -50% 0px' });
    spyTargets.forEach(s => spy.observe(s.section));
    if(hero) spy.observe(hero);
  }

  /* ---------- MOBILE MENU ---------- */
  const menuBtn = $('#menuBtn');
  const mobileMenu = $('#mobileMenu');
  const FOCUSABLE = 'a[href], button:not([disabled]), input, select, textarea';

  if(menuBtn && mobileMenu){
    let lastFocus = null;

    const menuIsOpen = () => mobileMenu.classList.contains('active');

    function setMenu(open){
      mobileMenu.classList.toggle('active', open);
      menuBtn.classList.toggle('active', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      mobileMenu.setAttribute('aria-hidden', String(!open));
      document.body.style.overflow = open ? 'hidden' : '';

      if(open){
        lastFocus = document.activeElement;
        const first = $(FOCUSABLE, mobileMenu);
        if(first) first.focus();
      } else if(lastFocus && document.body.contains(lastFocus)){
        lastFocus.focus();
      }
    }

    menuBtn.addEventListener('click', () => setMenu(!menuIsOpen()));

    mobileMenu.addEventListener('click', e => {
      if(e.target.closest('a')) setMenu(false);
    });

    document.addEventListener('keydown', e => {
      if(!menuIsOpen()) return;

      if(e.key === 'Escape'){ setMenu(false); return; }

      if(e.key === 'Tab'){
        const items = $$(FOCUSABLE, mobileMenu).filter(el => el.offsetParent !== null);
        if(!items.length) return;
        const first = items[0];
        const last  = items[items.length - 1];
        if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
        else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
      }
    });
  }

  /* ---------- CUSTOM CURSOR ---------- */
  const finePointer = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  if(finePointer && HAS_GSAP && !reduced){
    const ring = $('#cursorRing');
    const dot  = $('#cursorDot');

    // Centre via GSAP, not CSS translate — GSAP owns the transform here.
    gsap.set([ring, dot], { xPercent:-50, yPercent:-50 });

    const ringX = gsap.quickTo(ring, 'x', { duration:0.5, ease:'power3' });
    const ringY = gsap.quickTo(ring, 'y', { duration:0.5, ease:'power3' });
    const dotX  = gsap.quickTo(dot,  'x', { duration:0.1 });
    const dotY  = gsap.quickTo(dot,  'y', { duration:0.1 });

    window.addEventListener('mousemove', e => {
      ringX(e.clientX); ringY(e.clientY);
      dotX(e.clientX);  dotY(e.clientY);
    }, { passive:true });

    const INTERACTIVE = 'a[href], button, input, select, textarea, [data-hover]';
    document.addEventListener('mouseover', e => {
      if(e.target.closest(INTERACTIVE)) ring.classList.add('hovered');
    });
    document.addEventListener('mouseout', e => {
      if(e.target.closest(INTERACTIVE)) ring.classList.remove('hovered');
    });
  }

  /* ---------- SCROLL REVEAL ---------- */
  function initReveals(){
    const heroLines  = $$('.hero-title .line');
    const heroRest   = $$('.hero [data-reveal]').filter(el => !el.classList.contains('line'));
    const belowFold  = $$('[data-reveal]').filter(el => !el.closest('.hero'));

    if(!canAnimate){
      // No JS, no GSAP or reduced motion: make sure nothing is left hidden.
      [heroLines, heroRest, belowFold].flat().forEach(el => {
        el.style.opacity = '';
        el.style.transform = '';
      });
      return;
    }

    // Masked title reveal: .line has overflow:hidden, so yPercent 100 -> 0 slides it up.
    gsap.set(heroLines, { opacity:1, yPercent:100 });
    gsap.set([...heroRest, ...belowFold], { opacity:0, y:30 });

    gsap.timeline({ delay:0.1 })
      .to(heroLines, { yPercent:0, duration:1, stagger:0.12, ease:'expo.out' })
      .to(heroRest, { opacity:1, y:0, duration:0.8, stagger:0.1, ease:'power3.out' }, '-=0.55');

    belowFold.forEach(el => {
      // IntersectionObserver rather than ScrollTrigger: reveals only need
      // "has this entered the viewport", and IO has no stale-geometry risk
      // while fonts/layout settle.
      const tween = gsap.to(el, {
        opacity:1, y:0, duration:0.9, ease:'power3.out', paused:true
      });
      revealObserver.observe(el);
      el.__revealTween = tween;
    });
  }

  /* ---------- HERO WORD CYCLE ---------- */
  const wordEl = $('#wordCycle');
  if(wordEl && canAnimate){
    const words = ['forward','faster','smarter','connected','transformed'];
    let index = 0;
    let timer = null;
    let heroVisible = true;
    let tabVisible  = !document.hidden;

    function startCycle(){
      if(timer) return;
      timer = setInterval(() => {
        index = (index + 1) % words.length;
        gsap.timeline()
          .to(wordEl, { opacity:0, y:-10, duration:0.28, ease:'power2.in' })
          .call(() => { wordEl.textContent = words[index]; })
          .fromTo(wordEl, { opacity:0, y:10 }, { opacity:1, y:0, duration:0.28, ease:'power2.out' });
      }, 2600);
    }

    function stopCycle(){
      if(timer){ clearInterval(timer); timer = null; }
      gsap.set(wordEl, { opacity:1, y:0 });
    }

    function syncCycle(){ (heroVisible && tabVisible) ? startCycle() : stopCycle(); }

    const hero = $('.hero');
    if(hero && 'IntersectionObserver' in window){
      new IntersectionObserver(([entry]) => {
        heroVisible = entry.isIntersecting;
        syncCycle();
      }, { threshold:0 }).observe(hero);
    }

    document.addEventListener('visibilitychange', () => {
      tabVisible = !document.hidden;
      syncCycle();
    });
  }

  /* ---------- PROCESS TIMELINE FILL ---------- */
  function initTimelineFill(){
    const fill = $('#timelineFill');
    if(!fill) return;
    if(!canAnimate){ fill.style.width = '100%'; return; }
    gsap.to(fill, {
      width:'100%',
      ease:'none',
      scrollTrigger:{
        trigger:'#process .timeline',
        start:'top 70%',
        end:'bottom 60%',
        scrub:1
      }
    });
  }

  /* ---------- SERVICE SELECT -> WHATSAPP MESSAGE ---------- */
  const WA_NUMBER = '27813864024'; // +27 81 386 4024
  const serviceSelect = $('#serviceSelect');
  const whatsappFloat = $('#whatsappFloat');

  function updateWhatsapp(service){
    if(!whatsappFloat) return;
    const msg = `Hi Re-EL, I would like to enquire about ${ (service || 'software development').toLowerCase() }.`;
    whatsappFloat.href = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`;
  }

  if(serviceSelect){
    updateWhatsapp('');
    serviceSelect.addEventListener('change', e => updateWhatsapp(e.target.value));
  }

  /* ---------- CONTACT FORM ---------- */
  const form = $('#contactForm');
  const note = $('#formNote');
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  const FIELD_LABELS = {
    name:'Full name',
    email:'Email',
    phone:'Phone',
    service:'Service',
    message:'Project description'
  };

  function setFieldError(input, message){
    const holder = input.closest('label');
    let error = holder && holder.querySelector('.field-error');

    if(!error && holder){
      error = document.createElement('span');
      error.className = 'field-error';
      error.id = `${input.name}-error`;
      error.setAttribute('role', 'alert');
      holder.appendChild(error);
    }

    if(message){
      input.setAttribute('aria-invalid', 'true');
      if(error){
        error.textContent = message;
        input.setAttribute('aria-describedby', error.id);
      }
    } else {
      input.removeAttribute('aria-invalid');
      input.removeAttribute('aria-describedby');
      if(error) error.textContent = '';
    }
  }

  function validateField(input){
    const value = (input.value || '').trim();
    const label = FIELD_LABELS[input.name] || 'This field';
    let message = '';

    if(input.required && !value){
      message = `${label} is required.`;
    } else if(input.type === 'email' && value && !EMAIL_RE.test(value)){
      message = 'Enter a valid email address.';
    }

    setFieldError(input, message);
    return !message;
  }

  if(form){
    const fields = ['name','company','email','phone','service','budget','message','timeline']
      .map(n => form.elements[n])
      .filter(Boolean);

    // Clear a field's error as soon as the visitor starts fixing it.
    fields.forEach(input => {
      input.addEventListener('input', () => {
        if(input.getAttribute('aria-invalid') === 'true') validateField(input);
      });
      input.addEventListener('change', () => {
        if(input.getAttribute('aria-invalid') === 'true') validateField(input);
      });
    });

    form.addEventListener('submit', e => {
      e.preventDefault();

      // Honeypot
      if(form.elements.company_website && form.elements.company_website.value) return;

      const required = fields.filter(f => f.required);
      const results  = required.map(validateField);
      const allValid  = results.every(Boolean);

      if(!allValid){
        const firstBad = required[results.indexOf(false)];
        if(firstBad) firstBad.focus();
        if(note) note.textContent = 'Please correct the highlighted fields and try again.';
        return;
      }

      const data = Object.fromEntries(new FormData(form).entries());

      const subject = `New Enquiry — ${data.service} (${data.name})`;
      const body = [
        `Name: ${data.name}`,
        `Company: ${data.company || '-'}`,
        `Email: ${data.email}`,
        `Phone: ${data.phone || '-'}`,
        `Service: ${data.service}`,
        `Budget: ${data.budget || '-'}`,
        `Timeline: ${data.timeline || '-'}`,
        '',
        'Project Description:',
        data.message
      ].join('\n');

      required.forEach(f => setFieldError(f, ''));
      window.location.href = `mailto:info@re-el.co.za?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      if(note) note.textContent = 'Opening your email client to send this enquiry to info@re-el.co.za…';
      form.reset();
    });
  }

  /* ---------- MEDIA (backdrop reveal + viewport-gated video) ---------- */
  function initMedia(){
    const items = $$('[data-media]');
    const videos = $$('video[data-reel-video]');
    if(!items.length && !videos.length) return;

    const play = v => {
      if(reduced){ v.pause(); return; }
      const p = v.play();
      if(p && typeof p.catch === 'function') p.catch(() => {});
    };
    const show = el => {
      el.classList.add('is-in');
      $$('video[data-reel-video]', el).forEach(play);
    };

    videos.forEach(v => v.addEventListener('playing', () => {
      const wrap = v.closest('[data-media]');
      if(wrap) wrap.classList.add('is-playing');
    }));

    if(!('IntersectionObserver' in window)){
      items.forEach(show);
    }else{
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if(e.isIntersecting) show(e.target);
          else $$('video[data-reel-video]', e.target).forEach(v => v.pause());
        });
      }, { rootMargin:'0px 0px -10% 0px', threshold:0 });
      items.forEach(el => io.observe(el));
    }

    // Honour a live switch to reduced motion without a reload.
    motionQuery.addEventListener('change', e => {
      if(!e.matches) return;
      videos.forEach(v => v.pause());
      items.forEach(el => el.classList.add('is-in'));
    });
  }
  initMedia();

  /* ---------- FOOTER GIANT HOVER ---------- */
  const giant = $('#footerGiant');
  if(giant && canAnimate){
    // scaleX is compositor-friendly; animating letter-spacing is not.
    const tl = gsap.timeline({ paused:true })
      .to(giant, { scaleX:1.06, duration:0.5, ease:'power3.out' });

    gsap.set(giant, { transformOrigin:'center center', willChange:'transform' });

    giant.addEventListener('mouseenter', () => tl.play());
    giant.addEventListener('mouseleave', () => tl.reverse());
  }
});

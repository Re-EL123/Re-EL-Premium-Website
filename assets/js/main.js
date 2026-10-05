/* Re-EL — Main interaction & animation controller */
document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  document.getElementById('year').textContent = new Date().getFullYear();

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- LOADER ---------- */
  const loader = document.getElementById('loader');
  const seen = sessionStorage.getItem('reel_loaded');

  function finishLoader(){
    loader.classList.add('hidden');
    runHeroEntrance();
    setTimeout(()=> loader.remove(), 700);
  }

  if(seen || reduced){
    loader.style.display = 'none';
    runHeroEntrance();
  } else {
    const lines = document.querySelectorAll('.loader-line');
    const fill = document.querySelector('.loader-bar-fill');
    const pct = document.querySelector('.loader-percent');
    const tl = gsap.timeline({ onComplete: () => {
      sessionStorage.setItem('reel_loaded','1');
      finishLoader();
    }});
    tl.to(lines, { opacity:1, y:0, stagger:0.15, duration:0.3 })
      .to({val:0}, {
        val:100, duration:1,
        onUpdate: function(){
          const v = Math.round(this.targets()[0].val);
          fill.style.width = v+'%';
          pct.textContent = v+'%';
        }
      }, 0.3)
      .to({}, { duration:0.3 });
  }

  /* ---------- LENIS SMOOTH SCROLL ---------- */
  if(!reduced && window.innerWidth > 768){
    const lenis = new Lenis({ duration:1.1, smoothWheel:true });
    function raf(time){ lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    lenis.on('scroll', ScrollTrigger.update);
  }

  /* ---------- NAV ---------- */
  const nav = document.getElementById('siteNav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
  });

  const menuBtn = document.getElementById('menuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  menuBtn.addEventListener('click', () => {
    const active = mobileMenu.classList.toggle('active');
    menuBtn.classList.toggle('active', active);
    menuBtn.setAttribute('aria-expanded', active);
    document.body.style.overflow = active ? 'hidden' : '';
  });
  mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    mobileMenu.classList.remove('active');
    menuBtn.classList.remove('active');
    document.body.style.overflow = '';
  }));

  /* ---------- CUSTOM CURSOR ---------- */
  if(window.matchMedia('(hover:hover) and (pointer:fine)').matches){
    const ring = document.getElementById('cursorRing');
    const dot = document.getElementById('cursorDot');
    const ringX = gsap.quickTo(ring, 'x', { duration:0.5, ease:'power3' });
    const ringY = gsap.quickTo(ring, 'y', { duration:0.5, ease:'power3' });
    const dotX = gsap.quickTo(dot, 'x', { duration:0.1 });
    const dotY = gsap.quickTo(dot, 'y', { duration:0.1 });

    window.addEventListener('mousemove', e => {
      ringX(e.clientX); ringY(e.clientY);
      dotX(e.clientX); dotY(e.clientY);
    });

    document.querySelectorAll('[data-hover]').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('hovered'));
      el.addEventListener('mouseleave', () => ring.classList.remove('hovered'));
    });
  }

  /* ---------- HERO WORD REVEAL + ENTRANCE ---------- */
  function runHeroEntrance(){
    gsap.set('[data-reveal]', { opacity:0, y:30 });
    const heroLines = document.querySelectorAll('.hero-title .line');
    gsap.timeline({ delay:0.1 })
      .to(heroLines, { opacity:1, y:0, duration:0.9, stagger:0.15, ease:'power3.out' })
      .to('.hero-sub, .hero-cta, .hero-status', { opacity:1, y:0, duration:0.7, stagger:0.1 }, '-=0.4');

    // Reveal everything else below the fold via ScrollTrigger
    document.querySelectorAll('[data-reveal]').forEach(el => {
      if(el.closest('.hero')) return;
      gsap.to(el, {
        opacity:1, y:0, duration:0.9, ease:'power3.out',
        scrollTrigger:{ trigger: el, start:'top 85%' }
      });
    });

    initTimelineFill();
  }

  /* ---------- WORD CYCLE ---------- */
  const words = ['forward','faster','smarter','connected','transformed'];
  let wIndex = 0;
  const wordEl = document.getElementById('wordCycle');
  if(wordEl && !reduced){
    setInterval(() => {
      wIndex = (wIndex+1) % words.length;
      gsap.to(wordEl, { opacity:0, y:-10, duration:0.3, onComplete:()=>{
        wordEl.textContent = words[wIndex];
        gsap.fromTo(wordEl, {opacity:0,y:10}, {opacity:1,y:0,duration:0.3});
      }});
    }, 2600);
  }

  /* ---------- PROCESS TIMELINE FILL ---------- */
  function initTimelineFill(){
    const fill = document.getElementById('timelineFill');
    if(!fill) return;
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

  /* ---------- SERVICE SELECT → WHATSAPP MESSAGE ---------- */
  const serviceSelect = document.getElementById('serviceSelect');
  const whatsappFloat = document.getElementById('whatsappFloat');
  const WA_NUMBER = '27000000000'; // TODO: replace with real WhatsApp number
  function updateWhatsapp(service){
    const msg = `Hi Re-EL, I would like to enquire about ${ (service || 'software development').toLowerCase() }.`;
    whatsappFloat.href = `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`;
  }
  if(serviceSelect){
    serviceSelect.addEventListener('change', e => updateWhatsapp(e.target.value));
  }

  /* ---------- CONTACT FORM (mailto fallback — swap for /api/contact later) ---------- */
  const form = document.getElementById('contactForm');
  const note = document.getElementById('formNote');
  if(form){
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      // honeypot
      if(form.company_website.value){ return; }

      const data = Object.fromEntries(new FormData(form).entries());
      if(!data.name || !data.email || !data.service || !data.message){
        note.textContent = 'Please complete all required fields.';
        return;
      }

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

      window.location.href = `mailto:info@re-el.co.za?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      note.textContent = 'Opening your email client to send this enquiry to info@re-el.co.za…';
      form.reset();
    });
  }

  /* ---------- FOOTER GIANT HOVER SEPARATE/RECONNECT ---------- */
  const giant = document.getElementById('footerGiant');
  if(giant){
    giant.addEventListener('mouseenter', () => {
      gsap.to(giant, { letterSpacing:'0.25em', duration:0.5, ease:'power3.out' });
    });
    giant.addEventListener('mouseleave', () => {
      gsap.to(giant, { letterSpacing:'0.02em', duration:0.5, ease:'power3.out' });
    });
  }
});

/* Re-EL analytics + verification
   ------------------------------------------------------------------
   Every entry below is optional. While the config is empty this file
   does nothing at all: no network requests, no globals, no cookies.

   To switch one on, fill in the value and redeploy.

     plausibleDomain : Plausible dashboard site domain, e.g. 're-el.co.za'
     ga4MeasurementId: Google Analytics 4 measurement ID, e.g. 'G-XXXXXXXXXX'
     searchConsole   : Google Search Console verification code. Filling this
                       in injects the <meta name="google-site-verification">
                       tag. Search Console can also verify by DNS or by the
                       existing sitemap — add the tag here only if you want
                       the meta-tag method.

   Google Tag Manager is not used; GA4 is loaded directly so the site stays
   free of third-party tag containers.
*/
(function () {
  'use strict';

  var CFG = {
    plausibleDomain: '',
    ga4MeasurementId: '',
    searchConsole: ''
  };

  var root = document.documentElement;
  var DNT = (navigator.doNotTrack === '1' || window.doNotTrack === '1');

  function inject(tag, attrs) {
    var el = document.createElement(tag);
    for (var k in attrs) el.setAttribute(k, attrs[k]);
    (document.head || document.documentElement).appendChild(el);
    return el;
  }

  if (CFG.searchConsole) {
    inject('meta', {
      name: 'google-site-verification',
      content: CFG.searchConsole
    });
  }

  // Plausible — cookieless, privacy-friendly, DNT respected by the script.
  if (CFG.plausibleDomain && !DNT) {
    inject('script', {
      defer: '',
      'data-domain': CFG.plausibleDomain,
      src: 'https://plausible.io/js/script.js'
    });
  }

  // Google Analytics 4 — loaded async, anonymised IP by default.
  if (CFG.ga4MeasurementId && !DNT) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', CFG.ga4MeasurementId, { anonymize_ip: true });

    inject('script', { async: '', src: 'https://www.googletagmanager.com/gtag/js?id=' + CFG.ga4MeasurementId });
  }

  // Small, self-describing marker so the loaded state is inspectable in devtools.
  root.setAttribute('data-analytics', [
    CFG.plausibleDomain ? 'plausible' : '',
    CFG.ga4MeasurementId ? 'ga4' : '',
    CFG.searchConsole ? 'gsc' : ''
  ].filter(Boolean).join(' ') || 'off');
})();

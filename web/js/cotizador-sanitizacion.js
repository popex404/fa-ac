(function () {
  'use strict';

  /* ============================================================
     Cotizador especializado de Sanitización — clon de
     js/cotizador-termitas.js, mismo patron.
     ============================================================ */

  var WA_NUMBER = '56936678897';
  var WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbyhEpYG3w91Z8gAT8tTvS5UTmFvJmqF2TbAfIUmHtAj28yg2rCYv1mBQ3SwoCkYDC6e9Q/exec';
  var PAGE_SLUG = 'landing-sanitizacion';

  var LBL = {
    indicio:   { 'certificado':'necesita certificado SEREMI', 'brote':'contagio o brote reciente', 'reapertura':'reapertura de local', 'periodica':'sanitización periódica' },
    propiedad: { casa:'casa', departamento:'departamento', comercial:'local comercial', oficina:'oficina', bodega:'bodega/galpón', institucion:'institución' },
    tamano:    { pequeno:'pequeño (< 80 m²)', mediano:'mediano (80–200 m²)', grande:'grande (> 200 m²)' },
    urgencia:  { normal:'normal (48h)', urgente:'urgente (24h)', emergencia:'emergencia (hoy)' }
  };

  var STEPS = [
    {
      id: 'indicio', question: '¿Qué necesitas?', subtitle: 'Elige lo que más se parece a tu caso',
      options: [
        { value:'certificado', label:'Certificado SEREMI',   icon:'📋' },
        { value:'brote',       label:'Contagio o brote',     icon:'🦠' },
        { value:'reapertura',  label:'Reapertura de local',  icon:'🔓' },
        { value:'periodica',   label:'Sanitización periódica', icon:'📅' }
      ]
    },
    {
      id: 'propiedad', question: '¿Qué tipo de inmueble?', subtitle: 'El espacio que necesita sanitización',
      options: [
        { value:'casa',         label:'Casa',            icon:'🏠' },
        { value:'departamento', label:'Departamento',    icon:'🏢' },
        { value:'comercial',    label:'Local comercial', icon:'🏪' },
        { value:'oficina',      label:'Oficina',         icon:'💼' },
        { value:'bodega',       label:'Bodega / Galpón', icon:'🏭' },
        { value:'institucion',  label:'Institución',     icon:'🏫' }
      ]
    },
    {
      id: 'tamano', question: '¿Qué tamaño tiene el espacio?', subtitle: 'Tamaño aproximado a sanitizar',
      options: [
        { value:'pequeno', label:'Pequeño', sublabel:'Menos de 80 m²', icon:'📦' },
        { value:'mediano', label:'Mediano', sublabel:'80 – 200 m²',    icon:'🏠' },
        { value:'grande',  label:'Grande',  sublabel:'Más de 200 m²',  icon:'🏗️' }
      ]
    },
    {
      id: 'urgencia', question: '¿Qué tan urgente es?', subtitle: 'La urgencia determina el orden de atención',
      options: [
        { value:'normal',     label:'Normal',     sublabel:'Atención en 48h', icon:'📅' },
        { value:'urgente',    label:'Urgente',     sublabel:'Atención en 24h', icon:'⚡' },
        { value:'emergencia', label:'Emergencia',  sublabel:'Atención hoy',    icon:'🚨' }
      ]
    }
  ];

  var EXPIRY_MS = 24 * 60 * 60 * 1000;
  var WA_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';

  function datosBloque(ans, contact, ref) {
    var indicio = LBL.indicio[ans.indicio] || ans.indicio;
    var prop    = LBL.propiedad[ans.propiedad] || ans.propiedad;
    var tam     = LBL.tamano[ans.tamano] || ans.tamano;
    var urg     = LBL.urgencia[ans.urgencia] || ans.urgencia;
    return '\n\n--- DATOS DE COTIZACIÓN (SANITIZACIÓN) ---' +
           '\nRef: ' + ref +
           '\nNombre: ' + ((contact && contact.nombre) || '-') +
           '\nCorreo: ' + ((contact && contact.correo) || '-') +
           '\nCiudad: ' + ((contact && contact.ciudad) || '-') +
           '\nNecesidad: ' + indicio +
           '\nInmueble: ' + prop +
           '\nTamaño: ' + tam +
           '\nUrgencia: ' + urg;
  }

  function buildWASanitizacion(ans, contact, ref) {
    var indicio = LBL.indicio[ans.indicio] || ans.indicio;
    var nombre  = (contact && contact.nombre) ? contact.nombre : '';
    var ciudad  = (contact && contact.ciudad) ? contact.ciudad : '';
    var intro   = nombre ? 'Hola, soy ' + nombre + '. ' : 'Hola. ';
    var loc     = ciudad ? 'en ' + ciudad + ' ' : '';
    var msg     = intro + 'Necesito un servicio de sanitización ' + loc + '(' + indicio + '). ¿Cuándo me pueden visitar?';
    return 'https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg + datosBloque(ans, contact, ref));
  }

  function postWebhook(ans, contact, cta, ref) {
    if (!WEBHOOK_URL) return;
    var utcM4  = new Date(Date.now() - 4 * 60 * 60 * 1000);
    var isoStr = utcM4.toISOString();
    var fecha  = isoStr.slice(8,10) + '/' + isoStr.slice(5,7) + '/' + isoStr.slice(0,4);
    var hora   = isoStr.slice(11,16);
    var payload = {
      ref:        ref || '',
      fecha:      fecha,
      hora:       hora,
      nombre:     contact.nombre || '',
      correo:     contact.correo || '',
      ciudad:     contact.ciudad || '',
      plaga:      'sanitizacion',
      indicio:    ans.indicio || 'N/A',
      propiedad:  ans.propiedad,
      tamano:     ans.tamano,
      urgencia:   ans.urgencia,
      precio_min: '',
      precio_max: '',
      source:        PAGE_SLUG,
      cta:           cta || 'Seccion-Cotizador',
      pagina_origen: window.location.pathname
    };
    try {
      fetch(WEBHOOK_URL, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(payload) })
        .catch(function () {});
    } catch (e) {}
  }

  function createCotizador(widgetEl) {
    var cta = widgetEl.getAttribute('data-cta') ||
      (widgetEl.id === 'cotizador-modal-widget' ? 'Modal' : 'Seccion-Cotizador');
    var domId      = widgetEl.id || 'widget';
    var storageKey = 'fa_cot_' + PAGE_SLUG + '_' + domId;
    var state      = { step: 0, answers: {}, contact: { nombre: '', correo: '', ciudad: '' } };

    function save() {
      try { localStorage.setItem(storageKey, JSON.stringify({ step: state.step, answers: state.answers, contact: state.contact, ts: Date.now() })); } catch (e) {}
    }
    function load() {
      try {
        var d = JSON.parse(localStorage.getItem(storageKey));
        if (!d || Date.now() - d.ts > EXPIRY_MS) { localStorage.removeItem(storageKey); return null; }
        return d;
      } catch (e) { return null; }
    }
    function clear() { try { localStorage.removeItem(storageKey); } catch (e) {} }

    function render() {
      widgetEl.innerHTML = '';
      if (state.step < STEPS.length)       renderStep();
      else if (state.step === STEPS.length) renderContact();
      else                                  renderResult();
    }

    function renderProgress(cur, total, showBack) {
      var prog = document.createElement('div');
      prog.className = 'cot-progress';
      if (showBack) {
        var back = document.createElement('button');
        back.className = 'cot-back';
        back.setAttribute('aria-label', 'Volver al paso anterior');
        back.textContent = '← Volver';
        back.addEventListener('click', function () { state.step--; save(); render(); });
        prog.appendChild(back);
      }
      var bar = document.createElement('div');
      bar.className = 'cot-progress-bar';
      var fill = document.createElement('div');
      fill.className = 'cot-progress-fill';
      fill.style.width = (cur / total * 100) + '%';
      bar.appendChild(fill);
      prog.appendChild(bar);
      var label = document.createElement('span');
      label.className = 'cot-progress-label';
      label.textContent = 'Paso ' + cur + ' de ' + total;
      prog.appendChild(label);
      return prog;
    }

    function renderStep() {
      var s   = STEPS[state.step];
      var cur = state.step + 1;
      widgetEl.appendChild(renderProgress(cur, STEPS.length + 1, state.step > 0));

      var q = document.createElement('div');
      q.className = 'cot-question';
      q.innerHTML = '<h3 class="cot-q-title">' + s.question + '</h3><p class="cot-q-subtitle">' + s.subtitle + '</p>';
      widgetEl.appendChild(q);

      var isSm = s.options.length <= 3;
      var grid = document.createElement('div');
      grid.className = 'cot-options ' + (isSm ? 'cot-options--sm' : 'cot-options--lg');

      s.options.forEach(function (opt) {
        var btn = document.createElement('button');
        btn.className = 'cot-option' + (state.answers[s.id] === opt.value ? ' cot-option--selected' : '');
        btn.setAttribute('aria-pressed', state.answers[s.id] === opt.value ? 'true' : 'false');
        btn.innerHTML = '<span class="cot-option-icon" aria-hidden="true">' + opt.icon + '</span>' +
                        '<span class="cot-option-label">' + opt.label + '</span>' +
                        (opt.sublabel ? '<span class="cot-option-sub">' + opt.sublabel + '</span>' : '');
        btn.addEventListener('click', function () {
          state.answers[s.id] = opt.value;
          state.step++;
          save();
          render();
        });
        grid.appendChild(btn);
      });
      widgetEl.appendChild(grid);
    }

    function renderContact() {
      widgetEl.appendChild(renderProgress(STEPS.length + 1, STEPS.length + 1, true));

      var q = document.createElement('div');
      q.className = 'cot-question';
      q.innerHTML = '<h3 class="cot-q-title">¿Cómo te contactamos?</h3>' +
                    '<p class="cot-q-subtitle">Para coordinar la visita técnica gratuita</p>';
      widgetEl.appendChild(q);

      var form = document.createElement('div');
      form.className = 'cot-contact-form';
      form.innerHTML =
        '<div class="cot-field">' +
          '<label class="cot-label" for="cot-nombre-' + domId + '">Tu nombre</label>' +
          '<input class="cot-input" id="cot-nombre-' + domId + '" type="text" placeholder="Ej: María González" autocomplete="name" value="' + (state.contact.nombre || '') + '" />' +
        '</div>' +
        '<div class="cot-field">' +
          '<label class="cot-label" for="cot-correo-' + domId + '">Correo electrónico</label>' +
          '<input class="cot-input" id="cot-correo-' + domId + '" type="email" placeholder="Ej: maria@correo.com" autocomplete="email" value="' + (state.contact.correo || '') + '" />' +
        '</div>' +
        '<div class="cot-field">' +
          '<label class="cot-label" for="cot-ciudad-' + domId + '">Ciudad y región</label>' +
          '<input class="cot-input" id="cot-ciudad-' + domId + '" type="text" placeholder="Ej: Quillota, Valparaíso" autocomplete="address-level2" value="' + (state.contact.ciudad || '') + '" />' +
        '</div>' +
        '<p class="cot-privacy">🔒 Tus datos son confidenciales. Solo A&C Soluciones los verá.</p>' +
        '<p class="cot-error" id="cot-err-' + domId + '" hidden></p>' +
        '<button class="btn btn-secondary cot-submit-btn" id="cot-submit-' + domId + '">' +
          'Ver mi cotización →' +
        '</button>';

      widgetEl.appendChild(form);

      var nombreEl = document.getElementById('cot-nombre-' + domId);
      var correoEl = document.getElementById('cot-correo-' + domId);
      var ciudadEl = document.getElementById('cot-ciudad-' + domId);
      var errEl    = document.getElementById('cot-err-' + domId);
      var submitEl = document.getElementById('cot-submit-' + domId);

      var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

      submitEl.addEventListener('click', function () {
        var nombre = nombreEl.value.trim();
        var correo = correoEl.value.trim();
        var ciudad = ciudadEl.value.trim();
        if (nombre.length < 2)          { errEl.textContent = 'Por favor ingresa tu nombre completo.'; errEl.removeAttribute('hidden'); nombreEl.focus(); return; }
        if (!EMAIL_RE.test(correo))     { errEl.textContent = 'Por favor ingresa un correo válido (ej: maria@correo.com).'; errEl.removeAttribute('hidden'); correoEl.focus(); return; }
        if (ciudad.length < 2)          { errEl.textContent = 'Por favor ingresa tu ciudad.'; errEl.removeAttribute('hidden'); ciudadEl.focus(); return; }
        errEl.setAttribute('hidden', '');
        submitEl.disabled = true;
        submitEl.textContent = 'Generando cotización...';
        state.contact = { nombre: nombre, correo: correo, ciudad: ciudad };

        function continuar(ref) {
          state.refCode = ref;
          postWebhook(state.answers, state.contact, cta, state.refCode);
          state.step++;
          save();
          render();
        }
        function refFallback() {
          return 'AYC-' + new Date().toISOString().slice(2,7).replace('-','') + '-' + (Math.floor(Math.random() * 9000) + 1000);
        }

        fetch(WEBHOOK_URL)
          .then(function(r) { return r.json(); })
          .then(function(d) { continuar(d.ref || refFallback()); })
          .catch(function()  { continuar(refFallback()); });
      });

      [nombreEl, correoEl, ciudadEl].forEach(function (el) {
        el.addEventListener('keydown', function (e) { if (e.key === 'Enter') submitEl.click(); });
      });
    }

    function renderResult() {
      var ans    = state.answers;
      var nombre = state.contact.nombre ? state.contact.nombre.split(' ')[0] : '';
      var wa = buildWASanitizacion(ans, state.contact, state.refCode);
      var div = document.createElement('div');
      div.className = 'cot-result';
      div.innerHTML =
        '<div class="cot-result-header">' +
          '<span class="cot-result-icon" aria-hidden="true">✅</span>' +
          '<h3 class="cot-result-title">' + (nombre ? nombre + ', r' : 'R') + 'ecomendamos una visita técnica</h3>' +
          '<p class="cot-result-sub">La <strong>sanitización</strong> se cotiza según el tamaño del espacio, te damos un presupuesto exacto en la visita.</p>' +
        '</div>' +
        '<div class="cot-result-cards">' +
          '<div class="cot-result-card cot-result-card--price">' +
            '<span class="cot-card-label">Visita técnica</span>' +
            '<span class="cot-card-value">Sin costo</span>' +
            '<span class="cot-card-note">Evaluación presencial gratuita</span>' +
          '</div>' +
          '<div class="cot-result-card">' +
            '<span class="cot-card-label">Incluye</span>' +
            '<span class="cot-card-value cot-card-value--sm">Evaluación del espacio, protocolo recomendado e informe con certificado SEREMI</span>' +
          '</div>' +
        '</div>' +
        '<div class="cot-result-disclaimer">' +
          '<strong>¿Por qué no hay precio online?</strong> La sanitización se cotiza por metros cuadrados y frecuencia (única vez o programa mensual). Sin ver tu espacio no podemos darte un valor justo.' +
        '</div>' +
        '<p class="cot-result-human">Serás atendido por el representante técnico de A&C Soluciones.</p>' +
        '<div class="cot-result-ctas">' +
          '<a href="' + wa + '" target="_blank" rel="noopener noreferrer" class="btn btn-secondary cot-wa-btn">' +
            WA_SVG + ' Agendar visita técnica gratuita' +
          '</a>' +
          '<button class="cot-restart">Empezar de nuevo</button>' +
        '</div>';

      div.querySelector('.cot-restart').addEventListener('click', function () {
        clear();
        state = { step: 0, answers: {}, contact: { nombre: '', correo: '', ciudad: '' } };
        render();
      });
      widgetEl.appendChild(div);
    }

    var saved = load();
    if (saved && saved.step > 0 && Object.keys(saved.answers || {}).length > 0) {
      var banner = document.createElement('div');
      banner.className = 'cot-resume-banner';
      banner.innerHTML =
        '<p>Tienes una cotización incompleta guardada. ¿Continúas?</p>' +
        '<div class="cot-resume-btns">' +
          '<button class="btn btn-secondary cot-resume-yes">Continuar</button>' +
          '<button class="cot-resume-no">Empezar de nuevo</button>' +
        '</div>';
      banner.querySelector('.cot-resume-yes').addEventListener('click', function () {
        state = { step: saved.step, answers: saved.answers, contact: saved.contact || { nombre: '', correo: '', ciudad: '' } };
        banner.remove();
        render();
      });
      banner.querySelector('.cot-resume-no').addEventListener('click', function () {
        clear();
        banner.remove();
        render();
      });
      widgetEl.appendChild(banner);
    } else {
      render();
    }

    return {
      setCta: function (v) { if (v) cta = v; }
    };
  }

  function initModal() {
    var modal   = document.getElementById('cot-modal');
    if (!modal) return;

    var overlay = document.getElementById('cot-modal-overlay');
    var closeBtn = document.getElementById('cot-modal-close');
    var widget  = document.getElementById('cotizador-modal-widget');
    var controller = null;

    function openModal(cta) {
      modal.removeAttribute('hidden');
      document.body.classList.add('cot-modal-open');
      if (!controller && widget) {
        controller = createCotizador(widget);
      }
      if (controller) controller.setCta(cta);
      if (closeBtn) closeBtn.focus();
    }

    function closeModal() {
      modal.setAttribute('hidden', '');
      document.body.classList.remove('cot-modal-open');
    }

    document.querySelectorAll('[data-open-cotizador]').forEach(function (el) {
      el.addEventListener('click', function () {
        openModal(el.getAttribute('data-cta'));
      });
    });

    if (closeBtn)  closeBtn.addEventListener('click', closeModal);
    if (overlay)   overlay.addEventListener('click', closeModal);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hasAttribute('hidden')) closeModal();
    });
  }

  function init() {
    var section = document.getElementById('cotizador-widget');
    if (section) createCotizador(section);
    initModal();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

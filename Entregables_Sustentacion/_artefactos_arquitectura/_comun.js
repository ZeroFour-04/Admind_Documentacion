(function(){
  // Modo repaso: difumina las explicaciones y respuestas marcadas con .oculta; un clic revela cada una.
  var boton = document.getElementById('boton-repaso');
  function aplicar(activo){
    document.body.classList.toggle('modo-repaso', activo);
    boton.setAttribute('aria-pressed', activo ? 'true' : 'false');
    boton.textContent = activo ? 'Modo repaso: activo' : 'Modo repaso';
    if (!activo) document.querySelectorAll('.oculta.visto').forEach(function(el){ el.classList.remove('visto'); });
  }
  if (boton){
    boton.addEventListener('click', function(){ aplicar(!document.body.classList.contains('modo-repaso')); });
    document.addEventListener('click', function(e){
      var el = e.target.closest('.oculta');
      if (el && document.body.classList.contains('modo-repaso')) el.classList.add('visto');
    });
  }

  // Índice: marca la sección visible.
  var enlaces = Array.prototype.slice.call(document.querySelectorAll('.indice a.ir'));
  var secciones = enlaces.map(function(a){ return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if ('IntersectionObserver' in window && secciones.length){
    var obs = new IntersectionObserver(function(entradas){
      entradas.forEach(function(en){
        if (en.isIntersecting){
          enlaces.forEach(function(a){ a.classList.toggle('activo', a.getAttribute('href') === '#' + en.target.id); });
        }
      });
    }, {rootMargin:'-20% 0px -70% 0px'});
    secciones.forEach(function(s){ obs.observe(s); });
  }

  // Buscador de apps.
  var filtro = document.getElementById('filtro-apps');
  if (filtro){
    var tarjetas = Array.prototype.slice.call(document.querySelectorAll('.rejilla-apps .app'));
    var vacio = document.getElementById('apps-vacio');
    var normal = function(t){ return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
    filtro.addEventListener('input', function(){
      var q = normal(filtro.value.trim()), visibles = 0;
      tarjetas.forEach(function(t){
        var ok = !q || normal(t.textContent).indexOf(q) !== -1;
        t.hidden = !ok; if (ok) visibles++;
      });
      if (vacio) vacio.hidden = visibles !== 0;
    });
  }
})();

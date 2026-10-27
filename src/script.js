(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function cardHTML(rank, suit){
    return '<div class="face"><div class="corner"><span class="rank">'+rank+'</span><span class="pip">'+suit+'</span></div><span class="big">'+suit+'</span><div class="corner bottom"><span class="rank">'+rank+'</span><span class="pip">'+suit+'</span></div></div><div class="back"></div>';
  }
  document.querySelectorAll('.card[data-rank]').forEach(function(c){
    c.innerHTML = cardHTML(c.dataset.rank, c.dataset.suit);
    if(c.dataset.color==='red') c.classList.add('red');
  });
  var hero = document.getElementById('hero');
  function start(){
    if(!hero) return;
    if(hero.classList.contains('ready')) return;
    hero.classList.add('ready');
    var t = reduce ? 0 : 1300;
    setTimeout(function(){ document.querySelectorAll('#hole .card').forEach(function(c){ c.classList.remove('down'); }); }, t);
  }
  if(hero){ if(document.fonts && document.fonts.ready){ document.fonts.ready.then(start); setTimeout(start, 1500); } else { start(); } }

  var slots = Array.prototype.slice.call(document.querySelectorAll('#board .slot'));
  // every slot holds a face-down card from the start; sections flip them face-up as the reader scrolls
  slots.forEach(function(s){
    if(s.firstChild) return;
    var c = document.createElement('div');
    c.className = 'card down' + (s.dataset.color==='red' ? ' red' : '');
    c.innerHTML = cardHTML(s.dataset.rank, s.dataset.suit);
    s.appendChild(c);
  });
  var dealt = 0;
  function dealTo(n){
    if(n <= dealt) return;
    for(var i = dealt; i < n; i++){
      (function(i){
        var c = slots[i] && slots[i].firstChild; if(!c) return;
        var delay = reduce ? 0 : 80 + (i - dealt) * 140;
        setTimeout(function(){ c.classList.remove('down'); }, delay);
      })(i);
    }
    dealt = n;
  }
  var boardEl = document.getElementById('board');
  if(boardEl && boardEl.dataset.dealt){ dealTo(parseInt(boardEl.dataset.dealt, 10)); }
  else if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ dealTo(parseInt(e.target.dataset.deal, 10)); } });
    }, { rootMargin: '0px 0px -40% 0px' });
    document.querySelectorAll('[data-deal]').forEach(function(s){ io.observe(s); });
  } else { dealTo(5); }

  if(hero && !reduce && window.matchMedia('(hover:hover) and (pointer:fine)').matches){
    var hole = document.getElementById('hole');
    hero.addEventListener('mousemove', function(ev){
      var r = hero.getBoundingClientRect();
      var x = (ev.clientX - r.left) / r.width - .5, y = (ev.clientY - r.top) / r.height - .5;
      hole.style.transform = 'rotateY(' + (x * 10) + 'deg) rotateX(' + (-y * 8) + 'deg)';
    });
    hero.addEventListener('mouseleave', function(){ hole.style.transform = ''; });
  }

  // wins marquee: duplicate the set once so the loop is seamless
  var track = document.getElementById('track');
  if(track && !reduce){ track.innerHTML += track.innerHTML; }

  document.querySelectorAll('a[data-pending]').forEach(function(a){
    a.addEventListener('click', function(e){ e.preventDefault(); a.setAttribute('aria-label', 'Link coming soon'); });
  });
})();

// contact form: static site, so it hands off to email when an address is configured, else to Instagram
(function(){
  var f = document.getElementById('contact-form'); if(!f) return;
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var to = f.getAttribute('data-contact-email') || '';
    var name = (f.name && f.name.value || '').trim(), email = (f.email && f.email.value || '').trim(), msg = (f.message && f.message.value || '').trim();
    if(!name || !email || !msg){ f.reportValidity && f.reportValidity(); return; }
    var body = 'Name: ' + name + '\nEmail: ' + email + '\nTopic: ' + (f.topic && f.topic.value) + '\nPlays: ' + (f.stakes && f.stakes.value) + '\n\n' + msg;
    if(to){ window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent('Weingoat site: ' + (f.topic && f.topic.value)) + '&body=' + encodeURIComponent(body); f.classList.add('is-sent'); }
    else { var s = f.querySelector('.sent'); s.innerHTML = 'The form isn\'t connected yet. For now, send this as a DM on <a href="https://www.instagram.com/adamweingard/" target="_blank" rel="noopener">Instagram</a>.'; f.classList.add('is-sent'); }
  });
})();

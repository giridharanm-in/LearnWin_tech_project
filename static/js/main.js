/* ================================================================
   Besant Technologies – main.js
   ================================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Auto-dismiss flash messages after 5s ──
  document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(110%)';
      el.style.transition = 'all 0.4s ease';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });


  // ── Course Category Filter (courses page) ──
  const filterBtns = document.querySelectorAll('.filter-btn');
  const catSections = document.querySelectorAll('.cat-section');

  if (filterBtns.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.cat;

        catSections.forEach(sec => {
          if (cat === 'all' || sec.dataset.category === cat) {
            sec.style.display = 'block';
          } else {
            sec.style.display = 'none';
          }
        });

        // Also filter individual cards if used in other grids
        document.querySelectorAll('.course-card[data-cat]').forEach(card => {
          if (cat === 'all' || card.dataset.cat === cat) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }


  // ── Phone validation ──
  const phoneInput = document.getElementById('phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', () => {
      phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
    });
  }


  // ── Pre-select course from URL param ──
  const urlParams = new URLSearchParams(window.location.search);
  const courseParam = urlParams.get('course');
  if (courseParam) {
    const sel = document.getElementById('course_id');
    if (sel) sel.value = courseParam;
  }


  // ── Set today's date as default for attendance ──
  const attDate = document.getElementById('att_date');
  if (attDate && !attDate.value) {
    const today = new Date().toISOString().split('T')[0];
    attDate.value = today;
  }


  // ── Smooth active nav highlight by current path ──
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });


  // ── Animate KPI numbers ──
  function animateCount(el) {
    const target = parseInt(el.innerText.replace(/\D/g, ''), 10);
    if (isNaN(target) || target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 40);
    const timer = setInterval(() => {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.innerText = current;
    }, 30);
  }

  document.querySelectorAll('.kpi-card strong, .att-stat-card strong').forEach(el => {
    const txt = el.innerText;
    if (/^\d+$/.test(txt.trim())) {
      const obs = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) { animateCount(el); obs.unobserve(el); } });
      }, { threshold: 0.5 });
      obs.observe(el);
    }
  });


  // ── Animate progress bars ──
  document.querySelectorAll('.progress-bar-fill').forEach(bar => {
    const targetWidth = bar.style.width;
    bar.style.width = '0%';
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          setTimeout(() => { bar.style.width = targetWidth; }, 200);
          obs.unobserve(bar);
        }
      });
    }, { threshold: 0.5 });
    obs.observe(bar);
  });


  // ── Client-side form validation ──
  document.querySelectorAll('.main-form').forEach(form => {
    form.addEventListener('submit', e => {
      let valid = true;
      form.querySelectorAll('[required]').forEach(field => {
        field.style.borderColor = '';
        if (!field.value.trim()) {
          field.style.borderColor = '#ef4444';
          field.style.boxShadow = '0 0 0 3px rgba(239,68,68,.1)';
          valid = false;
        } else {
          field.style.borderColor = '#10b981';
          field.style.boxShadow = '0 0 0 3px rgba(16,185,129,.1)';
        }
      });
      if (!valid) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        const firstErr = form.querySelector('[required][style*="ef4444"]');
        if (firstErr) firstErr.focus();
      }
    });
  });


  // ── Scroll-in animation for cards ──
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.feature-card, .course-card, .testi-card, .value-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });

});

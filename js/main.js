document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav drawer
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        const firstLink = nav.querySelector('a');
        if (firstLink) firstLink.focus();
      }
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Dark mode toggle (theme is already applied pre-paint by the inline
  // head script in PAGE() — this just wires the button and persists choice)
  const themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    const root = document.documentElement;
    const syncPressed = () => {
      const isDark = root.getAttribute('data-theme') === 'dark';
      themeBtn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
      themeBtn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    };
    syncPressed();
    themeBtn.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('toolpeg-theme', next); } catch (e) {}
      syncPressed();
    });
  }

  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
});


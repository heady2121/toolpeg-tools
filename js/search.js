document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-input');
  const searchBox = document.getElementById('tool-search');
  if (!input) return;

  const sections = Array.from(document.querySelectorAll('[data-section]'));
  const cards = Array.from(document.querySelectorAll('.tool-grid .peg-card'));
  const noResults = searchBox.querySelector('.no-results');

  function applyFilter() {
    const q = input.value.trim().toLowerCase();
    searchBox.classList.toggle('has-query', q.length > 0);

    let anyVisible = false;
    cards.forEach((card) => {
      const match = !q || (card.dataset.name || '').includes(q);
      card.classList.toggle('search-hidden', !match);
      if (match) anyVisible = true;
    });

    sections.forEach((section) => {
      const visibleCards = section.querySelectorAll('.peg-card:not(.search-hidden)');
      section.classList.toggle('search-hidden', q.length > 0 && visibleCards.length === 0);
    });

    if (noResults) noResults.classList.toggle('show', q.length > 0 && !anyVisible);
  }

  input.addEventListener('input', applyFilter);
});

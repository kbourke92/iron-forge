// Auto-dismiss messages after 4s
document.addEventListener('DOMContentLoaded', () => {
  const msgs = document.querySelectorAll('.message');
  msgs.forEach(m => {
    setTimeout(() => {
      m.style.transition = 'opacity 0.5s';
      m.style.opacity = '0';
      setTimeout(() => m.remove(), 500);
    }, 4000);
  });
});

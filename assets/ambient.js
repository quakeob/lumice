(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const canvas = document.getElementById('snowCanvas');

  if (!canvas || reducedMotion.matches) return;

  const context = canvas.getContext('2d');
  if (!context) return;

  const particles = [];
  const count = 100;
  const cursorRadius = 120;
  const cursorForce = 1.8;
  const mouse = { x: -1000, y: -1000, active: false };

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  resize();
  window.addEventListener('resize', resize, { passive: true });
  document.addEventListener?.('mousemove', (event) => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
    mouse.active = true;
  });
  document.addEventListener?.('mouseleave', () => { mouse.active = false; });

  for (let index = 0; index < count; index += 1) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 2.5 + 0.5,
      baseX: (Math.random() - 0.5) * 0.3,
      baseY: Math.random() * 0.6 + 0.2,
      velocityX: 0,
      velocityY: 0,
      opacity: Math.random() * 0.5 + 0.15,
      phase: Math.random() * Math.PI * 2,
    });
  }

  function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((particle) => {
      particle.phase += 0.012;
      const opacity = particle.opacity * (0.65 + 0.35 * Math.sin(particle.phase));

      if (mouse.active) {
        const deltaX = particle.x - mouse.x;
        const deltaY = particle.y - mouse.y;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        if (distance < cursorRadius && distance > 0) {
          const force = (1 - distance / cursorRadius) * cursorForce;
          const angle = Math.atan2(deltaY, deltaX);
          particle.velocityX += Math.cos(angle) * force;
          particle.velocityY += Math.sin(angle) * force;
        }
      }

      particle.velocityX = particle.velocityX * 0.96 + particle.baseX * 0.04;
      particle.velocityY = particle.velocityY * 0.96 + particle.baseY * 0.04;
      particle.velocityX += Math.sin(particle.phase * 0.5) * 0.02;

      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fillStyle = `rgba(210, 225, 245, ${opacity})`;
      context.fill();

      particle.x += particle.velocityX;
      particle.y += particle.velocityY;

      if (particle.y > canvas.height + 10) {
        particle.y = -10;
        particle.x = Math.random() * canvas.width;
      }
      if (particle.x > canvas.width + 10) particle.x = -10;
      if (particle.x < -10) particle.x = canvas.width + 10;
    });

    window.requestAnimationFrame(draw);
  }

  draw();
})();

(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const heroBackground = document.querySelector('[data-parallax]');

  if (heroBackground && !reducedMotion) {
    window.addEventListener('scroll', () => {
      if (window.scrollY < window.innerHeight * 1.2) {
        heroBackground.style.transform = `translateY(${window.scrollY * 0.3}px)`;
      }
    }, { passive: true });
  }

  const reveals = document.querySelectorAll('.reveal');
  if (reducedMotion || !('IntersectionObserver' in window)) {
    reveals.forEach((element) => element.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('visible');
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach((element) => observer.observe(element));
})();

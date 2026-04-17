// enhancements.js — Interatividade e animações modernas

document.addEventListener('DOMContentLoaded', function() {
  
  // ═══════════════════════════════════════════════════════════════
  // SCROLL REVEAL ANIMATIONS
  // ═══════════════════════════════════════════════════════════════
  
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, observerOptions);
  
  // Observar todos os elementos com data-scroll-reveal
  document.querySelectorAll('[data-scroll-reveal]').forEach(element => {
    observer.observe(element);
  });
  
  // ═══════════════════════════════════════════════════════════════
  // PRODUCT CARDS STAGGER ANIMATION
  // ═══════════════════════════════════════════════════════════════
  
  const productCards = document.querySelectorAll('.pcard');
  productCards.forEach((card, index) => {
    card.style.setProperty('--index', index);
    
    // Observar cada card para aparecer
    const cardObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('pcard--visible');
          }, index * 50);
          cardObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    cardObserver.observe(card);
  });
  
  // ═══════════════════════════════════════════════════════════════
  // NAVBAR SCROLL EFFECT
  // ═══════════════════════════════════════════════════════════════
  
  const navbar = document.getElementById('navbar');
  if (navbar) {
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      if (scrollTop > 100) {
        navbar.classList.add('navbar--scrolled');
      } else {
        navbar.classList.remove('navbar--scrolled');
      }
      
      lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, false);
  }
  
  // ═══════════════════════════════════════════════════════════════
  // SMOOTH SCROLL FOR ANCHOR LINKS
  // ═══════════════════════════════════════════════════════════════
  
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href !== '#' && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href).scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // ═══════════════════════════════════════════════════════════════
  // BUTTON RIPPLE EFFECT
  // ═══════════════════════════════════════════════════════════════
  
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
  
  // ═══════════════════════════════════════════════════════════════
  // FORM INPUT FOCUS EFFECTS
  // ═══════════════════════════════════════════════════════════════
  
  document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('form-group--focused');
    });
    
    input.addEventListener('blur', function() {
      if (!this.value) {
        this.parentElement.classList.remove('form-group--focused');
      }
    });
  });
  
  // ═══════════════════════════════════════════════════════════════
  // PARALLAX EFFECT
  // ═══════════════════════════════════════════════════════════════
  
  const parallaxElements = document.querySelectorAll('[data-parallax]');
  if (parallaxElements.length > 0) {
    window.addEventListener('scroll', function() {
      parallaxElements.forEach(element => {
        const scrollPosition = window.pageYOffset;
        const elementOffset = element.offsetTop;
        const distance = scrollPosition - elementOffset;
        element.style.backgroundPosition = `center ${distance * 0.5}px`;
      });
    });
  }
  
  // ═══════════════════════════════════════════════════════════════
  // COUNTER ANIMATION
  // ═══════════════════════════════════════════════════════════════
  
  function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function update() {
      start += increment;
      if (start < target) {
        element.textContent = Math.floor(start).toLocaleString();
        requestAnimationFrame(update);
      } else {
        element.textContent = target.toLocaleString();
      }
    }
    
    update();
  }
  
  const counters = document.querySelectorAll('[data-counter]');
  const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        const value = parseInt(entry.target.dataset.counter);
        animateCounter(entry.target, value);
        entry.target.dataset.counted = 'true';
        counterObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  counters.forEach(counter => counterObserver.observe(counter));
  
  // ═══════════════════════════════════════════════════════════════
  // MOBILE MENU TOGGLE
  // ═══════════════════════════════════════════════════════════════
  
  const hamburger = document.querySelector('.navbar__hamburger');
  const navLinks = document.getElementById('navLinks');
  
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function() {
      this.classList.toggle('navbar__hamburger--open');
      navLinks.classList.toggle('navbar__links--open');
    });
    
    // Fechar menu ao clicar em um link
    navLinks.querySelectorAll('.navbar__link').forEach(link => {
      link.addEventListener('click', function() {
        hamburger.classList.remove('navbar__hamburger--open');
        navLinks.classList.remove('navbar__links--open');
      });
    });
  }
  
  // ═══════════════════════════════════════════════════════════════
  // LAZY LOAD IMAGES
  // ═══════════════════════════════════════════════════════════════
  
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.classList.add('lazy-loaded');
          }
          observer.unobserve(img);
        }
      });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }
});

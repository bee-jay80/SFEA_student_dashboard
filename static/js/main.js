/**
 * Sound Foundation Edtech Academy - Main JavaScript
 * Contains utility functions and event listeners for the dashboard
 */

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Add scroll effect to navbar
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
  if (navbar) {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 50) {
      navbar.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.3)';
    } else {
      navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.15)';
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }
});

// Add animation to cards when they come into view
function observeElements() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  };

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const cards = document.querySelectorAll('.course-card, .feature-item, .stat-item');
  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
  });
}

// Initialize observers when DOM is ready
document.addEventListener('DOMContentLoaded', observeElements);

// Toggle mobile menu
function toggleMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navbarMenu = document.getElementById('navbarMenu');
  
  if (hamburger && navbarMenu) {
    hamburger.addEventListener('click', function() {
      navbarMenu.classList.toggle('active');
      this.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!event.target.closest('.navbar-container')) {
        navbarMenu.classList.remove('active');
        hamburger.classList.remove('active');
      }
    });
  }
}

// Initialize mobile menu
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', toggleMobileMenu);
} else {
  toggleMobileMenu();
}

// Utility function to show notifications
function showNotification(message, type = 'info', duration = 3000) {
  const notification = document.createElement('div');
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 80px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 5px;
    color: white;
    font-weight: 600;
    z-index: 2000;
    animation: slideIn 0.3s ease;
  `;

  // Set background color based on type
  const colors = {
    success: '#4caf50',
    error: '#f44336',
    warning: '#ff9800',
    info: '#2196f3'
  };
  notification.style.backgroundColor = colors[type] || colors.info;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, duration);
}

// Add CSS animations to document
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);

// Log that the script is loaded
console.log('Sound Foundation Edtech Academy Dashboard - Ready!');

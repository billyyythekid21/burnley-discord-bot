window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

/* text scrolling effect */
document.addEventListener("DOMContentLoaded", function() {
  const element = document.querySelector('.indexdesc');
  const text = "Your fun and friendly Discord bot companion!";
  let index = 0;
  let isAdding = true;

  function typeEffect() {
      if (isAdding) {
          if (index < text.length) {
              element.textContent += text.charAt(index);
              index++;
          } else {
              isAdding = false;
              setTimeout(typeEffect, 2000); // Wait 2 seconds before erasing
              return;
          }
      } else {
          if (index > 0) {
              element.textContent = text.substring(0, index - 1);
              index--;
          } else {
              isAdding = true;
          }
      }
      setTimeout(typeEffect, isAdding ? 100 : 50); // Adjust typing/erasing speed
  }

  typeEffect();
});

document.addEventListener("DOMContentLoaded", function() {
    const element = document.querySelector('.commandstitle');
    const text = "The guide that puts everything about commands together.";
    let index = 0;
    let isAdding = true;
  
    function typeEffect() {
        if (isAdding) {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
            } else {
                isAdding = false;
                setTimeout(typeEffect, 2000); // Wait 2 seconds before erasing
                return;
            }
        } else {
            if (index > 0) {
                element.textContent = text.substring(0, index - 1);
                index--;
            } else {
                isAdding = true;
            }
        }
        setTimeout(typeEffect, isAdding ? 100 : 50); // Adjust typing/erasing speed
    }
  
    typeEffect();
  });
document.addEventListener("DOMContentLoaded", function () {
    const profileBtn = document.getElementById("profileBtn");
    const sidebar = document.getElementById("sidebar");
    const overlay = document.getElementById("overlay");

    // === Открытие/закрытие боковой панели ===
    if (profileBtn && sidebar && overlay) {
        profileBtn.addEventListener("click", function () {
            sidebar.classList.toggle("open");
            overlay.classList.toggle("show");
        });

        overlay.addEventListener("click", function () {
            sidebar.classList.remove("open");
            overlay.classList.remove("show");
        });
    }

    // === Логика модального окна ===
    const avatarDiv = document.getElementById("userInitial");
    const userLetter = avatarDiv ? avatarDiv.textContent.trim() : "";

    if (avatarDiv) {
        avatarDiv.style.cursor = 'pointer';
        avatarDiv.addEventListener("click", function () {
            document.getElementById("avatarModal").style.display = "block";
        });
    }

    const modal = document.getElementById("avatarModal");
    const closeBtn = document.getElementById("closeAvatarModal");

    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    // === Сохранение новой буквы ===
    const initialForm = document.getElementById("initialForm");
    const initialInput = document.getElementById("initialInput");

    if (initialForm && initialInput) {
        initialForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const newLetter = initialInput.value.trim();

            if (newLetter !== "") {
                if (avatarDiv) {
                    avatarDiv.style.backgroundImage = 'none';
                    avatarDiv.style.color = '#fff';
                    avatarDiv.textContent = newLetter.charAt(0).toUpperCase();
                }
                modal.style.display = "none";
            } else {
                alert('Введите одну букву');
            }
        });
    }

    // === Превью локальной картинки ===
    const avatarInput = document.getElementById("avatarInput");

    if (avatarInput) {
        avatarInput.addEventListener("change", function (e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    if (avatarDiv) {
                        avatarDiv.style.backgroundImage = `url('${event.target.result}')`;
                        avatarDiv.style.color = 'transparent';
                        avatarDiv.textContent = '';
                    }
                    modal.style.display = "none";
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // === Сброс до первой буквы ===
    const resetBtn = document.getElementById("resetAvatarBtn");
    if (resetBtn && avatarDiv) {
        resetBtn.addEventListener("click", function () {
            avatarDiv.style.backgroundImage = 'none';
            avatarDiv.style.color = '#fff';
            avatarDiv.textContent = userLetter;
            modal.style.display = "none";
        });
    }

    // === AJAX: Загрузка аватара ===
    const avatarForm = document.getElementById("avatarForm");
    if (avatarForm) {
        avatarForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const avatarElement = document.querySelector('.user-avatar img');
                    if (avatarElement) {
                        avatarElement.src = data.avatar_url;
                    } else {
                        const container = document.querySelector('.user-initial');
                        if (container) {
                            container.innerHTML = `<img src="${data.avatar_url}" alt="Аватар" style="width: 40px; height: 40px;">`;
                        }
                    }
                    alert('Аватар успешно загружен!');
                    location.reload();
                } else {
                    alert('Ошибка при загрузке аватара.');
                    console.error(data.error);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при загрузке аватара.');
            });
        });
    }
});

// === Функция получения CSRF-токена ===
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
  const track = document.querySelector('.carousel-track');
  const prevBtn = document.querySelector('.carousel-btn.prev-btn');
  const nextBtn = document.querySelector('.carousel-btn.next-btn');
  const items = Array.from(document.querySelectorAll('.carousel-item'));
  
  const visibleItems = 3;
  const totalItems = items.length;
  let currentIndex = 0;
  let isAnimating = false;
  const animationDuration = 600;

  // Стили для анимации
  const style = document.createElement('style');
  style.textContent = `
    .carousel-track {
      display: flex;
      gap: 16px;
      position: relative;
      height: 450px;
    }
    .carousel-item {
      flex: 0 0 calc((100% - 32px) / 3);
      transition: all ${animationDuration}ms cubic-bezier(0.16, 0.84, 0.44, 1);
      will-change: transform, opacity;
    }
    /* Анимации для правой кнопки (сдвиг влево) */
    .item-exiting-left {
      animation: exitLeft ${animationDuration}ms forwards;
    }
    .item-entering-right {
      animation: enterRight ${animationDuration}ms forwards;
    }
    /* Анимации для левой кнопки (сдвиг вправо) */
    .item-exiting-right {
      animation: exitRight ${animationDuration}ms forwards;
    }
    .item-entering-left {
      animation: enterLeft ${animationDuration}ms forwards;
    }
    @keyframes enterRight {
      0% { opacity: 0; transform: translateX(50px) scale(0.95); }
      100% { opacity: 1; transform: translateX(0) scale(1); }
    }
    @keyframes exitLeft {
      0% { opacity: 1; transform: translateX(0) scale(1); }
      100% { opacity: 0; transform: translateX(-50px) scale(0.95); }
    }
    @keyframes enterLeft {
      0% { opacity: 0; transform: translateX(-50px) scale(0.95); }
      100% { opacity: 1; transform: translateX(0) scale(1); }
    }
    @keyframes exitRight {
      0% { opacity: 1; transform: translateX(0) scale(1); }
      100% { opacity: 0; transform: translateX(50px) scale(0.95); }
    }
  `;
  document.head.appendChild(style);

  function initCarousel() {
    track.innerHTML = '';
    for (let i = 0; i < visibleItems; i++) {
      addItem((currentIndex + i) % totalItems, false);
    }
  }

  function addItem(index, animate, direction) {
    const item = items[index].cloneNode(true);
    if (animate) {
      const enteringClass = direction === 'next' ? 'item-entering-right' : 'item-entering-left';
      item.classList.add(enteringClass);
      item.style.opacity = '0';
    }
    track.appendChild(item);
    
    if (animate) {
      setTimeout(() => {
        item.style.opacity = '';
      }, 20);
    }
    return item;
  }

  function smoothReplace(direction) {
    if (isAnimating) return;
    isAnimating = true;
    
    const isNext = direction === 'next';
    const exitingIndex = isNext ? 0 : visibleItems - 1; // Для next - первый элемент, для prev - последний
    const enteringIndex = isNext 
      ? (currentIndex + visibleItems) % totalItems 
      : (currentIndex - 1 + totalItems) % totalItems;
    
    const currentItems = Array.from(track.children);
    const exitingClass = isNext ? 'item-exiting-left' : 'item-exiting-right';
    currentItems[exitingIndex].classList.add(exitingClass);
    
    // Добавляем новый элемент
    const newItem = addItem(enteringIndex, true, direction);
    if (!isNext) {
      track.insertBefore(newItem, track.firstChild);
    }
    
    setTimeout(() => {
      currentItems[exitingIndex].remove();
      const enteringClass = isNext ? 'item-entering-right' : 'item-entering-left';
      newItem.classList.remove(enteringClass);
      
      currentIndex = isNext 
        ? (currentIndex + 1) % totalItems 
        : (currentIndex - 1 + totalItems) % totalItems;
      
      isAnimating = false;
    }, animationDuration);
  }

  nextBtn.addEventListener('click', () => smoothReplace('next'));
  prevBtn.addEventListener('click', () => smoothReplace('prev'));

  initCarousel();
});

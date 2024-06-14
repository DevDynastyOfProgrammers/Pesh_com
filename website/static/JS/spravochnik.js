// Функция для перенаправления на карту при клике на кнопку
document.getElementById('map-button').addEventListener('click', () => {
    window.location.href = 'home.html'; // Перенаправление на страницу map.html
});

// Функция для преобразования строковой даты в объект Date
function parseDate(dateString) {
  const [day, month, year] = dateString.split(' ');
  const monthIndex = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'].indexOf(month);
  return new Date(year, monthIndex, day);
}


// Функция для установки времени на полночь
function setToMidnight(date) {
    date.setHours(0, 0, 0, 0); // Устанавливаем часы, минуты, секунды и миллисекунды на 0
    return date; // Возвращаем измененную дату
}

// Основной код, который выполняется после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    const dateFilter = document.getElementById('date-filter'); // Получаем элемент фильтра даты
    const categoryFilter = document.getElementById('category-filter'); // Получаем элемент фильтра категории
    const priceFilter = document.getElementById('price-filter'); // Получаем элемент фильтра цены
    const eventCards = document.querySelectorAll('.event-card'); // Получаем все карточки мероприятий

    // Поиск мероприятий по названию
    const searchInput = document.querySelector(".search-and-filters input[type='text']"); // Получаем элемент поля ввода для поиска
    searchInput.addEventListener("input", function() {
        const searchText = searchInput.value.toLowerCase().trim(); // Получаем введенный текст, приводя его к нижнему регистру и убирая пробелы
        eventCards.forEach(card => {
            const eventTitle = card.querySelector(".event-details h2").innerText.toLowerCase(); // Получаем заголовок мероприятия и приводим его к нижнему регистру
            card.style.display = eventTitle.startsWith(searchText) ? 'block' : 'none'; // Показываем или скрываем карточку мероприятия в зависимости от соответствия заголовка введенному тексту
        });
    });

// Функция для фильтрации мероприятий
function filterEvents() {
    const selectedDate = dateFilter.value;
    const selectedCategory = categoryFilter.value;
    const selectedPrice = priceFilter.value;

    eventCards.forEach(card => {
        const eventDateString = card.dataset.date;
        const eventDate = parseDate(eventDateString);
        const eventCategory = card.dataset.category;
        const eventPriceString = card.dataset.price;
        const eventPrice = parseInt(eventPriceString.replace('₽', ''));

        let matchesDate = false;
        let matchesCategory = false;
        let matchesPrice = true;

        const currentDate = new Date();
        const currentYear = currentDate.getFullYear();
        const currentMonth = currentDate.getMonth();
        const currentDay = currentDate.getDate();

        if (selectedDate === '') {
            matchesDate = true;
        } else if (selectedDate === 'today') {
            matchesDate = eventDate.getFullYear() === currentYear &&
                          eventDate.getMonth() === currentMonth &&
                          eventDate.getDate() === currentDay;
        } else if (selectedDate === 'tomorrow') {
            const tomorrow = new Date(currentYear, currentMonth, currentDay + 1);
            matchesDate = eventDate.getFullYear() === tomorrow.getFullYear() &&
                          eventDate.getMonth() === tomorrow.getMonth() &&
                          eventDate.getDate() === tomorrow.getDate();
        } else if (selectedDate === 'this-week') {
            const startOfWeek = new Date(currentYear, currentMonth, currentDay - currentDay % 7);
            const endOfWeek = new Date(startOfWeek.getFullYear(), startOfWeek.getMonth(), startOfWeek.getDate() + 6);
            matchesDate = eventDate >= startOfWeek && eventDate <= endOfWeek;
        } else if (selectedDate === 'month') {
            matchesDate = eventDate.getFullYear() === currentYear &&
                          eventDate.getMonth() === currentMonth;
        }

        if (selectedCategory === '' || eventCategory === selectedCategory) {
            matchesCategory = true; // Если фильтр категории не выбран или совпадает, то категория соответствует
        }

        // Проверяем фильтр по цене
        if (selectedPrice === "1000₽" && eventPrice > 1000) {
            matchesPrice = false;
        } else if (selectedPrice === "1500₽" && (eventPrice <= 1000 || eventPrice >= 2000)) {
            matchesPrice = false;
        } else if (selectedPrice === "2000₽" && eventPrice < 2000) {
            matchesPrice = false;
        }

        // Показываем или скрываем карточку мероприятия в зависимости от соответствия даты, категории и цены
        card.style.display = (matchesDate && matchesCategory && matchesPrice)? 'block' : 'none';
    });
}



    // События изменения для фильтров
    dateFilter.addEventListener('change', filterEvents);
    categoryFilter.addEventListener('change', filterEvents);
    priceFilter.addEventListener('change', filterEvents);

    // Изначальная фильтрация при загрузке страницы
    filterEvents();
});

// Добавляем обработчик клика на карточки мероприятий для перехода на страницу с информацией о мероприятии
document.addEventListener('DOMContentLoaded', function() {
    const eventCards = document.querySelectorAll('.event-card');

    eventCards.forEach(card => {
        card.addEventListener('click', function() {
        const eventId = card.getAttribute('data-id');
        window.location.href = `/xu?id=${eventId}`; // Передача event_id через URL
        });
    });
});

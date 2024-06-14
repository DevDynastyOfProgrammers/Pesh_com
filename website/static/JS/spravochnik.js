// Функция для перенаправления на карту при клике на кнопку
document.getElementById('map-button').addEventListener('click', () => {
    window.location.href = 'home.html'; // Перенаправление на страницу map.html
});

// Функция для преобразования строковой даты в объект Date
function parseDate(dateString) {
    const months = {
        'января': 0,
        'февраля': 1,
        'марта': 2,
        'апреля': 3,
        'мая': 4,
        'июня': 5,
        'июля': 6,
        'августа': 7,
        'сентября': 8,
        'октября': 9,
        'ноября': 10,
        'декабря': 11
    }; // Объект для сопоставления русских названий месяцев с их порядковыми номерами
    const [day, month, year] = dateString.split(' '); // Разбиваем строку на день, месяц и год
    return new Date(year, months[month], parseInt(day, 10)); // Возвращаем объект Date
}

// Функция для преобразования строковой даты в объект Date
function parseDate(dateString) {
    const [year, month, day] = dateString.split('-').map(part => parseInt(part, 10)); // Разбиваем строку на день, месяц и год
    return new Date(year, month - 1, day); // Возвращаем объект Date
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
        const selectedDate = dateFilter.value; // Получаем выбранное значение фильтра даты
        const selectedCategory = categoryFilter.value; // Получаем выбранное значение фильтра категории
        const selectedPrice = priceFilter.value; // Получаем выбранное значение фильтра цены
        const currentDate = setToMidnight(new Date()); // Текущая дата с временем, установленным на полночь
        const startOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1); // Начало текущего месяца
        const endOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0); // Конец текущего месяца

        eventCards.forEach(card => {
            const eventDate = setToMidnight(parseDate(card.dataset.date)); // Дата мероприятия с временем, установленным на полночь
            const eventCategory = card.dataset.category; // Категория мероприятия
            const eventPriceString = card.dataset.price; // Строка с ценой мероприятия
            const eventPrice = parseInt(eventPriceString.replace('₽', '')); // Парсинг строки цены в целое число

            let matchesDate = false; // Соответствие фильтру по дате
            let matchesCategory = false; // Соответствие фильтру по категории
            let matchesPrice = true; // Соответствие фильтру по цене

            const dateDiff = (eventDate - currentDate) / (1000 * 60 * 60 * 24); // Разница в днях между датой мероприятия и текущей датой

            // Проверяем фильтр по дате
            if (selectedDate === '') {
                matchesDate = true; // Если фильтр даты не выбран, то все даты соответствуют
            } else if (selectedDate === 'today') {
                matchesDate = dateDiff === 0; // Проверка на совпадение с текущей датой
            } else if (selectedDate === 'tomorrow') {
                matchesDate = dateDiff === 1; // Проверка на совпадение с завтрашней датой
            } else if (selectedDate === 'this-week') {
                matchesDate = dateDiff >= 0 && dateDiff < 7; // Проверка на совпадение с текущей неделей
            } else if (selectedDate === 'month') {
                matchesDate = eventDate >= startOfMonth && eventDate <= endOfMonth; // Проверка на совпадение с текущим месяцем
            }

            if (selectedCategory === '' || eventCategory === selectedCategory) {
                matchesCategory = true; // Если фильтр категории не выбран или совпадает, то категория соответствует
            }

            if (selectedCategory === '' || eventCategory === selectedCategory) {
                matchesCategory = true;
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
            card.style.display = (matchesDate && matchesCategory && matchesPrice) ? 'block' : 'none';
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

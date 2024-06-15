// Функция для перенаправления на карту при клике на кнопку
document.getElementById('map-button').addEventListener('click', () => {
    window.location.href = '/'; // Перенаправление на страницу map.html
});





// Функция для преобразования строковой даты в объект Date
function parseDate(dateString) {
    const months = {
        'Января': 0,
        'Февраля': 1,
        'Марта': 2,
        'Апреля': 3,
        'Мая': 4,
        'Июня': 5,
        'Июля': 6,
        'Августа': 7,
        'Сентября': 8,
        'Октября': 9,
        'Ноября': 10,
        'Декабря': 11
    }; // Объект для сопоставления русских названий месяцев с их порядковыми номерами
    const [day, month, year] = dateString.split(' '); // Разбиваем строку на день, месяц и год
    return new Date(year, months[month], parseInt(day, 10)); // Возвращаем объект Date
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
            card.style.display = eventTitle.includes(searchText) ? 'block' : 'none'; // Показываем или скрываем карточку мероприятия в зависимости от соответствия заголовка введенному тексту
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

            // Проверяем фильтр по цене
            if (selectedPrice === "1000₽" && eventPrice > 1000) {
                matchesPrice = false; // Если цена больше 1000₽ и фильтр установлен на 1000₽, то не соответствует
            } else if (selectedPrice === "1500₽" && (eventPrice <= 1000 || eventPrice >= 2000)) {
                matchesPrice = false; // Если цена не входит в диапазон от 1000₽ до 2000₽, то не соответствует
            } else if (selectedPrice === "2000₽" && eventPrice < 2000) {
                matchesPrice = false; // Если цена меньше 2000₽ и фильтр установлен на 2000₽, то не соответствует
            }

            // Показываем или скрываем карточку мероприятия в зависимости от соответствия дате, категории и цене
            card.style.display = (matchesDate && matchesCategory && matchesPrice) ? 'block' : 'none';
        });
    }

    // События изменения для фильтров
    dateFilter.addEventListener('change', filterEvents); // Обработчик изменения фильтра даты
    categoryFilter.addEventListener('change', filterEvents); // Обработчик изменения фильтра категории
    priceFilter.addEventListener('change', filterEvents); // Обработчик изменения фильтра цены

    // Изначальная фильтрация при загрузке страницы
    filterEvents();
});

// Добавляем обработчик клика на карточки мероприятий для перехода на страницу с информацией о мероприятии
document.addEventListener('DOMContentLoaded', function() {
    const eventCards = document.querySelectorAll('.event-card'); // Получаем все карточки мероприятий

    eventCards.forEach(card => {
        card.addEventListener('click', function() {
            const eventId = card.getAttribute('data-id'); // Получаем ID мероприятия из атрибута data-id
            window.location.href = `/xu?id=${eventId}`; // Переходим на страницу с информацией о мероприятии, передавая ID в качестве параметра URL
        });
    });
});



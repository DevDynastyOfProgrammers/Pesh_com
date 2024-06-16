// Функция для перенаправления на карту при клике на кнопку
// document.getElementById('map-button').addEventListener('click', () => {
//     window.location.href = '/'; // Перенаправление на страницу map.html
// });





// Функция для преобразования строковой даты в объект Date
function parseDate(dateString) {
    const [day, month, year] = dateString.split(' '); // Разбиваем строку даты на день, месяц и год
    const monthIndex = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'].indexOf(month); // Получаем индекс месяца из массива месяцев
    return new Date(year, monthIndex, day); // Создаем объект Date с использованием полученных значений
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
        const selectedDate = dateFilter.value; // Получаем выбранную дату из фильтра
        const selectedCategory = categoryFilter.value; // Получаем выбранную категорию из фильтра
        const selectedPrice = priceFilter.value; // Получаем выбранную цену из фильтра

        eventCards.forEach(card => {
            const eventDateString = card.dataset.date; // Получаем строку даты мероприятия из атрибута data-date
            const eventDate = parseDate(eventDateString); // Преобразуем строку даты в объект Date
            const eventCategory = card.dataset.category; // Получаем категорию мероприятия из атрибута data-category
            const eventPriceString = card.dataset.price; // Получаем строку цены мероприятия из атрибута data-price
            const eventPrice = parseInt(eventPriceString.replace('₽', '')); // Преобразуем строку цены в число, удаляя символ ₽

            let matchesDate = false; // Флаг соответствия даты
            let matchesCategory = false; // Флаг соответствия категории
            let matchesPrice = true; // Флаг соответствия цены (по умолчанию true)

            const currentDate = new Date(); // Получаем текущую дату
            const currentYear = currentDate.getFullYear(); // Получаем текущий год
            const currentMonth = currentDate.getMonth(); // Получаем текущий месяц
            const currentDay = currentDate.getDate(); // Получаем текущий день

            // Проверяем соответствие даты в зависимости от выбранного фильтра
            if (selectedDate === '') {
                matchesDate = true; // Если фильтр даты не выбран, то все даты соответствуют
            } else if (selectedDate === 'today') {
                matchesDate = eventDate.getFullYear() === currentYear &&
                    eventDate.getMonth() === currentMonth &&
                    eventDate.getDate() === currentDay; // Проверяем, если дата мероприятия совпадает с текущей датой
            } else if (selectedDate === 'tomorrow') {
                const tomorrow = new Date(currentYear, currentMonth, currentDay + 1); // Получаем дату следующего дня
                matchesDate = eventDate.getFullYear() === tomorrow.getFullYear() &&
                    eventDate.getMonth() === tomorrow.getMonth() &&
                    eventDate.getDate() === tomorrow.getDate(); // Проверяем, если дата мероприятия совпадает со следующим днем
            } else if (selectedDate === 'this-week') {
                const startOfWeek = new Date(currentYear, currentMonth, currentDay - currentDay % 7); // Получаем дату начала текущей недели
                const endOfWeek = new Date(startOfWeek.getFullYear(), startOfWeek.getMonth(), startOfWeek.getDate() + 6); // Получаем дату конца текущей недели
                matchesDate = eventDate >= startOfWeek && eventDate <= endOfWeek; // Проверяем, если дата мероприятия находится в пределах текущей недели
            } else if (selectedDate === 'month') {
                matchesDate = eventDate.getFullYear() === currentYear &&
                    eventDate.getMonth() === currentMonth; // Проверяем, если дата мероприятия находится в текущем месяце
            }

            // Проверяем соответствие категории
            if (selectedCategory === '' || eventCategory === selectedCategory) {
                matchesCategory = true; // Если фильтр категории не выбран или совпадает, то категория соответствует
            }

            // Проверяем фильтр по цене
            if (selectedPrice === "1000₽" && eventPrice > 1000) {
                matchesPrice = false; // Если выбрана цена до 1000₽, но цена мероприятия больше 1000₽, то цена не соответствует
            } else if (selectedPrice === "1500₽" && (eventPrice <= 1000 || eventPrice >= 2000)) {
                matchesPrice = false; // Если выбрана цена до 1500₽, но цена мероприятия меньше или равна 1000₽ или больше или равна 2000₽, то цена не соответствует
            } else if (selectedPrice === "2000₽" && eventPrice < 2000) {
                matchesPrice = false; // Если выбрана цена от 2000₽, но цена мероприятия меньше 2000₽, то цена не соответствует
            }

            // Показываем или скрываем карточку мероприятия в зависимости от соответствия даты, категории и цены
            card.style.display = (matchesDate && matchesCategory && matchesPrice) ? 'block' : 'none';
        });
    }

    // События изменения для фильтров
    dateFilter.addEventListener('change', filterEvents); // Вызываем функцию фильтрации при изменении фильтра даты
    categoryFilter.addEventListener('change', filterEvents); // Вызываем функцию фильтрации при изменении фильтра категории
    priceFilter.addEventListener('change', filterEvents); // Вызываем функцию фильтрации при изменении фильтра цены

    // Изначальная фильтрация при загрузке страницы
    filterEvents(); // Вызываем функцию фильтрации при первоначальной загрузке страницы
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



document.addEventListener('DOMContentLoaded', function() {
    // Получаем параметры URL
    const urlParams = new URLSearchParams(window.location.search);
    // Получаем ID мероприятия из параметров URL
    const eventId = urlParams.get('id');

    // Создаем запрос на получение данных мероприятия по его ID
    fetch(`/xu?id=${eventId}`)
       .then(response => response.json())
       .then(eventData => {
            if (eventData) {
                // Заполняем информацию о мероприятии на странице данными из eventData
                document.querySelector('.event-title').innerText = eventData.name; // Заголовок мероприятия
                document.querySelector('.event-date').innerText = `Дата: ${eventData.start_date}`; // Дата мероприятия
                document.querySelector('.event-time').innerText = `Время: ${eventData.start_time}`; // Время мероприятия
                document.querySelector('.event-venue').innerText = `Место: ${eventData.place.name}`; // Место мероприятия
                document.querySelector('.event-description-text').innerText = eventData.description; // Описание мероприятия
                document.querySelector('.event-image').src = eventData.image; // Изображение мероприятия

                // Инициализируем карту Яндекс
                ymaps.ready(init);

                function init() {
                    // Создаем объект карты с центром в координатах мероприятия
                    var myMap = new ymaps.Map("map", {
                        center: [eventData.place.latitude, eventData.place.longitude], // Координаты центра карты
                        zoom: 10 // Масштаб карты
                    });

                    // Добавляем метку на карту в месте проведения мероприятия
                    var myPlacemark = new ymaps.Placemark([eventData.place.latitude, eventData.place.longitude], {
                        hintContent: 'Место проведения мероприятия', // Подсказка при наведении на метку
                        balloonContent: 'Здесь выбранное мероприятие '// Содержание всплывающей подсказки при клике на метку
                    });

                    myMap.geoObjects.add(myPlacemark); // Добавляем метку на карту
                }
            } else {
                // Если данные для мероприятия отсутствуют, выводим сообщение об ошибке
                document.querySelector('main').innerHTML = '<p>Мероприятие не найдено</p>';
            }
        })
       .catch(error => console.error(error));
});

document.addEventListener('DOMContentLoaded', function() {
    const routeCards = document.querySelectorAll('.route-card'); // Получаем все карточки мероприятий

    routeCards.forEach(card => {
        card.addEventListener('click', function() {
            const routeID = card.getAttribute('data-id'); // Получаем ID мероприятия из атрибута data-id
            window.location.href = `/route?id=${routeID}`; // Переходим на страницу с информацией о мероприятии, передавая ID в качестве параметра URL
        });
    });
});

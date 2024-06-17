document.addEventListener('click', e => {
    // определяем, что клик произошёл на ссылке
    if (e.target.nodeName === 'A' & e.target.classList.contains('popup')) {
      // отменяем переход по ссылке
      e.preventDefault()
      window.location.href = '/map_object/' + e.target.innerHTML
      
    }
  })
document.addEventListener('click', e => {
    // определяем, что клик произошёл на ссылке
    if (e.target.nodeName === 'A' & e.target.classList.contains('popup')) {
      // отменяем переход по ссылке
      e.preventDefault()
      window.location.href = '/map_object/' + e.target.innerHTML
      
    }
  })

function createNewFormGroup() {
  // Создаем новый элемент .form-group
  const newFormGroup = document.createElement('div');
  newFormGroup.classList.add('form-group');

  const inputs = document.querySelectorAll('input');
  let maxId = 0;
  inputs.forEach(input => {
    const id = parseInt(input.getAttribute('id')); // Получаем значение атрибута "id" и преобразуем его в число

    if (!isNaN(id) && id > maxId) {
        maxId = id;
    }
  });

  // Создаем метку и поле ввода для нового элемента
  newFormGroup.innerHTML = `
      <label for="point">Новое поле</label>
      <input type="text" id=${maxId+1} name=${maxId+1} required>
  `;

  return newFormGroup;
};

document.addEventListener( "DOMContentLoaded" , function() {
  let start = document.querySelector('.add-form');

  start.addEventListener('click', function () {
    const newElement = createNewFormGroup();
    const lastFormGroup = document.querySelector('.form-group:last-of-type');
    console.log(lastFormGroup.id)
    lastFormGroup.parentNode.insertBefore(newElement, lastFormGroup);
  });
});

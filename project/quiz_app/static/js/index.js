const vars = document.querySelectorAll('[name="variant"]');


vars.forEach((element)=>{
  element.addEventListener('change', (event)=>{
    document.querySelector('button').disabled = false
  })
})
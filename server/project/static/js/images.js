document.addEventListener('DOMContentLoaded', () => {
    var addCategoryButton = document.querySelector('#add_img_btn');
    var addForm = document.querySelector('#add_img_form');
      addCategoryButton.addEventListener('click', () =>{
        if(window.getComputedStyle(addForm).display === 'block'){
            HideAddForm(addForm, addCategoryButton);
            return;
        }
        addForm.style.display = 'block';
        addCategoryButton.innerHTML = "Hide";
    })
    var img_input = document.querySelector('#img_file');
    img_input.addEventListener('change', (e) => {
        readURL(e.target);
    })
})

function readURL(input){
    if(input.files && input.files[0]){
      var reader = new FileReader();
      reader.onload = function(e){
          var img = document.querySelector('#preview_image');
          img.setAttribute('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]);
    }
  }

function HideAddForm(form, btn){
    form.style.display = 'none';
    btn.innerHTML = "Add";
}
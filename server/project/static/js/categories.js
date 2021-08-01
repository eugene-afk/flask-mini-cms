document.addEventListener('DOMContentLoaded', () => {
    var addCategoryButton = document.querySelector('#add_cat_btn');
    var addForm = document.querySelector('#add_cat_form');
      addCategoryButton.addEventListener('click', () =>{
        if(window.getComputedStyle(addForm).display === 'block'){
            HideAddForm(addForm, addCategoryButton);
            return;
        }
        var edit_form_div = document.querySelector('.update_cat_form');
        if(edit_form_div.innerHTML != ""){
          edit_form_div.innerHTML = "";
        }
        addForm.style.display = 'block';
        addCategoryButton.innerHTML = "Hide";
        
        FocusTop();
    })

    var editCategoryButtons = document.querySelectorAll('.edit_cat_btn');
    if(editCategoryButtons != null){
      for(var i = 0; i < editCategoryButtons.length; ++i){
        editCategoryButtons[i].addEventListener('click', (e) => {
            if(window.getComputedStyle(addForm).display === 'block'){
                HideAddForm(addForm, addCategoryButton);
            }
            var data = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.id.split('_');
            var form_html= '<form action="/ucat/' + data[0] + '" method="post" autocomplete="false">'+
                            '<div class="field">'+
                                '<div class="control">'+
                                    '<input id="category_name" class="input is-medium mb-2" type="text"'+
                                            'name="category_name"'+
                                            'value="'+ data[1] +'"'+
                                            'placeholder="Type new category name"'+
                                            'autofocus="">'+
                                        '<button class="button is-block is-info is-small is-fullwidth">Save</button>'+
                                '</div>'+
                            '</div>'+
                        '</form>'+
                        '<button id="cancel_edit_cat" class="button is-block is-danger is-small is-fullwidth mt-2">Cancel</button>'
            var form_div = document.querySelector('.update_cat_form');
            form_div.innerHTML = form_html;
            
            FocusTop();
        })
      }
    }

    document.addEventListener('click', (e) => {
        if(e.target.id == 'cancel_edit_cat'){
            document.querySelector('.update_cat_form').innerHTML = "";       
        }
    })

})

function HideAddForm(form, btn){
    form.style.display = 'none';
    btn.innerHTML = "Add";
}

function FocusTop(){
    var input = document.querySelector('#category_name');
    input.focus();
    input.selectionStart = input.selectinEnd = input.value.length;
    window.scrollTo(0, 0);
}
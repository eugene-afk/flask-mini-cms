document.addEventListener('DOMContentLoaded', () => {
    var addLanguageButton = document.querySelector('#add_lang_btn');
    var addForm = document.querySelector('#add_lang_form');
      addLanguageButton.addEventListener('click', () =>{
        if(window.getComputedStyle(addForm).display === 'block'){
            HideAddForm(addForm, addLanguageButton);
            return;
        }
        var edit_form_div = document.querySelector('.update_lang_form');
        if(edit_form_div.innerHTML != ""){
          edit_form_div.innerHTML = "";
        }
        addForm.style.display = 'block';
        addLanguageButton.innerHTML = "Hide";

        FocusTop();
    })

    var editLanguageButtons = document.querySelectorAll('.edit_lang_btn');
    if(editLanguageButtons != null){
      for(var i = 0; i < editLanguageButtons.length; ++i){
        editLanguageButtons[i].addEventListener('click', (e) => {
            if(window.getComputedStyle(addForm).display === 'block'){
                HideAddForm(addForm, addLanguageButton);
            }
            var data = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.id.split('_');
            console.log(e)
            var form_html= '<form action="/ulang/' + data[0] + '" method="post" autocomplete="false">'+
                            '<div class="field">'+
                                '<div class="control">'+
                                    '<input id="language_name" class="input is-medium mb-2" type="text"'+
                                            'name="language_name"'+
                                            'value="'+ data[1] +'"'+
                                            'placeholder="Type new language name"'+
                                            'autofocus="">'+
                                    '<input id="language_code" class="input is-medium mb-2" type="text"'+
                                            'name="language_code"'+
                                            'value="'+ data[2] +'"'+
                                            'placeholder="Type new language code"'+
                                            'autofocus="">'+
                                        '<button class="button is-block is-info is-small is-fullwidth">Save</button>'+
                                '</div>'+
                            '</div>'+
                        '</form>'+
                        '<button id="cancel_edit_lang" class="button is-block is-danger is-small is-fullwidth mt-2">Cancel</button>'
            var form_div = document.querySelector('.update_lang_form');
            form_div.innerHTML = form_html;

            FocusTop();
        })
      }
    }

    document.addEventListener('click', (e) => {
        if(e.target.id == 'cancel_edit_lang'){
            document.querySelector('.update_lang_form').innerHTML = "";       
        }
    })

})

function HideAddForm(form, btn){
    form.style.display = 'none';
    btn.innerHTML = "Add";
}

function FocusTop(){
    var input = document.querySelector('#language_name');
    input.focus();
    input.selectionStart = input.selectinEnd = input.value.length;
    window.scrollTo(0, 0);
} 
document.addEventListener('DOMContentLoaded', () => {
    var editTagButtons = document.querySelectorAll('.edit_tag_btn');
    if(editTagButtons != null){
      for(var i = 0; i < editTagButtons.length; ++i){
        editTagButtons[i].addEventListener('click', (e) => {
            var data = e.target.parentNode.parentNode.parentNode.parentNode.parentNode.id.split('_');
            var form_html= '<form action="/utag/' + data[0] + '" method="post" autocomplete="off">'+
                            '<div class="field">'+
                                '<div class="control">'+
                                    '<input id="tag_name" class="input is-medium mb-2" type="text"'+
                                            'name="tag_name"'+
                                            'value="'+ data[1] +'"'+
                                            'placeholder="Type new tag name"'+
                                            'autofocus="">'+
                                        '<button class="button is-block is-info is-small is-fullwidth">Save</button>'+
                                '</div>'+
                            '</div>'+
                        '</form>'+
                        '<button id="cancel_edit_tag" class="button is-block is-danger is-small is-fullwidth mt-2">Cancel</button>'
            var form_div = document.querySelector('.update_tag_form');
            form_div.innerHTML = form_html;
            
            var input = document.querySelector('#tag_name');
            input.focus();
            input.selectionStart = input.selectinEnd = input.value.length;
            window.scrollTo(0, 0);
        })
      }
    }

    document.addEventListener('click', (e) => {
        if(e.target.id == 'cancel_edit_tag'){
            document.querySelector('.update_tag_form').innerHTML = "";       
        }
    })
})
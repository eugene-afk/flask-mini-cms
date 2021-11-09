var langs = JSON.parse(document.currentScript.getAttribute('langs'))
var csrf_token = document.currentScript.getAttribute("data-csrf");

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

async function getCategoryTranslation(id, lang){
    $.ajaxSetup({
      beforeSend: function(xhr, settings){
        if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
          xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
      }
    });

    var res = await $.ajax({
      url: `/get_translation?lang=${lang}&id=${id}`,
      cache: false,
      contentType: false,
      processData: false,
      type: "GET",
      success: function(data){
            // console.log(data)
            return data
      },
      error: function(data){
        // console.log(data);
        return ""
      }
    });
    return res
}

async function edit(e){
  var addForm = document.querySelector('#add_cat_form');
  if(window.getComputedStyle(addForm).display === 'block'){
      HideAddForm(addForm, addCategoryButton);
  }
  var data = e.id.split('_');
  var inputs = ''
  for(var i = 0; i < langs.langs.length; ++i){
      var translation = await getCategoryTranslation(data[2], langs.langs[i].lang_code)
      inputs += `<input id="category_name_${langs.langs[i].lang_code}" class="input is-medium mb-2" type="text"
                      name="category_name_${langs.langs[i].lang_code}"
                      value="${translation}"
                      placeholder="Type new category name (${langs.langs[i].lang_name})"
                      autofocus="">`
  }
  var form_html= '<form action="/ucat/' + data[0] + '" method="post" autocomplete="false">'+
                  '<div class="field">'+
                      '<div class="control">'+
                          '<input id="category_name" class="input is-medium mb-2" type="text"'+
                                  'name="category_name"'+
                                  'value="'+ data[1] +'"'+
                                  'placeholder="Type new category name"'+
                                  'autofocus="">'+ inputs +
                              '<button class="button is-block is-info is-small is-fullwidth">Save</button>'+
                      '</div>'+
                  '</div>'+
              '</form>'+
              '<button id="cancel_edit_cat" class="button is-block is-danger is-small is-fullwidth mt-2">Cancel</button>'
  var form_div = document.querySelector('.update_cat_form');
  form_div.innerHTML = form_html;

  FocusTop();
} 
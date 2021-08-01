$(document).ready(function() {

  $('#title').setCursorPosition($('#title').val().length);
  $('#summernote').summernote({
    disableResizeEditor: true,
    height: 600,
    placeholder: 'Start writing here...',
    callbacks:{
      onImageUpload: function(image){
        uploadImage(image[0]);
      }
    },
    toolbar:[
      ['style', ['bold', 'italic', 'underline', 'clear']],
      ['font style', ['fontname']],
      ['fontsize', ['fontsize']],
      ['color', ['color']],
      ['para', ['style', 'ul', 'ol', 'paragraph']],
      ['insert', ['picture', 'link', 'video']],
      ['height', ['height']],
      ['misc', ['codeview']]
    ]
  });

  $('#img_file').on('change', function(e){
    readURL(e.target);
  })

  $('#tag_input').on('change', function(e){
      var tags = $('#tags');
      var tag = e.target.value;

      e.target.value = "";
      //e.target.blur();
      $(e.target).trigger('focusout');
      if(tags.val().length > 0){
        tags.val(tags.val() + ', ' + tag);
        return;
      }
      tags.val(tag);
  })

  $(document).on('click', '.gallery-img', function(e){
    selectImage(e.target);
  })

  $('#img_gallery_btn').on('click', function(){
    getImages(galleryPage);
  })

  $(document).on('click', '#unselect_img_btn', function(e){
    $('.img-selected').each(function(){
      $(this).removeClass("img-selected");
    })
    $('#selected_note').text(no_img_selected_txt);
    $('#unselect_img_btn').hide();
  })

  $(document).on('click', '#select_to_post_img_btn', function(e){
    if($('#select_to_post_img_btn').attr('disabled')){
      return;
    }
    $('.img-selected').each(function(){
      var src = $(this).attr('src');
      var image = $('<img>').attr('src', src).addClass("img-fluid");
      $('#summernote').summernote("insertNode", image[0]);
    })
  })

  $(document).on('click', '#select_as_main_img_btn', function(e){
    if($('#select_as_main_img_btn').attr('disabled')){
      return;
    }
    var imgCount = $('.img-selected').length;
    if(imgCount > 1){
      alert(main_img_select_alert_txt);
      return;
    }
    var src = $('.img-selected').attr('src');
    $('#selected_image').attr('src', src);
    
    var imageName = src.replace('/static/img/media/', '');
    $('#storage_img').val(imageName);
  })

  $(document).on('click', '#gallery_next', function(){
    galleryPage += 1;
    getImages(galleryPage);
    $('#gallery_prev').attr('disabled', false);
    hideUnselect();
  })

  $(document).on('click', '#gallery_prev', function(){
    galleryPage -= 1;
    getImages(galleryPage);
    if(galleryPage == 1){
      $('#gallery_prev').attr('disabled', true);
    }
    hideUnselect();
  })

  $('#img_file_trigger').on('click', function(){
    $('#img_file').click();
  })

});

const no_img_selected_txt = "No selected images.";
const img_selected_txt = "Selected <strong>#VAL#</strong> images.";
const img_item_template_node = '<div class="col-2 pb-4">'+
'<img class="gallery-img pointer" src="/static/img/media/#VAL#" class="img-fluid">'+
'</div>'
const main_img_select_alert_txt = 'For main image you need to select only 1 picture.';
var galleryPage = 1;

function readURL(input){
  if(input.files && input.files[0]){
    var reader = new FileReader();
    reader.onload = function(e){
      $('#selected_image').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
    var storage_img = $('#storage_img');
    if(storage_img.val() != ""){
      storage_img.val('');
    }
  }
}

function uploadImage(image){
  var data = new FormData();
  data.append('img', image)
  var csrf_token = document.getElementById("post_js").getAttribute("data-csrf");

  $.ajaxSetup({
    beforeSend: function(xhr, settings){
      if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
      }
    }
  });

  $.ajax({
    url: "/saveimg",
    cache: false,
    contentType: false,
    processData: false,
    data: data,
    type: "POST",
    success: function(filename){
      console.log(filename);
      var image = $('<img>').attr('src', filename).addClass("img-fluid");
      $('#summernote').summernote("insertNode", image[0]);
    },
    error: function(data){
      // console.log(data);
    }
  });
}

$.fn.setCursorPosition = function(pos) {
  this.each(function(index, elem) {
    if (elem.setSelectionRange) {
      elem.setSelectionRange(pos, pos);
    }
    else if (elem.createTextRange) {
      var range = elem.createTextRange();
      range.collapse(true);
      range.moveEnd('character', pos);
      range.moveStart('character', pos);
      range.select();
    }
  });
  return this;
};

async function getImages(page){
  const response = await fetch('/imglist?page=' + page);
  const data = await response.json();
  var gallery = $('#gallery_grid');
  var note = $('#selected_note');

  if(data['total_pages'] == 0){
    gallery.empty().append('<div class="text-muted text-center d-flex justify-content-center w-100">No images.</div>');
    $('#select_as_main_img_btn').attr('disabled', true).addClass('disabled');
    $('#select_to_post_img_btn').attr('disabled', true).addClass('disabled');
    return;
  }

  gallery.empty();
  for(var i = 0; i < data['imgs'].length; ++i){
    var node = $(img_item_template_node.replace('#VAL#', data['imgs'][i]['media_name']));
    gallery.append(node);
  }

  note.empty();
  note.append(no_img_selected_txt);

  var next = $('#gallery_next');
  if(data['current_page'] != data['total_pages']){
    next.attr('disabled', false);
    return;
  }
  next.attr('disabled', true);
}

function selectImage(imageElem){
  $(imageElem).toggleClass("img-selected");
  var selectedCount = $('.img-selected').length;
  var note = $('#selected_note');
  var unselectButton = $('#unselect_img_btn');

  note.empty();
  if(selectedCount > 0){
    note.append(img_selected_txt.replace("#VAL#", selectedCount));
    if(unselectButton.is(":hidden")){
      unselectButton.show();
    }
    return;
  }  

  note.append(no_img_selected_txt);
  unselectButton.hide();
}

function hideUnselect(){
  var unselectButton = $('#unselect_img_btn');
  if(unselectButton.is(":visible")){
    unselectButton.hide();
  }
}
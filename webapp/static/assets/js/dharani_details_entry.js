$(document).ready(function() {
    getScreens()
    $('.sidebar').css('display', 'none')
    $('#open_sidebar').css('display', 'block')
//    if(verify_access){
//        $('.edit_access').remove()
//        $('.tablinks').first().addClass('active')
//        $('.tabcontent').first().css('display', 'block')
//    }

});

$('#revert').on('click', function(){
    location.reload()
})

$('#open_sidebar').on('click', function(){
    $('.sidebar').css('display', 'block')
    $(this).css('display', 'none')
})

function closeNav(){
    $('.sidebar').css('display', 'none')
    $('#open_sidebar').css('display', 'block')
}

$('#add_row').on('click', function(){
    if($('.loop').length){
        sno = parseInt($('.loop').last().html()) + 1
    }else{
        sno = 1
    }
    row_html = '<tr><td class="loop">'+sno+'</td><td class="p-0"><textarea  class="district" required></textarea></td>'+
    '<td class="p-0"><textarea class="mandal" required></textarea></td>'+
    '<td class="p-0"><textarea class="village" required></textarea></td>'+
    '<td class="p-0"><textarea class="survey_no" required></textarea></td>'+
    '<td class="p-0"><textarea class="extent" required></textarea></td>'+
    '<td class="p-0"><textarea class="pattadar" required></textarea></td>'+
    '<td class="p-0"><select class="signed" required><option selected disabled></option>'+
    '<option value="Y">Yes</option><option value="N">No</option></select></td>'+
    '<td class="p-0"><i style="font-size:24px" class="fa delete">&#xf014;</i></td></tr>'
    $('#dharani_table').append(row_html)
})

var delete_ids = []
$(document).on('click', '.delete', function() {
    if(this.id){
        delete_ids.push(this.id.replace('delete', ''))
    }
    $(this).parent('td').parent('tr').remove()
    s_no = 1
    $('#dharani_table tr').each(function(){
        $(this).children('td').first().html(s_no)
        s_no += 1
    })
});


$(document).on('keypress', '.extent', function(event) {
    if ((event.which != 46 || $(this).val().indexOf('.') != -1) && (event.which < 48 || event.which > 57)) {
        event.preventDefault();
    }
});

function save_data(){
    temp = []
    $('#dharani_table tr').each(function(){
        td = $(this).children('td')
        sno = parseInt(td.first().html())
        district = td.children('.district').val()
        mandal = td.children('.mandal').val()
        village = td.children('.village').val()
        survey_no = td.children('.survey_no').val()
        extent = td.children('.extent').val()
        pattadharname = td.children('.pattadar').val()
        isdigitallysigned = td.children('.signed').val()
        id = null
        if(this.id){
            id = this.id.replace('tr', '')
        }
        temp.push({'district': district, 'mandal': mandal, 'village': village, 'surveyno': survey_no,
        'extent': extent, 'pattadharname': pattadharname, 'isdigitallysigned': isdigitallysigned, 'sno': sno,
        'prelimtaskid': prelimtaskid, 'requestid': requestid, 'id': id})
    })
    if($('#save').length){
        final_data = {
            'data': JSON.stringify(temp),
            'delete_ids': JSON.stringify(delete_ids),
            'notes': $('#dharani_notes').val(),
            'hours': $('#entryhours').val(),
            'status': $('#status').val(),
            'prelimtaskid': prelimtaskid,
            csrfmiddlewaretoken: CSRF_TOKEN
        }
    }else{
        final_data = {
            'remarks': $('#dharani_comments').val(),
            'verifyhours': $('#verifyhours').val(),
            'status': $('#status').val(),
            'prelimtaskid': prelimtaskid,
            csrfmiddlewaretoken: CSRF_TOKEN
        }
    }
    console.log(final_data)
    $.post("http://localhost:8000/save-dharani-details", final_data, function (res) {
        window.location.href = "./preliminary-verification"+requestid
    });
}
// Query the element
const resizer = document.getElementById('dragMe');
const leftSide = resizer.previousElementSibling;
const rightSide = resizer.nextElementSibling;

// The current position of mouse
let x = 0;
let y = 0;

// Width of left side
let leftWidth = 0;

// Handle the mousedown event
// that's triggered when user drags the resizer
const mouseDownHandler = function (e) {
    // Get the current mouse position
    x = e.clientX;
    y = e.clientY;
    leftWidth = leftSide.getBoundingClientRect().width;

    // Attach the listeners to `document`
    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
};

// Attach the handler
resizer.addEventListener('mousedown', mouseDownHandler);

const mouseMoveHandler = function (e) {
    // How far the mouse has been moved
    const dx = e.clientX - x;
    const dy = e.clientY - y;

    const newLeftWidth = ((leftWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
    leftSide.style.width = `${newLeftWidth}%`;
    resizer.style.cursor = 'col-resize';
    document.body.style.cursor = 'col-resize';
    leftSide.style.userSelect = 'none';
    leftSide.style.pointerEvents = 'none';

    rightSide.style.userSelect = 'none';
    rightSide.style.pointerEvents = 'none';
};

const mouseUpHandler = function () {
    resizer.style.removeProperty('cursor');
    document.body.style.removeProperty('cursor');

    leftSide.style.removeProperty('user-select');
    leftSide.style.removeProperty('pointer-events');

    rightSide.style.removeProperty('user-select');
    rightSide.style.removeProperty('pointer-events');

    // Remove the handlers of `mousemove` and `mouseup`
    document.removeEventListener('mousemove', mouseMoveHandler);
    document.removeEventListener('mouseup', mouseUpHandler);
};


// tabs

function openScreen(evt, cityName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

//$('#upload_file').on('change', function(){
//    file = $(this)[0].files[0]
//    console.log(file)
//})

function zoomin(screen_name){
    var currWidth = $("#"+screen_name).width()
    if(currWidth == 2500) return false;
    else{
        $("#"+screen_name).width(currWidth + 100);
    }
}
function zoomout(screen_name){
    var currWidth = $("#"+screen_name).width()
    if(currWidth == 100) return false;
    else{
        console.log(currWidth - 100)
        $("#"+screen_name).width(currWidth - 100);
    }
}

// drop and upload file

document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");

  dropZoneElement.addEventListener("click", (e) => {
    inputElement.click();
  });

  inputElement.addEventListener("change", (e) => {
    if (inputElement.files.length) {
        file = inputElement.files[0]
        upload_file(file)
    }
  });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("drop-zone--over");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("drop-zone--over");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();

    if (e.dataTransfer.files.length) {
      inputElement.files = e.dataTransfer.files;
      upload_file(inputElement.files[0])
//      updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
    }

    dropZoneElement.classList.remove("drop-zone--over");
  });
});

/**
 * Updates the thumbnail on a drop zone element.
 *
 * @param {HTMLElement} dropZoneElement
 * @param {File} file
// */
//function updateThumbnail(dropZoneElement, file) {
//  let thumbnailElement = dropZoneElement.querySelector(".drop-zone__thumb");
//
//  // First time - remove the prompt
//  if (dropZoneElement.querySelector(".drop-zone__prompt")) {
//    dropZoneElement.querySelector(".drop-zone__prompt").remove();
//  }
//
//  // First time - there is no thumbnail element, so lets create it
//  if (!thumbnailElement) {
//    thumbnailElement = document.createElement("div");
//    thumbnailElement.classList.add("drop-zone__thumb");
//    dropZoneElement.appendChild(thumbnailElement);
//  }
//
//  thumbnailElement.dataset.label = file.name;
//
//  // Show thumbnail for image files
//  if (file.type.startsWith("image/")) {
//    const reader = new FileReader();
//
//    reader.readAsDataURL(file);
//    reader.onload = () => {
//      thumbnailElement.style.backgroundImage = `url('${reader.result}')`;
//    };
//  } else {
//    thumbnailElement.style.backgroundImage = null;
//  }
//}


// upload file
function upload_file(file){
    var re = /(\.jpg|\.png|\.pdf)$/i;
    if (re.exec(file.name)) {
//        console.log(file.name.split('.'))
        filetype = file.name.split('.')[file.name.split('.').length-1][0]
        var fd = new FormData();
        data = {'requestid': requestid, 'task': 'D', 'filename': file.name, 'filetype': filetype}
        fd.append('file', file)
        fd.append('data', JSON.stringify(data));
//        console.log(fd)
        $.ajax({
            url: "http://localhost:8000/save-image",
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: 'POST',
            data: fd,
            processData: false,
            contentType: false,
            success: function(res){
                display_screens(res)
            }
        });
    }else{
        swal("", "Only pdf,jpg and png formats are allowed", "warning");
    }
}

function getScreens(){
    $.get("http://localhost:8000/get-screens?requestid="+requestid+"&task=D", function (res) {
        display_screens(res)
    });
}

$('#clear').on('click', function(){
    location.reload()
})



function display_screens(res){
    tabs = ''
    screens = ''
    $('.remove_class').remove()
//    $('#drop-zone').prepend(screens)
    for(i=0;i<res['data'].length;i++){
        screen = res['data'][i]['screen']
        screen_name = res['data'][i]['function']
        filecontent = res['data'][i]['file']
        ext = res['data'][i]['ext']
        doc_id = res['data'][i]['doc_id']
        screen_id = JSON.stringify(screen.replace(' ', '_'))
        screen_zoom = JSON.stringify(screen.replace(' ', '_') + "zoom")
        if(ext != 'pdf'){
            image_html = '<img id='+screen_zoom+' src="'+filecontent+'" />'
        }else{
//            image_html = '<embed type="application/pdf" id='+screen_zoom+' src="'+filecontent+'">'
            image_html = '<iframe id='+screen_zoom+' src="D:\\Downloads\\Payslip_Sep_2022.pdf"></iframe>'
        }
        tabs += '<button class="tablinks remove_class" onclick="'+screen_name+'">'+screen+'</button>'
        screens += '<div id='+screen_id+' class="tabcontent remove_class"><div id="navbar">'+
        "<button type='button' class='zoom p-2 m-2' onclick='zoomin("+screen_zoom+")'>"+
        '<i class="fa fa-search-plus" aria-hidden="true"></i></button>'+
        "<button type='button' class='zoom p-2 m-2' onclick='zoomout("+screen_zoom+")'>"+
        '<i class="fa fa-search-minus" aria-hidden="true"></i></button>'+
        "<button type='button' class='zoom p-2 m-2 mr-5' onclick='delete_image("+doc_id+")' style='float: right;'>"+
        '<i style="font-size:24px"  class="fa delete">&#xf014;</i></button></div>'+
        '<div class="main">'+image_html+'</div></div>'
    }
//    console.log(screens)
    $('#add_screen').prepend(tabs)
    $('#screens').prepend(screens)
    console.log(verify_access)
    if(verify_access != "False"){
        $('.edit_access').remove()
        $('.tablinks').first().addClass('active')
        $('.tabcontent').first().css('display', 'block')
        $('td textarea').attr('disabled', true)
    }
}


function delete_image(doc_id){
    swal("Are you sure want to delete?", {
        dangerMode: true,
        buttons: true,
    })
    .then((confirm) => {
        if (confirm) {
            var final_data = {
                'task': 'D',
                'requestid': requestid,
                'doc_id': doc_id,
                csrfmiddlewaretoken: CSRF_TOKEN
            };
            $.post("http://localhost:8000/delete-screen", final_data, function (res) {
                display_screens(res)
                $('.tablinks').last().addClass('active')
                $('#drop-zone').css('display', 'block')
            });
        }
    });
}
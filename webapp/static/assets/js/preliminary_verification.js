$(document).ready(function() {
    $('select').on('change',  function(){
        values = this.id.split('_')
        tasktype = values[0]
        to = values[1]
        assign_to = $(this).val()
        var final_data = {
            'tasktype': tasktype,
            'to': to,
            'assign_to': assign_to,
            'req_id': req_id,
            csrfmiddlewaretoken: CSRF_TOKEN
        };
        console.log(final_data)
        $.post("http://localhost:8000/save-preliminarytask", final_data, function (res) {
            location.reload();
        });
    })
})
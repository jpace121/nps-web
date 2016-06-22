/*
  Contains javascript functions for analysis.html page.
  */

/* Page load globals.*/
// There is probably a better way to do this.
// These are reset in send file
var global_cone_maxes = [];
var global_donut_maxes = [];
var global_range_maxes = [];
var global_cur_filename;

/* Run at page load. */
$(function (event){
    display_files();
    $("#fileSelect").collapse('show');
});

/* Attach functions to buttons. */
$("#submit-file-button").click(function (event){
    send_file();
    $("#fileSelect").collapse('hide');
    $("#validGraphSelect").collapse('show');
});

$("#submit-max-button").click(function (event){

    $("#validGraphSelect").collapse('hide');
    $("#resultsCollapse").collapse('show');
    show_results();
});


/* Function definitions. */
var display_files = function () {
    $.getJSON($SCRIPT_ROOT + '/_get_downloads',{
       option: "update"
    }, function(data) {
        //console.log(data.result);
        $('#file-list').empty();
        data.result.forEach(function (curVal, index, array) {
            $('#file-list').append('<tr> <td> <input type="radio" name="fileList" value = "' + curVal + '">' + curVal + '</td> </tr>');
        });
    });
};

var send_file = function () {
    var to_send;
    var request;
    global_cone_maxes = [];
    global_donut_maxes = [];
    global_range_maxes = [];
    global_cur_filename = [];

    to_send = $('input[name=fileList]:checked').val();
    
    request = $.ajax({
        url: "/_analysis/upload/"+to_send,
        type: 'POST',
        });
    request.error(function(response) {
        console.log('Error from AJAX call (send_file).');
        });
    request.done(function(response) {
        var cone_maxes = response.result.cone_maxes;
        var donut_maxes = response.result.donut_maxes;
        var plot_dict = response.result.plot_dict;
        var range_maxes = response.result.range_maxes;
        plot_dict.forEach( function (plot, index, array) {
            $('#plot-maxes-tbl').append('<tr>' +
                                        '<td>' +
                                        "<img class='img-responsive' src=data:image/png;base64," + plot + '>'+
                                        '</td>' +
                                        '<td>' +
                                        '<p> Cone Max: ' + cone_maxes[index] + '</p>' +
                                        '<p> Donut Max: ' + donut_maxes[index] + '</p>' +
                                        '</td>' +
                                        '<td>' +
                                        '<input type="checkbox" name="plotList" value = "' +
                                        index + '">' +
                                        '</td>' + 
                                        '</tr>');
            global_cone_maxes.push(cone_maxes[index]); //Do I need to do this in the for loop?
            global_donut_maxes.push(donut_maxes[index]); //Ditto
            global_range_maxes.push(range_maxes[index]); //More ditto
            });
        global_cur_filename = response.result.filename;
        });
};

var show_results = function () {
    var selected = [];
    var cone_max = [];
    var donut_max = [];
    var range_max = [];
    var request;
    var data;

    //What checkbox was checked?
    $('input[name=plotList]:checked').each(function() {
        selected.push($(this).attr('value'));
     });
    selected = selected.map(Number); //Convert to number, not string

    //Selected contains index of maxes, need actual maxes.
    selected.forEach(function (num, index, arr) {
        cone_max.push(global_cone_maxes[num]);
        donut_max.push(global_donut_maxes[num]);
        range_max.push(global_range_maxes[num]);
    });

    data = {'cone_maxes':cone_max,
            'donut_maxes':donut_max,
            'range_maxes':range_max,
            'filename': global_cur_filename
            };
    
    request = $.ajax({
        url: "/_analysis/calc_ratio",
        type: 'POST',
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8'
    });
    request.error(function (response) {
        console.log('AJAX error show_results.');
    });
    request.done(function (response) {
        console.log(response);
    });
}

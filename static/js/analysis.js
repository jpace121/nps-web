/*
  Contains javascript functions for analysis.html page.
  */
$("#file-form").submit(function (event){
    var fd = new FormData();
    var request;
    var data;
    var download_bool = false;
    event.preventDefault();
    console.log("File uploading.");
    
    download_bool = $("#download-chk").is(':checked');
    console.log('download_bool values is: ' + download_bool);
    
    $("#submit-btn").text("Uploading...");
    fd.append('file',$("#file-input")[0].files[0]);
    request = $.ajax({
        url: "/_analysis/upload?response=" + download_bool,
        data: fd,
        processData: false,
        contentType: false,
        type: "POST",
        });
    request.done(function(response) {
        //console.log(response);
        $("#submit-btn").text("Submit");
        response.result.filenames.forEach(function (filename, index, array) {
            plots = response.result.plots;
            $("#results").append("<tr>" +
                                 "<td>" +'<a href="' + $SCRIPT_ROOT + 'log\\' +
                                    filename + '">' + filename + '<\a>' +
                                 "</td>" +
                                 "<td>" + "<img src=" +"data:image/png;base64,"
                                    + plots[index] + ">" + " </td>" +
                                 "</tr>");
            });
        });
    request.error(function(reponse) {
        console.log('Error from AJAX call.');
        $("#submit-btn").text("Try again?");
        });
})

$("#clear-btn").click(function () {
    $("#results td").remove();
})


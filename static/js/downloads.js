/*
  javascript for downloads.html
  Displays the files, allows the files to be downloaded, allows files to be
  deleted.
*/

/*"Helper" functions. */
var display_files = function () {
    $.getJSON($SCRIPT_ROOT + '/_get_downloads',{
       option: "update"
    }, function(data) {
        console.log(data.result);
        //$('#file-list').html('<ul> </ul>').text(' ');
        data.result.forEach(function (curVal, index, array) {
            $('#file-list').append("<p>"+ curVal+"</p>");
        });
    });
};

/* "Bound to keys" function. */
//Delete
$(function () {
    $('#delete-btn').bind('click',function () {
        console.log("Delete button got hit!");
        $.getJSON($SCRIPT_ROOT + '/_get_downloads',{
            option: "delete"
       }, function(data) {
           if(data.result !== "error") {
               console.log("Delete Button success.");
          }else{
              $("#delete-btn").text("Try Again?");
         }
       });
        return false; //to remove the button from hreffing
        });
});

$(function () {
    $('#update-btn').bind('click',function () {
        console.log("Update button got hit!");
        display_files();
        return false; //to remove the button from hreffing
       });
});

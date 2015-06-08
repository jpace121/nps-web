/*
  Javascript for range_finder.html
  This should be refactored to something that uses less
  anonymous functions.
*/

//Start Streaming
$(function () {
    $('#start-stream-btn').bind('click',function () {
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_start"
       }, function(data) {
           $("#start-stream-btn").text("Streaming...")
       });
        return false; //to remove the button from hreffing
        })
});

//Stop Streaming
$(function () {
    $('#stop-stream-btn').bind('click',function () {
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_stop"
       }, function(data) {
           $("#start-stream-btn").text("Start Stream")
           $("#result").text(data.result)
       });
        return false; //to remove the button from hreffing
        })
});

//Read Once
$(function () {
    $('#once-btn').bind('click',function () {
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "once"
       }, function(data) {
           $("#result").text(data.result)
       });
        return false; //to remove the button from hreffing
        })
});

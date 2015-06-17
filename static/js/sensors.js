/*
  Javascript for range_finder.html
  This should be refactored to something that uses less
  anonymous functions.
*/

//Connect
$(function () {
    $('#connect-btn').bind('click',function () {
        $("connect-btn").text("Connecting...");
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "connect"
       }, function(data) {
           $("#connect-btn").text("Connected!");
           $("#stream-btn").removeClass("disabled");
           $("#once-btn").removeClass("disabled");
       });
        return false; //to remove the button from hreffing
        })
});
//Streaming
$(function () {
    $('#stream-btn').bind('click',function () {
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
           $("#result").html(data.result)
       });
        return false; //to remove the button from hreffing
        })
});

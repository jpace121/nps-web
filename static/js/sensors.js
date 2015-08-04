/*
  Javascript for range_finder.html
  This should be refactored to something that uses less
  anonymous functions.
*/

/* Helper functions. */

$(function () {
    getStatus();
    //setInterval(getStatus,1000);
   //^ conflicted with the "loading" style messages that overlay some keys.
})

function getStatus() {
    $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
        option: "get_status"
    }, function(data) {
        if(data.result.connected){
            $("#connect-btn").text("Connected!");
            $("#connect-btn").addClass("disabled");
            $("#disconnect-btn").removeClass("disabled");
            $("#once-btn").removeClass("disabled");
        }else{
            $("#connect-btn").text("Connect");
            $("#connect-btn").removeClass("disabled");
            $("#disconnect-btn").addClass("disabled");
            $("#once-btn").addClass("disabled");
        }
        if(data.result.streaming && data.result.connected){
            $("#start-stream-btn").text("Streaming...");
            $("#start-stream-btn").addClass("disabled");
            $("#stop-stream-btn").removeClass("disabled");
        }else if(data.result.connected){ //hack?
            $("#start-stream-btn").text("Start Stream");
            $("#start-stream-btn").removeClass("disabled");
            $("#stop-stream-btn").addClass("disabled");
        }
    });
}

/*"Bound to keys" functions. */

//Connect
$(function () {
    $('#connect-btn').bind('click',function () {
        $("#connect-btn").text("Connecting...");
        console.log("Connect button got hit!");
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "connect"
       }, function(data) {
           if(data.result !== "error") {
            $("#connect-btn").text("Connected!");
            $("#connect-btn").addClass("disabled");
            $("#start-stream-btn").removeClass("disabled");
            $("#once-btn").removeClass("disabled");
            $("#disconnect-btn").removeClass("disabled");
          }else{
              $("#connect-btn").text("Try Again?");
         }
       });
        return false; //to remove the button from hreffing
        });
});

//Disconnect
$(function () {
    $('#disconnect-btn').bind('click',function () {
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "disconnect"
       }, function(data) {
           if(data.result !== "error") {
                $("#connect-btn").text("Connect");
                $("#connect-btn").removeClass("disabled");
                $("#start-stream-btn").addClass("disabled");
                $("#once-btn").addClass("disabled");
                $("#disconnect-btn").addClass("disabled");
           }
       });
        return false; //to remove the button from hreffing
        });
});

//Start Streaming
/*This should probably be error checked somehow, if for example, the server
    fail. */
$(function () {
    $('#start-stream-btn').bind('click',function () {
        console.log("Start stream button go hit.");
        $("#start-stream-btn").text("Waiting...");
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_start"
       }, function(data) {
           $("#start-stream-btn").text("Streaming...");
           $("#stop-stream-btn").removeClass("disabled");
           $("#once-btn").addClass("disabled");
           $("#start-stream-btn").addClass("disabled");
       });
        return false; //to remove the button from hreffing
        });
});


//Stop Streaming
$(function () {
    $('#stop-stream-btn').bind('click',function () {
        console.log("Stop button got hit!");
        $('#stop-stream-btn').text('Waiting...');
        $('#stop-stream-btn').addClass('disabled');
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_stop"
       }, function(data) {
           $('#start-stream-btn').text('Start Stream');
           $('#start-stream-btn').removeClass('disabled');
           $('#once-btn').removeClass('disabled');
           $('#stop-stream-btn').text('Stop Stream');
           $('#chart').html('<img class="img-responsive" src="/image/fig">')
           console.log(data.result)
       });
        return false; //to remove the button from hreffing
        });
});

//Read Once
$(function () {
    $('#once-btn').bind('click',function () {
        console.log('Once button hit!');
        $('#once-btn').text('Waiting...');
        $('#start-stream-btn').addClass('disabeled');
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "once"
       }, function(data) {
           $('#once-btn').text('One Reading');
           $('#start-stream-btn').removeClass('disabeled');
           $("#once-range").text(data.result.range);
           $("#once-cone").text(data.result.cone_force.toFixed(2));
           $("#once-donut").text(data.result.donut_force.toFixed(2));
       });
        return false; //to remove the button from hreffing
        });
});

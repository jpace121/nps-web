/*
  Javascript for range_finder.html
  This should be refactored to something that uses less
  anonymous functions.
*/

//Connect
$(function () {
    $('#connect-btn').bind('click',function () {
        $("connect-btn").text("Connecting...");
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
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_stop"
       }, function(data) {
           var chart = c3.generate({
               bindto: "#chart",
               data: {
                   xs: {
                       'Drop Distance':'distance_t',
                       'Cone Force':'cone_t',
                       'Sleeve Friction':'donut_t',
                   },
                  columns: [
                      ['distance_t', data.result.range_vals.t],
                      ['cone_t', data.result.cone_vals.t],
                      ['donut_t', data.result.donut_vals.t],

                      ['Drop Distance', data.result.donut_vals.d],
                      ['Cone Force', data.result.donut_vals.d],
                      ['Sleeve Friction', data.result.donut_vals.d],

                  ]
                  }
               });
           $('#start-stream-btn').text('Start Stream');
           $('#start-stream-btn').removeClass('disabled');
           $('#once-btn').removeClass('disabled');
           $('#stop-stream-btn').addClass('disabled');
           $('#result').text(data.result);
       });
        return false; //to remove the button from hreffing
        });
});

//Read Once
$(function () {
    $('#once-btn').bind('click',function () {
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

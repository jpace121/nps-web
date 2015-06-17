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
 up chucks.*/
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
    var ctx = $("#chart").get(0).getContext("2d");
    $('#stop-stream-btn').bind('click',function () {
        console.log("Stop button got hit!");
        $.getJSON($SCRIPT_ROOT + '/_get_range_vals',{
            option: "stream_stop"
       }, function(data) {
           var chartData = {
               labels: [" ", " ", " ", " ", " ", " ", " "],
               datasets: [
                   {
                       label: "Cone",
                       data: data.result.cone_vals,
                       fillColor: "rgba(220,220,220,0.2)",
                       strokeColor: "rgba(220,220,220,1)",
                       pointColor: "rgba(220,220,220,1)",
                       pointStrokeColor: "#fff",
                       pointHighlightFill: "#fff",
                       pointHighlightStroke: "rgba(220,220,220,1)"
                       },
                   {
                       label: "Donut",
                       data: data.result.donut_vals,
                       fillColor: "rgba(151,187,205,0.2)",
                       strokeColor: "rgba(151,187,205,1)",
                       pointColor: "rgba(151,187,205,1)",
                       pointStrokeColor: "#fff",
                       pointHighlightFill: "#fff",
                       pointHighlightStroke: "rgba(151,187,205,1)"
                       },
                   {
                       label: "Range",
                       data: data.result.range_vals
                       }
                   ]
               };
           var myLineChart = new Chart(ctx).Line(chartData);
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

$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    //console.log("Got websocket message " + message.data);
    

    var ws_path = ws_scheme + '://' + window.location.host + window.location.pathname;
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);
            



    // Handle incoming messages

    socket.onmessage = function(message) {

        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        if (data.error) {
            alert(data.error);
        return;
        }



        ele.append(
            $("<td></td>").text(data.timestamp)
        )
        ele.append(
            $("<td></td>").text(data.username)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            /*username: $('#username').val(),*/
            message: $('#message').val(),
        }
        socket.send(JSON.stringify(message));
        $("#message").val('').focus();

        return false;
    });
    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    }
});

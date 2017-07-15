$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    
    
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
    
    chatsock.onmessage = function(message) {

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
            $("<td></td>").text(data.handle)
        )
        ele.append(
            $("<td></td>").text(data.message)
        )
        
        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        var message = {
            /*handle: $('#handle').val(),*/
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();

        return false;
    });

    // Says if we joined a room or not by if there's a div for it
    inRoom = function (roomId) {
        return $("#room-" + roomId).length > 0;
    };

    // Room join/leave
    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            $(this).removeClass("joined");
            chatsock.send(JSON.stringify({
                "command": "leave",
                "room": roomId
            }));
        } else {
            // Join room
            $(this).addClass("joined");
            chatsock.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    });
    // Helpful debugging
    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    };
    chatsock.onclose = function () {
        console.log("Disconnected from chat socket");
    }

});
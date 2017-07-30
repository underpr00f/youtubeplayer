$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    
    
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + window.location.pathname);
    


    chatsock.onmessage = function(message) {

        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        var chat = $("#chats")
        var usname = $("div.handle").attr("data-user");
        
        if (data.error) {
            alert(data.error);
        return;
        }
        var fromdb = $(data.history);
                
        //creating array from history
        var arr = [];

        $.each(fromdb, function(key) {
                    
            var mess = "";
            var selfmess = "";
            var alymess = "";
            
            //message from history with editting   
            if (fromdb[key].handle == usname) {
                selfmess += "<img class='sp-profile-img-selfchat' src='" + fromdb[key].avatar + "'>" + "<span class='selfmessages'>" + fromdb[key].messageid + ') ' + fromdb[key].message + "</span>" + "<br>" + "<span class='selfusername'>" + fromdb[key].handle + "</span>" + "<span class='selfdate'>[" + fromdb[key].now + "]</span><br>" ;
                        
            } else {
                alymess += "<img class='sp-profile-img-chat' src='" + fromdb[key].avatar + "'>" + "<span class='message'>" + fromdb[key].messageid + ') ' + fromdb[key].message + "</span>"  + "<br>" + "<span class='username'>" + fromdb[key].handle + "</span>" + "<span class='udate'>[" + fromdb[key].now + "]</span>" + "<span class='clearing'></span>" + "<br>";
                        
            }

            mess = selfmess + alymess
                    
            arr.push(mess); 
                                                        
        });
                        //add new message to array from history
                if (data.messageid === undefined && data.message !== null) {
                    

                    if (data.message) {
                        if (data.username == usname) {
                            arr.unshift("<img class='sp-profile-img-selfchat' src='" + data.avatar + "'>" + "<span class='selfmessages'>" + data.msgid + ') ' + data.message + "</span>" + "<br>" + "<span class='selfusername'>" + data.username + "</span>" + "<span class='selfdate'>[" + data.now + "]</span><br>");
                        } else {
                            arr.unshift("<img class='sp-profile-img-chat' src='" + data.avatar + "'>" + "<span class='message'>" + data.msgid + ') ' + data.message + "</span>" + "<br>" + "<span class='username'>" + data.username + "</span>" + "<span class='udate'>[" + data.now + "]</span><br>" );
                        }
                    
                    }
                } else {
                    arr.push(data.message+data.messageid);
                    
                }
        //check for NaN, remove NaN from array
        function bouncer(arr) {
            return arr.filter( function(v){return !(v !== v);});
        }
        var roomdiv = $("<div class='messages'>"+ bouncer(arr).join(' ') + "</div>");

        roomdiv.scrollTop(roomdiv.prop("scrollHeight"));
        $("#chats").html(roomdiv);

    };


    $("#chatform").on("submit", function(event) {
        var message = {
            "command": "send",
            "room": $("div.chats").attr("data-room-id"),
            /*handle: $('#handle').val(),*/
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();

        return false;
    });

    
    $("a.roomlink").click(function () {
        chatsock.send(JSON.stringify({
            "command": "leave",
            "room": $("div.chats").attr("data-room-id"),
        }));
    });
    // Helpful debugging
    chatsock.onopen = function () {
        console.log("Connected to chat socket");
    };
    chatsock.onclose = function () {
        console.log("Disconnected from chat socket");
    }

});  
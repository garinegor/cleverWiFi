var socket = io.connect(location.origin + ":5000");

socket.on("success", function(msg){
   console.log("complete:\n" + msg);
});

socket.on("fail", function(msg){
   console.log("failed:\n" + msg);
});

function run(command){
   socket.emit("run", {command: command});
}

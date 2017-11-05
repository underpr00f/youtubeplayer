var names   = [];

var nameInput   = document.getElementById("name");

var messageBox  = document.getElementById("display");

function insert ( ) {
 
 names.push( nameInput.value );
   
 clearAndShow();
}

function clearAndShow () {
  // Clear our fields
  
  nameInput.value = "";
  
  
  // Show our output
  messageBox.innerHTML = "";
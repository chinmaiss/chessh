function login(){
    var uname = document.getElementById("nameform").value;
    var pw = document.getElementById("pwform").value;
    document.cookie = "username="+uname + ";  path=/";
    console.log(uname);
}

function create(){
    alert("not implimented; login with name:name and any non empty password")
}
function offline(){
    alert("not implimented; login with name:name and any non empty password")
}

console.log("hello world");
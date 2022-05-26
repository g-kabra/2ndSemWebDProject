const student_btn = document.getElementById("student-btn");
const teacher_btn = document.getElementById("teacher-btn");
const admin_btn = document.getElementById("admin-btn");
const loginBtn = document.querySelectorAll(".login-btn");
const pathSelector = document.getElementById("login-btn-list");
const loginBox = document.getElementById("login-box");
const loginBack = document.getElementById("login-back");
const loginTypeText = document.getElementById("login-type-text");

function fade(element) {
    // var op = 1;  // initial opacity
    // element.style.position = 'absolute';
    // var timer = setInterval(function () {
    //     if (op <= 0.1){
    //         clearInterval(timer);
    //         element.style.display = 'none';
    //     }
    //     element.style.opacity = op;
    //     element.style.filter = 'alpha(opacity=' + op * 100 + ")";
    //     op -= op * 0.1;
    // }, 50);
    element.style.display = 'none';
}

function unfade(element) {
    var op = 0.1;  // initial opacity
    element.style.opacity = op;
    element.style.display = 'flex';
    var timer = setInterval(function () {
        if (op >= 1){
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 10);
}

loginBtn.forEach(btn => {
    btn.addEventListener("click", function(event) {
        console.log(btn);
        fade(pathSelector);
        unfade(loginBack);
        unfade(loginBox);
        loginBack.style.display = 'block';
        if(btn.id == "student-btn"){
            loginTypeText.innerText = "Student's Login";
        }
        if(btn.id == "admin-btn"){
            loginTypeText.innerText = "Admin's Login";
        }
        if(btn.id == "teacher-btn"){
            loginTypeText.innerText = "Teacher's Login";
        }
    });
})

loginBack.addEventListener('click', function() {
    fade(loginBox);
    fade(loginBack);
    unfade(pathSelector);
})


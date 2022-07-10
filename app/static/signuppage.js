const studentbtn = document.getElementById("studentbtn");
const teacherbtn = document.getElementById("teacherbtn");
const adminbtn = document.getElementById("adminbtn");
const teachersignup = document.getElementById("teachersignup");
const studentsignup = document.getElementById("studentsignup");
const adminsignup = document.getElementById("adminsignup");

function fade(element) {
  element.style.display = "none";
}

function unfade(element) {
  var op = 0.1; // initial opacity
  element.style.opacity = op;
  element.style.display = "flex";
  var timer = setInterval(function () {
    if (op >= 1) {
      clearInterval(timer);
    }
    element.style.opacity = op;
    element.style.filter = "alpha(opacity=" + op * 100 + ")";
    op += op * 0.1;
  }, 10);
}

teacherbtn.addEventListener("click", function () {
  fade(studentsignup);
  fade(adminsignup);
  unfade(teachersignup);
});

studentbtn.addEventListener("click", function () {
  fade(teachersignup);
  fade(adminsignup);
  unfade(studentsignup);
});

adminbtn.addEventListener("click", function () {
  fade(teachersignup);
  fade(studentsignup);
  unfade(adminsignup);
});

const addAssignmentForm = document.getElementById("add-assignment-form");
const addAssignmentBtn = document.getElementById("add-assignment");
const removeAddAssignmentForm = document.getElementById("add-assignment-back");

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

addAssignmentBtn.addEventListener("click", function () {
  unfade(addAssignmentForm);
});
removeAddAssignmentForm.addEventListener("click", function () {
  fade(addAssignmentForm);
});

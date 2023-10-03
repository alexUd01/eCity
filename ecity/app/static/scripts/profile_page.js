$(function () {
  // Delete my student's account
  const delStudentButton = document.getElementById("del-student-button");
  if (delStudentButton) {
    delStudentButton.addEventListener('click', function (event) {
      if (!confirm(`Are you sure you want to delete this student's account?\nBe informed that all data related to this account will be completely erased. This action cannot be undone.\n\nDo you want to continue?`)) {
	event.preventDefault();
      }
    });
  }

  // Delete my account
  const delMeButton = document.getElementById("del-me-button");
  if (delMeButton) {
    delMeButton.addEventListener('click', function (event) {
      if (!confirm(`Are you sure you want to delete your account?\nBe informed that all your data will be completely erased. This action cannot be undone.\n\nDo you want to continue?`)) {
	event.preventDefault();
      }
    });
  }
});

$(function () {
  const delExamButtons = document.getElementsByClassName('delete-exam');
  if (delExamButtons) {
    for (delExamButton of delExamButtons) {
      delExamButton.addEventListener('click', function (event) {
	if (!confirm('Are you sure that you want to delete this examination?')) {
	  event.preventDefault();
	}
      });
    }
  }
});

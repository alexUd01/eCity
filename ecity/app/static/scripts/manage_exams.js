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

  const rescheduleExamButtons = document.getElementsByClassName('reschedule-exam');
  if (rescheduleExamButtons) {
    for (rescheduleExamButton of rescheduleExamButtons) {
      rescheduleExamButton.addEventListener('click', function (event) {
	if (!confirm(`Are you sure that you want to reschedule this examination?  All your students' answersheets as well as their scores will be deleted.\n\nDo you want to continue?`)) {
	  event.preventDefault();
	}
      });
    }
  }

});

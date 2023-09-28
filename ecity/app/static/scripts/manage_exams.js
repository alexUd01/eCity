$(function () {
  $('.delete-exam').on('click', function () {
    while (true) {
      resp = prompt('Are you sure that you want to delete this examination? Yes/No');
      if (resp.toLowerCase() === 'yes' || resp.toLowerCase() === 'no') {
	alert(resp);
	break;
      }
    if (resp === "no") {
      // stop execution of this link
      return;
    }
  });
});

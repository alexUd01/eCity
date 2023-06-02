$(function () {
  // Question sect
  $.get('/test_exam/1/', function (data, status) {

    // Define two functions `displayQuestions` and `displayNavBar` to help
    const displayQuestion = function (i, data) {
      // 1-Display Question
      const question = data[i].data
      $('div.question h3#No').text(i+1 + '. ');
      $('div.question h3#Q').text(question);
      // 2-Display Question's options
      const options = data[i].options;
      mapper = { 0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H' }
      for (let j = 0; j < Object.keys(options).length; j++) {
	const v = '<span><input type="radio" name="ans" class="option-item"><b id="' + j + '">A. Loading...</b></span>'
	$('.option-container').append(v);
	$('div span b#' + j).text(' ' + String(mapper[j]) + '.  ' + String(options[mapper[j]]));
      }
    };
    const displayNavBar = function (i) {
      // Display/Hide navigation buttons
      if (i === 0) {
	$('button#prev').css('display', 'none');
	$('button#next').css('margin-left', '36.15em');
      }
      else if (i === data.length - 1) {
	$('button#next').css('display', 'none');
      }
      else {
	$('button#next').css('margin-left', '10em');  // Re-adjust left margin from 36.15em back to 10em
	$('button#next').show();
	$('button#prev').show();
      }
    };
    const clearQuestion = function () {
      $(".option-container").remove('.option-item');
    };

    // Exam is retrieved (Visualization of Execution begins)
    if (status === "success") {
      let i = 0;

      // 1. Landing page
      displayNavBar(i);
      displayQuestion(i, data);

      // 2. Click action on prev buttons
      $('button#prev').on('click', function () {
	clearQuestion();
	if (i !== 0) {
	  i = i - 1;
	}
	displayQuestion(i, data);
	displayNavBar(i);
      });

      // 3. Click action on next buttons
      $('button#next').on('click', function () {
	if (i !== data.length - 1) {
	clearQuestion();
	  i = i + 1;
	}
	displayNavBar(i);
	displayQuestion(i, data);
      });
    }
    else {
      alert('Something seems wrong...\nPlease notify your system administrator.');
    }
  });
});

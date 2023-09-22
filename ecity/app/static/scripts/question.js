$(function () {
  exam_id = globalThis.exam_id;
  user_id = globalThis.user_id;
  // NOTE: Global properties are initialized in the file `./exports.js`.

  // Question sect
  const url = `/get_exam_questions/${exam_id}/`;
  $.get(url, function (data, status) {
    // Define three functions `displayQuestions`, `displayNavBar` and `clearQuestion` to help
    const displayQuestion = function (i, data) {
      // 1-Display Question
      const question = data[i].data;
      $('div.question h3#No').text(i+1 + '. ');
      $('div.question h3#Q').text(question);
      // 2-Display Question's options
      const options = data[i].options;
      mapper = { 0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H' };
      for (let j = 0; j < Object.keys(options).length; j++) {
	const full_text = ' ' + String(mapper[j])+ '.  ' +String(options[mapper[j]]);
	const val = String(mapper[j]);
	const opt = '<span><input type="radio" name="ans" value="'+ val +'"class="option-item"><b id="'+ j +'">A. Loading...</b></span>';
	$('.option-container').append(opt);
	$('div span b#' + j).text(full_text);
      }
      // Update attempted questions on click
      $('span input[type="radio"]').on('click', function () {
	const num = Object.keys(globalThis.ans_sheet.q_and_a).length + 1
	$('h4#attempted').text('QUESTIONS ATTEMPTED:  ' + num);
      });
    };

    const displayNavBar = function (i) {
      // Display/Hide navigation buttons
      if (i === 0) {
	$('button#prev').hide();
	$('button#next').css('margin-left', '36.15em');
      }
      else if (i === data.length - 1) {
	$('button#next').hide();
      }
      else {
	$('button#next').css('margin-left', '10em');  // Re-adjust left margin from 36.15em back to 10em
	$('button#next').show();
	$('button#prev').show();
      }
    };

    // Clear all previouly appended options
    const clearOptions = function () {
      $(".option-container").empty('.option-item');
    };

    // store the just answered question to an object
    const storeData = function (i, data) {
      const question_id = data[i].question_id;
      const val = $("input[type='radio'][name='ans']:checked").val();

      if (val === undefined) {
	alert('Please select an option for the current question.');
	return i - 1;
      }
      globalThis.ans_sheet.q_and_a[question_id] = val;
      return i;
    };


    // Exam is retrieved (Visualization of Execution begins)
    if (status === "success") {
      let i = 0;
      $('h4#attempted').text('QUESTIONS ATTEMPTED: 0');

      // 1. First question
      displayQuestion(i, data);
      displayNavBar(i);

      // 2. Click action on prev button
      $('button#prev').on('click', function () {
	clearOptions();
	if (i !== 0) {
	  i = i - 1;
	}
	displayQuestion(i, data);
	displayNavBar(i);
      });

      // 3. Click action on next button
      $('button#next').on('click', function () {
	i = storeData(i, data);
	clearOptions();
	if (i !== data.length - 1) {
	  i = i + 1;
	}
	displayNavBar(i);
	displayQuestion(i, data);
      });
      // 4. Click action on submit button
      $('button#submit').on('click', function () {
	if (Object.keys(globalThis.ans_sheet.q_and_a).length >= data.length - 1) {  // Check if some questions are unanswered
	  i = storeData(i, data);
	  const val = $("input[type='radio'][name='ans']:checked").val();
	  if (val === undefined) {
	    i = i + 1; // Fixes prev button going 2 questions back
	    console.log('ok'); // Just do nothing (a workaround). Error is already handled by `storeData` above.
	  } else {
	    // All questions have been answered
	    $.post(`/student/${user_id}/submit_exam/`, globalThis.ans_sheet, function (response) {
	      $('form').submit();
	    });
	  }
	} else {
	  alert('You still have unanswered questions.');
	}
      });
    }
    else {
      alert('Something seems wrong...\nPlease notify your system administrator.');
    }
  });
});

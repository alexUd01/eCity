$(function () {
  // The exam answer sheet
  const exam_id = 1;
  const user_id = 4;
  const ans_sheet = { exam_id:exam_id, user_id:user_id, q_and_a:{} };

  // Question sect
  $.get('/test_exam/1/', function (data, status) {
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
	const num = Object.keys(ans_sheet.q_and_a).length + 1
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
      ans_sheet.q_and_a[question_id] = val;
      return i;
    };


    // Exam is retrieved (Visualization of Execution begins)
    if (status === "success") {
      let i = 0;
      $('h4#attempted').text('QUESTIONS ATTEMPTED: 0');

      // 1. Landing page
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
	if (Object.keys(ans_sheet.q_and_a).length >= data.length - 1) {  // Check if some questions are unanswered
	  i = storeData(i, data);
	  const val = $("input[type='radio'][name='ans']:checked").val();
	  if (val === undefined) {
	    i = i + 1; // Fixes prev button going 2 questions back
	    console.log('ok'); // Just do nothing (a workaround). Error is already handled by `storeData` above.
	  } else {
	    // All questions have been answered
	    $.post('/users/'+user_id+'/exams/', ans_sheet, function () {
	      $('form').submit();
	    });
	  }
	} else {
	  alert('You still have unanswered questions.');
	}
      });
      // Create and Manage examination timer
//      $('header').append('<div class="timer-container"><h1 id="timer">THE TIMER</h1></div>');
//      $('div.timer-container').css('width', '11.5em');
//      $('div.timer-container').css('height', '2.8em');
//      $('div.timer-container').css('position', 'absolute');
//      $('div.timer-container').css('right', '0');
//      $('div.timer-container').css('top', '3.2em');
//      $('div.timer-container').css('color', 'white');
//      $('h1#timer').css('margin-left', '1em');
//      $('h1#timer').css('margin-right', '0.3em');
//      $('h1#timer').css('margin-top', '0.2em');
//      $('h1#timer').css('font-size', '1.65em');
//
      let time_allowed = $('h4#time_allowed b').text();
      time_allowed = Number(time_allowed);
      let hours_left = time_allowed > 60 ? time_allowed / 60 : 0;
      let mins_left = time_allowed % 60;
//
//      $('h1#timer').text(hours_left + ':' + mins_left + ':[SECS]');
//      setInterval(function () {
//	if (mins_left - 1 === -1 && hours_left > 0) {
//	  hours_left = hours_left - 1;
//	  mins_left = 59;
//	}
//	$('h1#timer').text(hours_left + ':' + mins_left + ':[SECS]')
//	mins_left = mins_left - 1;
//      }, 60 * 1000);

      // CONFIGURE AUTO SUBMIT FEATURE UPON TIME UP
      setTimeout(function () {
	$.post('/users/' + user_id + '/exams/', ans_sheet, function () {
	  alert('TIMEUP!!!');
	  $('form').submit();
	});
      }, time_allowed*60*1000);
    }
    else {
      alert('Something seems wrong...\nPlease notify your system administrator.');
    }
  });
});

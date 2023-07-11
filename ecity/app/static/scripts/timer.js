$(function() {
  exam_id = globalThis.exam_id;
  user_id = globalThis.user_id;
  ans_sheet = globalThis.ans_sheet; // No need for this

  // Create and Manage examination timer
  $('header').append('<div class="timer-container"><h1 id="timer"><span id="h">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;:&nbsp;<span id="m">&nbsp;&nbsp;</span>&nbsp;:&nbsp;<span id="s">&nbsp;&nbsp;</span></h1></div>');
  $('div.timer-container').css('width', '14vw');
  $('div.timer-container').css('height', '3.1vw');
  $('div.timer-container').css('position', 'absolute');
  $('div.timer-container').css('right', '0');
  $('div.timer-container').css('top', '4.4vw');
  $('div.timer-container').css('color', 'white');
  $('div.timer-container').css('text-align', 'center');
  $('h1#timer').css('font-size', '2.2vw');
  $('h1#timer').css('font-family', 'sans-serif');
  $('h1#timer').css('font-stretch', 'ultra-expanded');
  $('h1#timer').css('font-weight', '900');

  let time_allowed = $('h4#time_allowed b').text();
  time_allowed = Number(time_allowed);

  let hours_left;
  if (time_allowed > 60) {
    hours_left = Math.floor(time_allowed / 60);
  } else if (time_allowed === 60) {
    hours_left = 1;
  } else {
    hours_left = 0;
  }

  let mins_left = time_allowed % 60;
  let secs_left = 0;

  const displayTime = (h, m, s) => {
    [h, m, s] = [h.toString(), m.toString(), s.toString()];
    if (h.length === 1) { h = '0' + h };
    if (m.length === 1) { m = '0' + m };
    if (s.length === 1) { s = '0' + s };
    $('span#h').text(h);
    $('span#m').text(m);
    $('span#s').text(s);
  }

  let first_iter = true;
  const interval = setInterval(function () {
    displayTime(hours_left, mins_left, secs_left);
    if (secs_left === 0) {
      secs_left = mins_left > 0 || first_iter ? 60 : 0;
      mins_left -= 1;
      if (mins_left <= 0) {
	mins_left = hours_left > 0 ? 59 : 0;
	hours_left = hours_left > 0 ? hours_left - 1: 0;
	if (hours_left <= 0 && mins_left <= 0 && secs_left === 0) { // TIMEUP
	  // AUTO SUBMIT UPON TIME UP
	  $.post(`/users/${user_id}/exams/`, globalThis.ans_sheet, function () {
	    alert('TIMEUP');
	    $('form').submit();
	  });
	}
      }
    }
    secs_left -= 1;
  }, 1000);
});

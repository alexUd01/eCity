$(function () {
  const username = $('h4#username').text();
  if (username === "guest") {
    const exam_demo_icon = '<div id="exam-demo"><p>Try out our exam demo <a href="/test_exam">here</a></p></div>';
    $('body').append(exam_demo_icon);
    $('div#exam-demo').css('position', 'fixed');
    $('div#exam-demo').css('bottom', '5vw');
    $('div#exam-demo').css('right', '3vw');
    $('div#exam-demo').css('width', '25vw');
    $('div#exam-demo').css('height', '3vw');
    $('div#exam-demo').css('border-radius', '3vw');
    $('div#exam-demo').css('border', '1px solid #0e688c');
    $('div#exam-demo').css('text-align', 'center');
    $('div#exam-demo').css('padding-top', '0.9vw');
    $('div#exam-demo').css('color', '#0e688c');
    $('div#exam-demo a').css('text-decoration', 'underline dotted');
    $('div#exam-demo a').css('color', 'maroon');
  }
});

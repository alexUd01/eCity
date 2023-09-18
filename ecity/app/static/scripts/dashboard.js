$(function () {
  const username = $('h4#username').text();
  if (username === "guest") {
    const exam_demo_icon = '<div id="exam-demo"><p>Try out our exam demo <a href="/test_exam">here</a></p></div>';
    $('body').append(exam_demo_icon);
    $('div#exam-demo').addId(exam-demo);
  }
});

// Used `globalThis` as a tamporary workaround (imports didn't work)
$(function () {
  globalThis.exam_id = $('span#exam_id').text();
  globalThis.user_id = $('h4#user_id').text().split(' ')[1];
  globalThis.ans_sheet = { exam_id: exam_id, user_id: user_id, q_and_a: {} };
});

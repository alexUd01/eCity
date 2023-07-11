// Used `this` a sa tamporary workaround (imports didn't work)
globalThis.exam_id = 1;
globalThis.user_id = $('h4#user_id').text().split(' ')[1];
globalThis.ans_sheet = { exam_id: exam_id, user_id: user_id, q_and_a: {} };

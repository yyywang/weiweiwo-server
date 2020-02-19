var formContent = document.getElementsByTagName('form')[0];

$('form').validate(function () {
    formContent.submit();
}, {
    validate: [{
        id: 'title',
        prompt: {
            ignore: '请填写作品名称',
            overflow: {
                maxlength: '最多100位'
            }
        }
    }, {
        id: 'author',
        prompt: {
            ignore: '请填写作者',
            overflow: {
                maxlength: '最多50位'
            }
        }
    }]
});
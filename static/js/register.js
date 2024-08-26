function bindEmailCaptchaClick() {
    // 绑定获取验证码按钮的点击事件
    $("#register").click(function (event) {
        var $this = $(this);
        event.preventDefault();

        var email = $("input[name='email']").val();
        var action = $(this).data('action');

        sendEmailCode(email, action);
    });

    // 绑定找回密码按钮的点击事件
    $("#reset_pw").click(function (event) {
        var $this = $(this);
        event.preventDefault();

        var email = $("input[name='email']").val();
        var action = $(this).data('action');

        sendEmailCode(email, action);
    });
}

// 发送请求的通用函数
function sendEmailCode(email, action) {
    $.ajax({
        url: "/register/email",
        method: "POST",
        cache: false,
        data: {
            email: email,
            action: action
        },
        success: function (result) {
            var code = result['code'];
            if (code === 200) {
                alert('nihao');
            } else {
                alert(result['message']);
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function handleFormSubmit(event) {
    event.preventDefault();
    var $form = $(this);
    $.ajax({
        url: $form.attr('action'),
        method: 'POST',
        data: $form.serialize(),
        success: function (result) {
            if (result.code === 400) {
                // alert(result['message'])
                var errorMessages = [];
                $.each(result.errors, function(field, messages) {
                    // 仅添加错误消息，不包括字段名和其他符号
                    messages.forEach(function(message) {
                        errorMessages.push(message);
                    });
                });

                // 显示错误信息
                alert('错误: \n' + errorMessages.join('\n'));
                // 填充表单字段
                $.each(result.form_data, function(key, value) {
                    $form.find(`[name=${key}]`).val(value);
                });
            }
            else {

                window.location.href = result.redirect_url || '/';

            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Error: ", textStatus, errorThrown);
            alert("请求失败，请稍后再试");
        }
    });
}

// 整个网页都加载完毕后再执行的
$(function () {
    bindEmailCaptchaClick();
    // $("form").submit(handleFormSubmit);
    $("form").submit(function (event){
        handleFormSubmit.call($(this), event);
    });
});

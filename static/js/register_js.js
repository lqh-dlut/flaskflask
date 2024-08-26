$(document).ready(function() {
        $('#getcode').click(function() {
            var email = $('#email').val();
            $.post('/register', {email: email, getcode: true}, function(data) {
                $('#message').text(data.message);
                if (data.status === 'success') {
                    $('#email').val(email);
                }
            });
        });

        $('#register').click(function() {
            var username = $('#username').val();
            var email = $('#email').val();
            var qrcode = $('#qrcode').val();
            var password = $('#password').val();
            var passwordRepeat = $('#password_repeat').val();
            $.post('/register', {
                username: username,
                email: email,
                qrcode: qrcode,
                password: password,
                password_repeat: passwordRepeat,
                register: true
            }, function(data) {
                $('#message').text(data.message);
                if (data.status === 'success') {
                    window.location.href = '/login';
                }
            });
        });
    });

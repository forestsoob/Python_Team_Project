const EMAIL_REGEXP = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;

// 이메일 필드 검증 함수
function validateEmailField(form, emailField, emailErrorMessage) {
    const email = form.querySelector('input[name="email"]').value;
    const isEmailValid = EMAIL_REGEXP.test(email);

    emailField.classList.toggle('invalid', !isEmailValid);
    emailErrorMessage.textContent = isEmailValid ? '' : '올바르지 않은 이메일입니다.';
}

// 로그인 폼 처리
const loginForm = document.querySelector('#login-form');
if (loginForm) {
    const emailField = document.querySelector('#email-field');
    const emailErrorMessage = document.querySelector('#email-field .error-message');
    const passwordField = document.querySelector('#password-field');
    const passwordErrorMessage = document.querySelector('#password-field .error-message');

  // 입력 필드 변경 이벤트 핸들러
    loginForm.addEventListener('input', (e) => {
    const input = e.target;

    // 입력된 필드의 name 속성에 따라 검증
    switch (input.name) {
        case 'email': {
        validateEmailField(loginForm, emailField, emailErrorMessage);
        break;
    }
        case 'password': {
        const password = form.querySelector('input[name="password"]').value;
        const isPasswordValid = password.length > 0;

        passwordField.classList.toggle('invalid', !isPasswordValid);
        passwordErrorMessage.textContent = isPasswordValid ? '' : '비밀번호를 입력해 주세요.';
        break;
    }
    default:
        break;
    }
});
}

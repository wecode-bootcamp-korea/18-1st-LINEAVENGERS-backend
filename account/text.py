def message(domain, uidb64, token):
    return f"아래 링크를 클릭해 이메일 인증을 완료해 주세요.\n\n회원가입 링크 : http://{domain}/account/activate/{uidb64}/{token}\n\n감사합니다."
    
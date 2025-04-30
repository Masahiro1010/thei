from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    subject = "【the.i】確認コードのお知らせ"
    message = f"""
    アカウントの登録ありがとうございます！

    以下の確認コードを入力して登録を完了してください：

    【確認コード】：{user.verification_code}

    ※このコードは他人に共有しないでください。
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)
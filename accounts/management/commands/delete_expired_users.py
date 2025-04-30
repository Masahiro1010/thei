from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import CustomUser

class Command(BaseCommand):
    help = '期限切れの仮登録ユーザーを削除します'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_users = CustomUser.objects.filter(
            is_active=False,
            verification_expiry__lt=now
        )
        count = expired_users.count()
        expired_users.delete()
        self.stdout.write(self.style.SUCCESS(f'{count} 件の期限切れユーザーを削除しました'))
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ChangeLog, System, UserProfile

@receiver(post_save, sender=System)
def log_system_change(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    ChangeLog.objects.create(
        user=instance.last_modified_by,
        change_type=action,
        model_name='System',
        record_id=instance.id,
        changeset=f"System '{instance.name}' was {action.lower()}d. Description: {instance.description}"
    )

@receiver(post_delete, sender=System)
def log_system_deletion(sender, instance, **kwargs):
    ChangeLog.objects.create(
        user=instance.last_modified_by,
        change_type='DELETE',
        model_name='System',
        record_id=instance.id,
        changeset=f"System '{instance.name}' was deleted"
    )

@receiver(post_save, sender=UserProfile)
def log_user_profile_change(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    ChangeLog.objects.create(
        user=instance.user,
        change_type=action,
        model_name='UserProfile',
        record_id=instance.id,
        changeset=f"User profile for {instance.user.username} was {action.lower()}d. Role: {instance.role}, Department: {instance.department}"
    )
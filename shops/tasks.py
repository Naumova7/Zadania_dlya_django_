from background_task import background
from django.core.mail import send_mail

@background
def send_shop_email(shop_name):
    send_mail(
        subject="Shop updated",
        message=f"Shop {shop_name} was updated.",
        from_email="[from@example.com](mailto:from@example.com)",
        recipient_list=["[to@example.com](mailto:to@example.com)"],
    )

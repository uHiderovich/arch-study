# from pywebpush import webpush, WebPushException
# from environs import Env

# env = Env()
# env.read_env()

# VAPID_PUBLIC_KEY = env("VAPID_PUBLIC_KEY")
# VAPID_PRIVATE_KEY = env("VAPID_PRIVATE_KEY")

# EMAIL_TEST = env("EMAIL_TEST")


def send_push(subscription: dict, title: str, body: str):
    print(f'subscription = {subscription}')
    print(f'title = {title}')
    print(f'body = {body}')

    # payload = {
    #     "title": title,
    #     "body": body
    # }

    # try:
    #     webpush(
    #         subscription_info=subscription,
    #         data=str(payload),
    #         vapid_private_key=VAPID_PRIVATE_KEY,
    #         vapid_claims={
    #             "sub": f"mailto:{EMAIL_TEST}"
    #         }
    #     )
    # except WebPushException as e:
    #     print("Push failed:", e)
    #     raise

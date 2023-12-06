import argparse
import json
import sys
from typing import TypedDict

from google.cloud import pubsub_v1
from google.oauth2 import service_account


class BannedCountyMessage(TypedDict):
    country: str


def main(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Listen for messages on the subscription
    def callback(message: pubsub_v1.subscriber.message.Message):
        message.ack()
        msg_json: BannedCountyMessage = json.loads(message.data.decode("utf-8"))
        print(f"Request received from banned country: {msg_json['country']}")
        sys.stdout.flush()

    # Block the thread until an exception is raised
    future = subscriber.subscribe(subscription_path, callback=callback)
    print("Listening for messages on subscription...")
    sys.stdout.flush()
    future.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_id",
        help="The ID of the project that owns the subscription",
        required=True,
    )
    parser.add_argument(
        "--subscription_id",
        help="The ID of the Pub/Sub subscription",
        required=True,
    )
    args = parser.parse_args()

    main(args.project_id, args.subscription_id)

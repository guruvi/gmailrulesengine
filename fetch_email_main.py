import sys

from core.fetch_and_store_email import process

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pdm run fetch-emails <user_id>")
        sys.exit(1)
    user_id = sys.argv[1]
    process(user_id=user_id)

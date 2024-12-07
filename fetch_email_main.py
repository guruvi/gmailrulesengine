import sys

from core.fetch_and_store_email import process

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: pdm run fetch-emails <user_id> <page_size> <no_of_pages>")
        sys.exit(1)
    process(
        user_id=sys.argv[1],
        page_size=int(sys.argv[2]) or 10,
        no_of_pages=int(sys.argv[3]) or 1
    )

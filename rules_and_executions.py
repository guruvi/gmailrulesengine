import sys

import rules_config
from core.rules_executions import execute


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: pdm run apply-rules <user_id> <page_size> <number_of_pages>")
        sys.exit(1)
    user_id = sys.argv[1]
    execute(
        user_id=user_id,
        pagee_size=sys.argv[2],
        number_of_pages=sys.argv[3],
        config_dict=rules_config.sample_rule,
    )

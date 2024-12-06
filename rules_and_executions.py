import sys

import rules_config
from core.rules_executions import execute


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pdm run apply-rules <user_id>")
        sys.exit(1)
    user_id = sys.argv[1]
    execute(
        user_id=user_id,
        config_dict=rules_config.sample_rule,
    )

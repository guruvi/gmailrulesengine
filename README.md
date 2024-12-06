# Gmail Rules Engine

A Python project that integrates with the Gmail API to perform rule-based operations on emails.

## Setup

This guide targets macOS for local development and assumes certain prerequisites are installed before setting up the project.

### Pre-requisites
- `make`
- `pdm` (Python Development Master)
- `Python 3.12`

### Local Setup on macOS

1. Clone the repository:
```bash
git clone git@github.com:guruvi/gmailrulesengine.git
cd gmailrulesengine
```

2. Run the following command to install dependencies and set up the project:
#### Caution: Do not to run this setup if you have setup already as this will delete existing data!
```bash
make setup-db
```

3. Install all the required dependencies
```bash
make install
```

4. Verify the setup by running tests:
```bash
make test
```

4. Run fetch emails
```bash
pdm run fetch-emails <email_id>
```

5. Edit the rules_config file under the root rules_config

6. Run the rules engine
```bash
pdm run apply-rules <email_id>
```

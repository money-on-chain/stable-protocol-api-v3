# Stable Protocol API v3 (Multicollateral)

## Warning: This is only for version 3 of the main contracts.

| Project              | Version | V3 | 
|----------------------|---------|----|
| MOC (Money on Chain) | V1      | ❌  |
| ROC (RIF on Chain)   | V3      | ✅  |

API list operations of the users dapp. This is a requirement for [stable-protocol-interface-v2](https://github.com/money-on-chain/stable-protocol-interface-v2), this service list operations of the users.

### Usage

Requirements:

* Python 3.9+
* Mongo DB installed also DB, User & pass created
* [Stable-protocol-indexer-v2](https://github.com/money-on-chain/stable-protocol-indexer-v2)Protocol Indexer installed & Running in the same Mongo DB

```
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database:
copy environments/development/.example.env .env

# Edit .env file and change settings point Mongo DB uris 

# Start the service
uvicorn api.app:app --reload
```

### Interactive API docs

Go to http://localhost:8000/


### Deployed environments


| Environment   | Project   | URL                                    | 
|---------------|-----------|----------------------------------------|
| Testnet       | Flipmoney | https://api-testnet.flipmoney.io/      |
| Mainnet       | Flipmoney | https://api-v2.flipmoney.io/           |
| Testnet       | ROC       | https://api-v2-testnet.rifonchain.com/ |
| Mainnet       | ROC       | https://api-v2.rifonchain.com/         |

### Docker (Recommended)

Build, change path to correct environment

```
docker build -t stable_protocol_api_v2 -f Dockerfile.api .
```

Run

```
docker run -d \
--name stable_protocol_api_v2_roc_mainnet \
--env APP_MONGO_URI=mongodb://localhost:27017 \
--env APP_MONGO_DB=roc_mainnet \
--env BACKEND_CORS_ORIGINS=["*"] \
--env ALLOWED_HOSTS=["*"] \
stable_protocol_api_v2
```

The `/v1/omoc/voting/` endpoints serve the OMoC proposal history from the indexed VotingMachine events, matched by changer address to the MIP documents of the proposal registry ([money-on-chain/proposals-changers](https://github.com/money-on-chain/proposals-changers), `docs/proposals/proposals.json`). The registry and its documents are cached in memory for 5 minutes, and the last good copy is kept if a refresh fails.

- `GOVERNANCE_REGISTRY_URL` — url of `proposals.json`; documents and images are resolved relative to it. Defaults to the `proposals_registry` branch on raw.githubusercontent.com. Set it empty to disable the registry (proposals are then served with `listed: null`).



# Stable Protocol API v3 (Multicollateral)

## Warning: This is only for version 3 of the main contracts.

| Project              | Version | V3 | 
|----------------------|---------|----|
| MOC (Money on Chain) | V1      | ❌  |
| ROC (RIF on Chain)   | V3      | ✅  |

API list operations of the users dapp. This is a requirement for [stable-protocol-interface-v2](https://github.com/money-on-chain/stable-protocol-interface-v2), this service list operations of the users.

### Usage

Requirements:

* Python 3.11+ (the Docker image uses 3.12)
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
| Testnet       | MOC (v1)  | https://api-operations-testnet.moneyonchain.com/ |
| Mainnet       | MOC (v1)  | https://api-operations.moneyonchain.com/ |

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
--env ALLOWED_HOSTS='["api-v2.rifonchain.com"]' \
stable_protocol_api_v2
```

`PROTOCOL_VERSION` (default `2`) is the stable protocol of the deployment's database, which picks the routers served besides OMoC, voting and lending (served by both):

- `2` — MoC v2 deployments (RoC, Flipmoney...), indexed by stable-protocol-indexer-v3: `/v1/operations/` and `/v1/events/`.
- `1` — MoC v1, indexed by stable-protocol-indexer: `/v1/webapp/transactions/list/` and `/v1/stats/`, which replace the stable-protocol-api service. `VENDOR_ADDRESS` and `COMMISSION_SPLITTER_V2` are excluded from the transactions list. The old `/api/v1/...` paths keep working as aliases of `/v1/...`, with a `Deprecation: true` response header.

`ALLOWED_HOSTS` is the `Host` header this backend accepts: set it to the API's own hostname(s) for that environment, never `["*"]` (which disables the check). `/ping` is exempt, so ALB health checks by private IP keep working.

`APP_MONGO_TIMEOUT_MS` (default `20000`) caps every database operation; a query that runs longer returns 503. Keep it below nginx's `proxy_read_timeout` (60s).

The `/v1/omoc/voting/` endpoints serve the OMoC proposal history from the indexed VotingMachine events, matched by changer address to the MIP documents of the proposal registry ([money-on-chain/proposals-changers](https://github.com/money-on-chain/proposals-changers), `docs/proposals/proposals.json`). The registry and its documents are cached in memory for 5 minutes, and the last good copy is kept if a refresh fails.

- `GOVERNANCE_REGISTRY_URL` — url of `proposals.json`; documents and images are resolved relative to it. Defaults to the `main` branch on raw.githubusercontent.com. Set it empty to disable the registry (proposals are then served with `listed: null`).
- `GOVERNANCE_NETWORK` — network the API serves, as named in the registry: `rskMainnet` or `rskTestnet`. The `mips` endpoints only return MIPs with a changer on that network (and only that network's changers); empty returns every MIP. Set in `environments/`. Draft MIPs are never listed.



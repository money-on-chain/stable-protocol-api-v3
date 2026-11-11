# Stable Protocol API v3

Public read-only API of the Money on Chain stable protocols: the users' operations and transactions, the OMoC governance, voting and lending endpoints, and the MoC Liquidity Mining incentives. It is used by the dapps ([stable-protocol-interface](https://github.com/money-on-chain/stable-protocol-interface) and [stable-protocol-interface-v3](https://github.com/money-on-chain/stable-protocol-interface-v3)) and by Grafana for the stats.

It supports both generations of the contracts. Each deployment serves one, picked with `PROTOCOL_VERSION`:

| Project              | Contracts | `PROTOCOL_VERSION` | Indexer |
|----------------------|-----------|--------------------|---------|
| MOC (Money on Chain) | V1        | `1`                | [stable-protocol-indexer](https://github.com/money-on-chain/stable-protocol-indexer) and MoC_Incentive |
| ROC (RIF on Chain)   | V2        | `2` (default)      | [stable-protocol-indexer-v3](https://github.com/money-on-chain/stable-protocol-indexer-v3) |

### Endpoints

Served by every deployment:

- `/v1/omoc/` — OMoC staking, vesting, delay machine and oracle events.
- `/v1/omoc/voting/` — OMoC proposals, votes and MIPs.
- `/v1/lending/` — lending operations.

With `PROTOCOL_VERSION=2` (V2 contracts):

- `/v1/operations/` and `/v1/events/` — the users' operations and the protocol events.

With `PROTOCOL_VERSION=1` (MoC V1 contracts):

- `/v1/webapp/transactions/list/` — the users' transactions, as JSON or as a text file (`format=text`). `VENDOR_ADDRESS` and `COMMISSION_SPLITTER_V2` are excluded from the list.
- `/v1/stats/` — volume, transaction and top transactor stats, as JSON or text.
- `/v1/incentives/` (`balance/{address}`, `claims/{address}`, `agent/`) — the MoC Liquidity Mining rewards of MoC_Incentive. The `mocin_*` collections are read from `APP_MONGO_DB`, or from `INCENTIVES_MONGO_DB` on the same server when set.

This API replaced the old MoC V1 services (stable-protocol-api, and MoC_Incentive's miniwebservice), and keeps their paths working as aliases, with a `Deprecation: true` response header: `/api/v1/...` is served as `/v1/...`, and `/balance/...`, `/claims/...` and `/agent` as `/v1/incentives/...`. The dapps need no changes.

### Usage

Requirements:

* Python 3.11+ (the Docker image uses 3.12)
* MongoDB, with the database, user and password created
* The indexer of the deployment's contracts (see the table above), running on the same database

```
# Install the requirements:
pip install -r requirements.txt

# Configure the location of your MongoDB database, starting from an example:
cp environments/development/.roc-development.env .env

# Edit .env: set APP_MONGO_URI and APP_MONGO_DB, and PROTOCOL_VERSION=1 for a MoC V1 database

# Start the service
uvicorn api.app:app --reload
```

### Interactive API docs

Go to http://localhost:8000/ (disabled with `DOCS_ENABLED=false`).


### Deployed environments

| Environment   | Project   | URL                                              |
|---------------|-----------|--------------------------------------------------|
| Testnet       | ROC       | https://api-v2-testnet.rifonchain.com/           |
| Mainnet       | ROC       | https://api-v2.rifonchain.com/                   |
| Testnet       | MOC (V1)  | https://api-operations-testnet.moneyonchain.com/ |
| Testnet       | MOC (V1)  | https://moc-incentives-testnet.moneyonchain.com/ |
| Mainnet       | MOC (V1)  | https://api-operations.moneyonchain.com/         |
| Mainnet       | MOC (V1)  | https://moc-incentives.moneyonchain.com/         |

Each MoC environment is a single service: both its hostnames point to it.

The settings of each environment are in `environments/production/`. `aws_api_build_and_push.sh -e <environment>` builds the image and pushes it to ECR (`moc_testnet`, `moc_mainnet`, `roc_testnet`, `roc_mainnet`).

### Docker (Recommended)

Build

```
docker build -t stable_protocol_api_v2 -f Dockerfile.api .
```

Run

```
docker run -d \
--name stable_protocol_api_v2_roc_mainnet \
--env APP_MONGO_URI=mongodb://localhost:27017 \
--env APP_MONGO_DB=roc_mainnet \
--env EDGE_HEADERS=true \
--env ALLOWED_HOSTS='["api-v2.rifonchain.com"]' \
stable_protocol_api_v2
```

For a MoC V1 deployment, also set `PROTOCOL_VERSION=1`, and `VENDOR_ADDRESS` and `COMMISSION_SPLITTER_V2` (see `environments/production/moc-*.env`).

### Settings

`PROTOCOL_VERSION` (default `2`) is the contracts of the deployment's database, which pick the endpoints served besides OMoC, voting and lending (see [Endpoints](#endpoints)).

`EDGE_HEADERS=true` makes the API send the CORS, security and `Cache-Control` headers itself. Set it on deployments served straight from the load balancer, with rate limiting and caching done by Cloudflare. Leave it unset on a deployment still behind the old nginx container, which sends the same headers: browsers reject a doubled `Access-Control-Allow-Origin`.

`ALLOWED_HOSTS` is the `Host` header this backend accepts: set it to the API's own hostname(s) for that environment, never `["*"]` (which disables the check). `/ping` is exempt, so ALB health checks by private IP keep working.

`APP_MONGO_TIMEOUT_MS` (default `20000`) caps every database operation; a query that runs longer returns 503. Keep it below the load balancer's idle timeout (60s).

The `/v1/omoc/voting/` endpoints serve the OMoC proposal history from the indexed VotingMachine events, matched by changer address to the MIP documents of the proposal registry ([money-on-chain/proposals-changers](https://github.com/money-on-chain/proposals-changers), `docs/proposals/proposals.json`). The registry and its documents are cached in memory for 5 minutes, and the last good copy is kept if a refresh fails.

- `GOVERNANCE_REGISTRY_URL` — url of `proposals.json`; documents and images are resolved relative to it. Defaults to the `main` branch on raw.githubusercontent.com. Set it empty to disable the registry (proposals are then served with `listed: null`).
- `GOVERNANCE_NETWORK` — network the API serves, as named in the registry: `rskMainnet` or `rskTestnet`. The `mips` endpoints only return MIPs with a changer on that network (and only that network's changers); empty returns every MIP. Set in `environments/`. Draft MIPs are never listed.

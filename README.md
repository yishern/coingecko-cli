# CoinGecko CLI

A command line interface (CLI) to browse [CoinGecko](https://coingecko.com)'s data in the terminal. Data provided by [CoinGecko](https://coingecko.com).

## Requirements

Python 3.7 and above

## Installation

```bash
    pip install git+https://github.com/yishern/coingecko-cli
```

## Usage

<!-- trunk-ignore(markdownlint/MD001) -->

#### Cryptocurrency prices

```bash
  cg market
```

| Option       | Short | Type      | Description                           |
| :----------- | :---- | :-------- | :------------------------------------ |
| `--page`     | `-p`  | `integer` | Page through results [default: 1]     |
| `--per-page` | `-pp` | `integer` | Total results per page [default: 100] |
| `--web`      | `-w`  |           | Open in web browser                   |

#### Token historical market data

```bash
  cg token -t ethereum
```

OR (for autocompletion)

```bash
  cg token -t eth[TAB][TAB]
```

| Option    | Short | Type      | Description                                                    |
| :-------- | :---- | :-------- | :------------------------------------------------------------- |
| `--token` | `-t`  | `integer` | **Required**. Id of token (bitcoin, ethereum, etc)             |
| `--days`  | `-d`  | `integer` | Data up to number of days ago (e.g. 1,14,30,max) [default: 30] |
| `--web`   | `-w`  |           | Open in web browser                                            |

#### Sync (Cache tokens locally for `token` command autocompletion)

```bash
  cg sync
```

#### Install completion for `token` command

```bash
  cg --install-completion
```

## Contributing

```bash
# Clone the repository
git clone https://github.com/yishern/coingecko-cli
cd coingecko-cli

# We recommend using a virtual environment
poetry install

# Make your changes...
...

# Run linter and formatters
./trunk check --all
./trunk fmt --all
```

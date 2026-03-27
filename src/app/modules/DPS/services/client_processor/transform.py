import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import requests


DEFAULT_PORTFOLIO_PATH = Path(__file__).resolve().parent / "portfolio.csv"
DEFAULT_ISIN_CACHE_PATH = Path(__file__).resolve().parent / "isin_to_ticker.json"
DEFAULT_HNW_AUM_THRESHOLD_AED = 10_000_000
OPENFIGI_URL = "https://api.openfigi.com/v3/mapping"
OPENFIGI_BATCH_SIZE = 10
OPENFIGI_BATCH_SLEEP_SECONDS = 5
OPENFIGI_TIMEOUT_SECONDS = 30


@dataclass
class ClientProfile:
    client_id: str
    client_name: str
    client_type: str
    client_segment: str
    client_segment_reason: str
    mandate: str
    total_aum_aed: float
    asset_types: list[str]
    asset_subtypes: list[str]
    asset_classifications: list[str]
    currencies: list[str]
    isins: list[str]
    asset_ids: list[str]
    asset_descriptions: list[str]
    classification_weights: dict[str, float]
    asset_type_weights: dict[str, float]
    ticker_symbols: list[str] = field(default_factory=list)
    query: str = field(default="")
    tags_of_interest: list[str] = field(default_factory=list)


def load_portfolio_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Portfolio CSV not found at {path}")
    print("Portfolios loaded")
    return pd.read_csv(path)


def build_client_documents(
    portfolio_df: pd.DataFrame,
    cache_path: Path = DEFAULT_ISIN_CACHE_PATH,
    hnw_aum_threshold_aed: float = DEFAULT_HNW_AUM_THRESHOLD_AED,
) -> list[dict]:
    profiles = build_all_client_profiles(
        portfolio_df,
        hnw_aum_threshold_aed=hnw_aum_threshold_aed,
    )
    all_isins = list({isin for profile in profiles.values() for isin in profile.isins})
    isin_ticker_map = build_isin_ticker_map(all_isins, cache_path=cache_path)
    attach_ticker_symbols(profiles, isin_ticker_map)
    print("Client Portfolio Processing Complete!")
    return [client_profile_to_document(profile) for profile in profiles.values()]


def build_isin_ticker_map(
    isins: list[str],
    cache_path: Path = DEFAULT_ISIN_CACHE_PATH,
) -> dict[str, str]:
    if cache_path.exists():
        cached = json.loads(cache_path.read_text())
        missing = [isin for isin in isins if isin not in cached]
        if not missing:
            return cached
        isins = missing
    else:
        cached = {}

    mapping: dict[str, str] = {}
    for index in range(0, len(isins), OPENFIGI_BATCH_SIZE):
        batch = isins[index:index + OPENFIGI_BATCH_SIZE]
        jobs = [{"idType": "ID_ISIN", "idValue": isin} for isin in batch]
        response = requests.post(
            OPENFIGI_URL,
            json=jobs,
            headers={"Content-Type": "application/json"},
            timeout=OPENFIGI_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        for isin, result in zip(batch, response.json()):
            for hit in result.get("data", []):
                ticker = hit.get("ticker")
                if ticker:
                    mapping[isin] = str(ticker).upper()
                    break
        if index + OPENFIGI_BATCH_SIZE < len(isins):
            time.sleep(OPENFIGI_BATCH_SLEEP_SECONDS)

    merged = {**cached, **mapping}
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(merged, indent=2))
    print("ISIN mappings completed")
    return merged


def attach_ticker_symbols(
    profiles: dict[str, ClientProfile],
    isin_ticker_map: dict[str, str],
) -> None:
    for profile in profiles.values():
        profile.ticker_symbols = sorted(
            {
                isin_ticker_map[isin]
                for isin in profile.isins
                if isin in isin_ticker_map and isin_ticker_map[isin]
            }
        )


def client_profile_to_document(profile: ClientProfile) -> dict:
    return {
        "id": profile.client_id,
        "client_id": profile.client_id,
        "client_name": profile.client_name,
        "client_type": profile.client_type,
        "client_segment": profile.client_segment,
        "client_segment_reason": profile.client_segment_reason,
        "mandate": profile.mandate,
        "total_aum_aed": profile.total_aum_aed,
        "asset_types": profile.asset_types,
        "asset_subtypes": profile.asset_subtypes,
        "asset_classifications": profile.asset_classifications,
        "currencies": profile.currencies,
        "isins": profile.isins,
        "ticker_symbols": profile.ticker_symbols,
        "asset_ids": profile.asset_ids,
        "asset_descriptions": profile.asset_descriptions,
        "classification_weights": profile.classification_weights,
        "asset_type_weights": profile.asset_type_weights,
        "query": profile.query,
        "tags_of_interest": profile.tags_of_interest,
    }


def build_client_profile(
    df: pd.DataFrame,
    *,
    hnw_aum_threshold_aed: float = DEFAULT_HNW_AUM_THRESHOLD_AED,
) -> ClientProfile:
    assert df["Client No."].nunique() == 1, "DataFrame must contain exactly one client."

    row0 = df.iloc[0]
    client_id = str(int(row0["Client No."]))
    client_name = str(row0["Client Name"])
    client_type = str(row0["Client Type"])
    mandate = str(row0["Mandate"])
    total_aum = float(df[" Market Value AED "].sum())
    client_segment, client_segment_reason = _derive_client_segment(
        total_aum_aed=total_aum,
        hnw_aum_threshold_aed=hnw_aum_threshold_aed,
    )

    asset_types = sorted(df["Asset Type"].dropna().unique().tolist())
    asset_subtypes = sorted(df["Asset Subtype"].dropna().unique().tolist())
    asset_classifications = sorted(df["Asset Classification"].dropna().unique().tolist())
    currencies = sorted(df["CCY"].dropna().unique().tolist())
    isins = sorted(df["ISIN"].dropna().unique().tolist())
    asset_ids = sorted(df["Asset ID"].astype(str).unique().tolist())
    asset_descriptions = df["Asset Description"].dropna().unique().tolist()

    aum_by_classification = (
        df[df[" Market Value AED "] > 0]
        .groupby("Asset Classification")[" Market Value AED "]
        .sum()
    )
    classification_weights = {
        key: round(float(value) / total_aum, 4)
        for key, value in aum_by_classification.items()
        if pd.notna(key) and total_aum > 0
    }

    aum_by_type = (
        df[df[" Market Value AED "] > 0]
        .groupby("Asset Type")[" Market Value AED "]
        .sum()
    )
    asset_type_weights = {
        key: round(float(value) / total_aum, 4)
        for key, value in aum_by_type.items()
        if pd.notna(key) and total_aum > 0
    }

    tags_of_interest = _derive_tags(
        asset_classifications=asset_classifications,
        asset_types=asset_types,
        currencies=currencies,
    )
    query = _build_query(
        client_name=client_name,
        client_type=client_type,
        mandate=mandate,
        asset_classifications=asset_classifications,
        asset_descriptions=asset_descriptions,
        classification_weights=classification_weights,
        asset_type_weights=asset_type_weights,
        currencies=currencies,
        total_aum_aed=total_aum,
    )
    print(f"Client Profile {client_id} built")
    return ClientProfile(
        client_id=client_id,
        client_name=client_name,
        client_type=client_type,
        client_segment=client_segment,
        client_segment_reason=client_segment_reason,
        mandate=mandate,
        total_aum_aed=round(total_aum, 2),
        asset_types=asset_types,
        asset_subtypes=asset_subtypes,
        asset_classifications=asset_classifications,
        currencies=currencies,
        isins=isins,
        asset_ids=asset_ids,
        asset_descriptions=asset_descriptions,
        classification_weights=classification_weights,
        asset_type_weights=asset_type_weights,
        tags_of_interest=tags_of_interest,
        query=query,
    )


def build_all_client_profiles(
    df: pd.DataFrame,
    *,
    hnw_aum_threshold_aed: float = DEFAULT_HNW_AUM_THRESHOLD_AED,
) -> dict[str, ClientProfile]:
    profiles = {}
    for _, group in df.groupby("Client No."):
        profile = build_client_profile(
            group.reset_index(drop=True),
            hnw_aum_threshold_aed=hnw_aum_threshold_aed,
        )
        profiles[profile.client_id] = profile
    return profiles


def _derive_client_segment(
    *,
    total_aum_aed: float,
    hnw_aum_threshold_aed: float,
) -> tuple[str, str]:
    threshold = max(float(hnw_aum_threshold_aed), 0.0)
    if total_aum_aed >= threshold:
        return "hnw", f"total_aum_aed>={threshold:.2f}"
    return "retail", f"total_aum_aed<{threshold:.2f}"


def _derive_tags(
    asset_classifications: list[str],
    asset_types: list[str],
    currencies: list[str],
) -> list[str]:
    tags = set()

    classification_tag_map = {
        "Equities": ["EQUITY MARKETS", "STOCK MARKET", "SHARE PRICE MOVEMENT"],
        "Fixed Income": ["BOND MARKETS", "INTEREST RATE CHANGES", "CREDIT EVENTS", "YIELD CURVE"],
        "Real Estate": ["REAL ESTATE", "REIT", "PROPERTY MARKET", "DIVIDEND PAYMENTS"],
        "Alternatives": ["ALTERNATIVE INVESTMENTS", "STRUCTURED PRODUCTS", "HEDGE FUNDS"],
        "Commodities": ["COMMODITIES", "RAW MATERIALS", "ENERGY MARKETS", "METALS"],
        "Multi Assets": ["MULTI-ASSET", "PORTFOLIO REBALANCING", "ASSET ALLOCATION"],
    }
    for classification in asset_classifications:
        tags.update(classification_tag_map.get(classification, []))

    asset_type_tag_map = {
        "EQUITY": ["IPO", "STOCK SPLIT", "BUYBACK", "DIVIDEND"],
        "FUNDS": ["FUND FLOWS", "NAV", "ETF", "INDEX TRACKING"],
        "BOND": ["BOND ISSUANCE", "DEFAULT RISK", "MATURITY", "COUPON"],
        "FIX_INCOME": ["FIXED INCOME", "DURATION RISK", "SPREAD WIDENING"],
        "REIT": ["REAL ESTATE", "RENTAL YIELD", "PROPERTY VALUATION"],
        "ALTERNATIV": ["VOLATILITY", "DERIVATIVES", "OPTIONS"],
        "CASH": [],
        "CFTD": [],
    }
    for asset_type in asset_types:
        tags.update(asset_type_tag_map.get(asset_type, []))

    currency_tag_map = {
        "EUR": ["EURO ZONE", "ECB POLICY", "EUROPEAN MARKETS"],
        "USD": ["US MARKETS", "FED POLICY", "DOLLAR STRENGTH"],
        "GBP": ["UK MARKETS", "BOE POLICY"],
        "JPY": ["JAPAN MARKETS", "BOJ POLICY", "YEN"],
        "CHF": ["SWISS MARKETS", "SNB POLICY"],
        "AUD": ["AUSTRALIA MARKETS", "RBA POLICY"],
        "SGD": ["SINGAPORE MARKETS", "MAS POLICY"],
        "CNY": ["CHINA MARKETS", "PBOC POLICY", "YUAN"],
        "HKD": ["HONG KONG MARKETS"],
    }
    for currency in currencies:
        tags.update(currency_tag_map.get(currency, []))

    return sorted(tags)


def _build_query(
    client_name: str,
    client_type: str,
    mandate: str,
    asset_classifications: list[str],
    asset_descriptions: list[str],
    classification_weights: dict[str, float],
    asset_type_weights: dict[str, float],
    currencies: list[str],
    total_aum_aed: float,
) -> str:
    parts = [
        f"{client_name} is a {client_type.lower()} client with an {mandate.lower().replace('-', ' ')} mandate."
    ]

    aum_m = total_aum_aed / 1_000_000
    if aum_m >= 1:
        parts.append(f"Total portfolio value is approximately {aum_m:.1f} million AED.")
    else:
        aum_k = total_aum_aed / 1_000
        parts.append(f"Total portfolio value is approximately {aum_k:.0f} thousand AED.")

    if classification_weights:
        meaningful = {key: value for key, value in classification_weights.items() if value >= 0.01}
        sorted_cls = sorted(meaningful.items(), key=lambda item: item[1], reverse=True)
        allocation_parts = [f"{int(weight * 100)}% {classification}" for classification, weight in sorted_cls]
        parts.append(f"The portfolio is allocated across: {', '.join(allocation_parts)}.")
    elif asset_type_weights:
        dominant = max(asset_type_weights, key=asset_type_weights.get)
        parts.append(f"The portfolio is primarily held in {_asset_type_label(dominant)}.")

    foreign_ccys = [currency for currency in currencies if currency != "AED"]
    if foreign_ccys:
        parts.append(f"The client has foreign currency exposure in {', '.join(foreign_ccys)}.")
    else:
        parts.append("The client holds assets in AED only.")

    real_assets = [
        description
        for description in asset_descriptions
        if not description.startswith("AL-")
        and not description.startswith("MX-")
        and description.strip() != "Client Fixed Term Deposit"
    ]
    if real_assets:
        options = [description for description in real_assets if _looks_like_option(description)]
        funds = [description for description in real_assets if _looks_like_fund(description)]
        bonds = [description for description in real_assets if _looks_like_bond(description) and description not in funds]
        equities = [
            description
            for description in real_assets
            if description not in options + funds + bonds and _looks_like_equity(description)
        ]
        other = [
            description
            for description in real_assets
            if description not in options + funds + bonds + equities
        ]

        if equities:
            parts.append(f"Key equity holdings include: {', '.join(equities[:8])}.")
        if bonds:
            parts.append(f"Fixed income positions include: {', '.join(bonds[:5])}.")
        if funds:
            parts.append(f"Fund and structured vehicle positions include: {', '.join(funds[:5])}.")
        if options:
            parts.append(f"Derivatives and options positions: {', '.join(options)}.")
        if other:
            parts.append(f"Other holdings: {', '.join(other[:5])}.")
    else:
        parts.append(
            "The client holds primarily cash and fixed term deposits with no active equity or bond positions."
        )

    if classification_weights:
        dominant_classification = max(classification_weights, key=classification_weights.get)
        dominant_weight = classification_weights[dominant_classification]
        if dominant_weight >= 0.7:
            profile_description = f"heavily concentrated in {dominant_classification.lower()}"
        elif dominant_weight >= 0.4:
            profile_description = f"primarily focused on {dominant_classification.lower()}"
        else:
            profile_description = "broadly diversified across asset classes"
        parts.append(f"The investment profile is {profile_description}.")

    return " ".join(parts)


_ASSET_TYPE_LABELS = {
    "CASH": "cash",
    "CFTD": "cash and fixed term deposits",
    "EQUITY": "equities",
    "FIX_INCOME": "fixed income",
    "FUNDS": "funds",
    "REIT": "real estate investment trusts",
    "ALTERNATIV": "alternative investments",
    "BOND": "bonds",
}


def _asset_type_label(asset_type: str) -> str:
    return _ASSET_TYPE_LABELS.get(asset_type, asset_type.lower().replace("_", " "))


_BOND_CORP_PATTERN = re.compile(r"\b\d+(\.\d+)?\s+\d{2}/\d{2}/\d{2,4}\s+CORP$")
_BOND_FRACTION_PATTERN = re.compile(r"\b\d+\s+\d+/\d+\b")
_BOND_DECIMAL_COUPON = re.compile(r"\b\d{1,2}\.\d{1,4}\b")
_BOND_INTEGER_COUPON = re.compile(r"\b(BHCCN|ASTONM|SAGLEN|XRX|OB|HTZ|ARADAD)\s+\d{1,2}\s+\d{2}/\d{2}/\d{2,4}$")
_COMPANY_SUFFIXES = re.compile(r"\b(INC|AG|SE|SA|PLC|LTD|LLC|NV|BV|SPA|ASA|CORP|NYRT|GROUP)\.?$", re.IGNORECASE)
_FUND_KEYWORDS = [
    "FUND",
    "ETF",
    "UCITS",
    "SICAV",
    "RAIF",
    "PORTFO",
    "CAPITAL",
    "DEBT",
    "BOND FUND",
    "RENTENSTRATEGIE",
    "WELTZINS",
    "PHYSICAL",
    "VECTORS",
    "ISHARES",
    "VANECK",
    "WISDOMTREE",
    "XTRACKERS",
    "SHS ",
    "SHS MAN",
    "CONVERTIB",
    "FIN.DEBT",
    "GROUPAMA",
]
_OPTION_KEYWORDS = ["C100", "C195", "P100", "OPTION"]


def _looks_like_option(description: str) -> bool:
    description_upper = description.upper()
    return any(keyword in description_upper for keyword in _OPTION_KEYWORDS)


def _looks_like_fund(description: str) -> bool:
    description_upper = description.upper()
    return any(keyword in description_upper for keyword in _FUND_KEYWORDS)


def _looks_like_bond(description: str) -> bool:
    if _BOND_FRACTION_PATTERN.search(description):
        return True
    if _BOND_DECIMAL_COUPON.search(description):
        return True
    if _BOND_CORP_PATTERN.search(description):
        return True
    if _BOND_INTEGER_COUPON.search(description):
        return True
    if "PERP" in description or "FLOAT" in description:
        return True
    return False


def _looks_like_equity(description: str) -> bool:
    words = description.strip().split()
    if len(words) < 2:
        return False
    if words[0][0].isdigit():
        return False
    if _COMPANY_SUFFIXES.search(description):
        return True
    return all(character.isalpha() or character in " .+&/-" for character in description)

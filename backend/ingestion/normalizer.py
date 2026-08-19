"""Canonical Ingestion & Normalization Layer for AuditVector."""

from decimal import Decimal, InvalidOperation
from typing import Dict, Any, List, Optional
import datetime
import uuid
from ..models.financial_event import FinancialEvent, OrderSide


class NormalizationError(Exception):
    pass


class IngestionNormalizer:
    """Normalizes heterogeneous trade dictionaries into canonical FinancialEvent records."""
    VERSION = "v1.2.0"

    # Field aliases
    QTY_ALIASES = ["quantity", "qty", "size", "amount", "volume", "contracts", "filled_qty", "units"]
    PRICE_ALIASES = ["price", "fill_price", "rate", "exec_price", "trade_price", "avg_price"]
    FEE_ALIASES = ["fee", "commission", "trading_fee", "cost", "fee_amount", "charges"]
    FEE_CURRENCY_ALIASES = ["fee_currency", "commission_currency", "fee_asset", "currency"]
    SIDE_ALIASES = ["side", "order_side", "action", "type", "direction"]
    SYMBOL_ALIASES = ["symbol", "pair", "ticker", "instrument", "asset"]
    TIME_ALIASES = ["timestamp", "time", "date", "datetime", "created_at", "exec_time", "ts"]
    ID_ALIASES = ["id", "event_id", "trade_id", "order_id", "fill_id", "exec_id"]
    POSITION_ALIASES = ["position_id", "pos_id", "trade_group", "batch_id"]

    @classmethod
    def _find_field(cls, row: Dict[str, Any], aliases: List[str]) -> Optional[Any]:
        # Exact match or lowercase stripped match
        cleaned_row = {str(k).strip().lower(): v for k, v in row.items()}
        for alias in aliases:
            if alias.lower() in cleaned_row:
                val = cleaned_row[alias.lower()]
                if val is not None and str(val).strip() != "":
                    return val
        return None

    @classmethod
    def normalize_row(cls, row: Dict[str, Any], source: str = "", default_symbol: str = "DEFAULT") -> FinancialEvent:
        """Converts a raw dictionary into a canonical FinancialEvent."""
        # 1. Identifier
        raw_id = cls._find_field(row, cls.ID_ALIASES)
        event_id = str(raw_id) if raw_id is not None else str(uuid.uuid4())

        # 2. Timestamp
        raw_time = cls._find_field(row, cls.TIME_ALIASES)
        timestamp_str = cls._parse_timestamp(raw_time)

        # 3. Symbol
        raw_sym = cls._find_field(row, cls.SYMBOL_ALIASES)
        symbol = str(raw_sym).upper().strip() if raw_sym else default_symbol

        # 4. Side
        raw_side = cls._find_field(row, cls.SIDE_ALIASES)
        side = cls._parse_side(raw_side)

        # 5. Quantity
        raw_qty = cls._find_field(row, cls.QTY_ALIASES)
        if raw_qty is None:
            raise NormalizationError(f"Missing quantity field in record: {row}")
        try:
            qty = abs(Decimal(str(raw_qty).replace(",", "").strip()))
        except InvalidOperation as e:
            raise NormalizationError(f"Invalid quantity value '{raw_qty}': {e}")

        # 6. Price
        raw_price = cls._find_field(row, cls.PRICE_ALIASES)
        if raw_price is None:
            raise NormalizationError(f"Missing price field in record: {row}")
        try:
            price = Decimal(str(raw_price).replace(",", "").replace("$", "").strip())
        except InvalidOperation as e:
            raise NormalizationError(f"Invalid price value '{raw_price}': {e}")

        # 7. Fee
        raw_fee = cls._find_field(row, cls.FEE_ALIASES)
        fee = Decimal("0.0")
        if raw_fee is not None:
            try:
                fee = Decimal(str(raw_fee).replace(",", "").replace("$", "").strip())
            except InvalidOperation:
                fee = Decimal("0.0")

        # 8. Fee Currency
        raw_fee_curr = cls._find_field(row, cls.FEE_CURRENCY_ALIASES)
        fee_curr = str(raw_fee_curr).upper().strip() if raw_fee_curr else "USD"

        # 9. Position ID / Trade ID
        pos_id = cls._find_field(row, cls.POSITION_ALIASES)
        trade_id = cls._find_field(row, ["trade_id", "tradeId", "id"])

        return FinancialEvent(
            event_id=event_id,
            timestamp=timestamp_str,
            symbol=symbol,
            side=side,
            quantity=qty,
            price=price,
            fee=fee,
            fee_currency=fee_curr,
            position_id=str(pos_id) if pos_id else None,
            trade_id=str(trade_id) if trade_id else None,
            source=source,
            metadata=row
        )

    @classmethod
    def _parse_side(cls, val: Any) -> OrderSide:
        if val is None:
            return OrderSide.BUY
        s = str(val).strip().upper()
        if s in ["BUY", "B", "LONG", "1", "ENTRY_LONG", "COVER"]:
            return OrderSide.BUY
        if s in ["SELL", "S", "SHORT", "-1", "ENTRY_SHORT", "EXIT"]:
            return OrderSide.SELL
        return OrderSide.BUY

    @classmethod
    def _parse_timestamp(cls, val: Any) -> str:
        if val is None:
            return datetime.datetime.now(datetime.timezone.utc).isoformat()
        s = str(val).strip()
        # UNIX timestamp in seconds or ms
        if s.isdigit():
            ts = int(s)
            if ts > 1e11:  # ms
                ts = ts / 1000.0
            return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).isoformat()
        try:
            # Try ISO format
            dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
            return dt.isoformat()
        except Exception:
            pass
        # Common formats
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%d-%m-%Y %H:%M:%S"):
            try:
                dt = datetime.datetime.strptime(s, fmt).replace(tzinfo=datetime.timezone.utc)
                return dt.isoformat()
            except ValueError:
                continue
        return s

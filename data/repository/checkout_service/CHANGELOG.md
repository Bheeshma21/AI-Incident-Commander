# Checkout Service Change History

## v1.8.3 - 2026-08-16

### Changes

- Refactored database connection handling.
- Improved checkout database performance.
- Simplified error handling in the checkout flow.

### Files Changed

- `app/db.py`
- `app/checkout.py`

### Notes

The database connection lifecycle was changed as part of the performance refactor.

---

## v1.8.2 - 2026-08-15

### Changes

- Improved payment timeout handling.
- Updated checkout validation.

### Files Changed

- `app/checkout.py`
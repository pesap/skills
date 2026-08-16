# API documentation

Document the public contract, not implementation details.

For each API surface, cover only applicable fields:

- purpose, audience, and stability;
- inputs, types, defaults, constraints, and required values;
- outputs, state changes, side effects, and idempotency;
- errors, failure conditions, retries, and partial-success behavior;
- authentication, permissions, pagination, limits, compatibility, and
  versioning;
- one realistic common example and one important edge case.

Generate or validate details from source contracts when tooling exists. Do not
manually duplicate generated reference material unless the source contract is
updated in the same change. Verify names, signatures, defaults, and examples
against code and tests before delivery.

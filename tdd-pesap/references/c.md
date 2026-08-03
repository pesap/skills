# C testing

Apply the core behavior-first doctrine through stable C APIs and explicit seams.

- Keep tests focused on observable API behavior and state transitions.
- Use function pointers or adapter seams for external boundaries.
- Avoid testing private layout or incidental call sequences unless they are part
  of a documented contract.
- Use sanitizers and static analysis where available, especially ASan, UBSan,
  and clang-tidy.
- Keep ownership, lifetime, and cleanup behavior visible in test cases.

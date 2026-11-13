# Engineering decisions
- React/Vite separates presentation from API services.
- FastAPI/Pydantic validates input at the API boundary and generates OpenAPI docs.
- SQLite simplifies local setup; migrate to managed PostgreSQL for production.
- Browser localStorage keeps saved roles simple; authenticated accounts should persist these server-side.
- Health endpoint checks database connectivity; request logs record method, path, status and latency.
- Accessibility baseline: semantic structure, labelled inputs, visible keyboard focus, mobile breakpoints, reduced-motion support.
- Security baseline: CORS allowlist, bounded fields, HTTP(S) URL validation. Add authentication, authorization, rate limiting, secrets management and dependency scanning before real public production.

## Two-minute walkthrough script
0:00–0:20 Introduce the portal and its audience.
0:20–0:50 Search/filter opportunities and bookmark one; refresh to show saved state.
0:50–1:15 Submit a sample listing and demonstrate validation.
1:15–1:35 Show API docs, health endpoint and logs.
1:35–1:50 Show mobile layout and keyboard navigation.
1:50–2:00 Show repository, real test output and deployed URL.

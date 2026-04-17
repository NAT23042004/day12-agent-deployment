# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets:** API keys and database URLs are written directly in the code.
2. **Fixed Port:** The port is hardcoded (8000) instead of being read from environment variables (required for Cloud).
3. **Lack of Configuration Management:** No separation between development and production settings.
4. **No Health Checks:** Missing endpoints for the platform to monitor if the app is alive or ready.
5. **No Proper Logging:** Using `print()` instead of structured JSON logging which is harder to analyze in production.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config  | Hardcoded | Env Vars | Security and flexibility across environments. |
| Logging | print() | JSON Logs | Searchable and parsable logs for monitoring. |
| Health Check | None | /health, /ready | Automated recovery and traffic routing. |
| Shutdown | Immediate | Graceful | Prevents data loss and finishes current requests. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image:** `python:3.11-slim` (or `python:3.11` for basic version).
2. **Working directory:** `/app`.
3. **Why copy requirements first?** To leverage Docker's layer caching; dependencies are only reinstalled if `requirements.txt` changes.
4. **CMD vs ENTRYPOINT:** CMD provides defaults that can be overridden; ENTRYPOINT is the main command that is always executed.

### Exercise 2.3: Image size comparison
- **Basic/Develop:** ~900 MB (Full Python image)
- **Production (Multi-stage):** < 200 MB (Slim image + Multi-stage optimization)
- **Difference:** ~75-80% reduction in size.

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **URL:** https://day12-production-f11f.up.railway.app
- **Status:** Deployment successful and verified.

## Part 4: API Security

### Exercise 4.4: Cost guard implementation
- **Approach:** Used Redis to track daily expenditures per `user_id`. Each request adds an estimated cost, and requests are blocked once the `daily_budget_usd` defined in environment variables is exceeded.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Health Checks:** Implemented `/health` (Liveness) and `/ready` (Readiness).
- **Stateless Design:** Moved conversation history to Redis. This allows us to scale to multiple instances without losing chat context, as any instance can pull the history from the central Redis store.
- **Graceful Shutdown:** Added signal handler for `SIGTERM` to allow uvicorn to finish in-flight requests before exiting.

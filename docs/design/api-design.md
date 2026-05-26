# API Design

> Last updated: <!-- DATE -->

## 1. Purpose

Defines the conventions for HTTP API endpoints: routing, authentication, validation, error handling, and response formats. Every API route in the application follows these patterns.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| <!-- e.g., `src/app/api/` --> | API route handlers |
| <!-- e.g., `src/lib/auth/` --> | Auth gateway (used by all routes) |
| <!-- e.g., `src/lib/validation/` --> | Input validation schemas |
| <!-- e.g., `src/lib/rate-limit.ts` --> | Rate limiting middleware |

## 3. Architecture

### Request Pipeline

Every API route follows this pipeline:

```
Request → Auth → Rate Limit → Validate Input → Access Check → Business Logic → Response
```

Each step is a hard gate. If any step fails, processing stops with the appropriate error response.

### Standard Route Template

<!-- CUSTOMIZE: Adapt to your framework. This shows the universal pattern. -->

```
async function handleRequest(request):
    // 1. Auth
    user = authGateway.requireAuth()

    // 2. Rate limiting
    checkRateLimit(key=user.id, limit=RATE_LIMITS.write)

    // 3. Input validation
    body = validateSchema(request.body, CreateResourceSchema)

    // 4. Access control
    assertAccess(user, body.resourceId)

    // 5. Business logic
    result = await createResource(body)

    // 6. Response
    return response(201, result)
```

## 4. Error Response Format

All error responses use a consistent JSON format:

```json
{
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_CODE",
  "details": {}
}
```

### Standard Status Codes

| Status | Meaning | When |
|--------|---------|------|
| 200 | OK | Successful read or update |
| 201 | Created | Successful resource creation |
| 204 | No Content | Successful delete |
| 400 | Bad Request | Input validation failed |
| 401 | Unauthorized | Missing or invalid auth token |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unhandled exception (always logged) |

## 5. Input Validation

All input MUST be validated with a schema at the API boundary:

```
// Define schemas separately from routes
const CreateResourceSchema = z.object({
  name: z.string().min(1).max(255),
  type: z.enum(["A", "B", "C"]),
  metadata: z.record(z.string()).optional(),
});
```

Rules:
- Validate shape, types, and ranges
- Sanitize strings that will be rendered in HTML
- Reject unknown fields (strict mode)
- Return specific validation error messages

## 6. Rate Limiting

| Endpoint Type | Default Limit | Window |
|---------------|---------------|--------|
| Read (GET) | 100 req | 1 min |
| Write (POST/PUT/PATCH) | 30 req | 1 min |
| Auth (login/register) | 10 req | 1 min |
| Heavy compute (AI, export) | 5 req | 1 min |

Rate limit responses include `Retry-After` header.

## 7. Streaming Endpoints (SSE)

For long-running operations (AI completion, real-time updates), use Server-Sent Events:

- Use a factory/helper to create SSE streams (never build raw streams)
- Include keepalive heartbeat (every 15-30 seconds)
- Track time-to-first-token (TTFT) for LLM endpoints
- Log total duration with severity (OK/SLOW)
- Clean up resources on client disconnect

## 8. Versioning

<!-- CUSTOMIZE: Choose your API versioning strategy. -->

- URL prefix versioning: `/api/v1/resources`
- Or header versioning: `Accept: application/vnd.app.v1+json`
- Breaking changes require a new version
- Old versions deprecated with a timeline, not removed immediately

## 9. Cross-references

- **[CONSTRAINTS.md](../CONSTRAINTS.md)** — API conventions (§4), Rate limiting (§4)
- **[design/auth-rbac.md](auth-rbac.md)** — Auth gateway methods
- **[design/security.md](security.md)** — Input security, CORS/CSRF

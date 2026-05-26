# Authentication & Role-Based Access Control

> Last updated: <!-- DATE -->

## 1. Purpose

Handles user identity, organization membership, role-based authorization, and data isolation. The auth provider handles identity; the application enforces tiered access control (platform, organization, resource).

## 2. Key Files

| File | Responsibility |
|------|---------------|
| <!-- e.g., `src/lib/auth/types.ts` --> | Provider interfaces: IAuthProvider, IPermissionStore, IAuditLogger |
| <!-- e.g., `src/lib/auth/gateway.ts` --> | AuthGateway: composes auth + permissions + audit |
| <!-- e.g., `src/lib/auth/factory.ts` --> | Factory to create AuthGateway instances |
| <!-- e.g., `src/lib/auth/index.ts` --> | Exports singleton authGateway instance |

## 3. Architecture

### AuthGateway Pattern

Authentication uses a gateway pattern with swappable provider interfaces:

```
AuthGateway
  ├─ IAuthProvider (identity resolution, org management)
  │   → Swappable: Clerk, Auth0, Supabase Auth, custom JWT
  ├─ IPermissionStore (role resolution, access checks)
  │   → Swappable: DB-backed, LDAP, policy engine
  └─ IAuditLogger (action logging)
      → Swappable: DB, log stream, external SIEM
```

API routes import the singleton: `import { authGateway } from "lib/auth"`.

The gateway pattern makes the auth provider swappable — changing identity providers requires only implementing `IAuthProvider`, not changing any route code.

### Gateway Methods

| Method | Purpose | Returns | Throws |
|--------|---------|---------|--------|
| `getCurrentUser()` | Get current authenticated user | `User \| null` | — |
| `requireAuth()` | Require authenticated user | `User` | 401 |
| `requireRole(roles[])` | Require specific role | `User` | 403 |
| `requireAdmin()` | Require platform admin | `User` | 403 |
| `canAccessResource(user, resourceId)` | Check resource access | `boolean` | — |
| `getUserOwnResources(user)` | Get user's own resources (deterministic) | `string[]` | — |
| `audit(entry)` | Write an audit log entry | `void` | — |

### Provider Interfaces

| Interface | Responsibility |
|-----------|----------------|
| `IAuthProvider` | Identity resolution, token validation, user CRUD |
| `IPermissionStore` | Role resolution, resource access checks, tenant scoping |
| `IAuditLogger` | Structured audit log writes and queries |

## 4. Role-Based Access Control

<!-- CUSTOMIZE: Define your application's roles and permissions. -->

### Role Hierarchy

```
┌──────────────────────────────────────┐
│  Platform Roles                       │
│  SITE_ADMIN · SITE_SUPPORT            │
├──────────────────────────────────────┤
│  Organization Roles                   │
│  ADMIN · MANAGER · MEMBER             │
├──────────────────────────────────────┤
│  Resource-Level Access                │
│  Determined by org role + ownership   │
└──────────────────────────────────────┘
```

### Permission Matrix

| Action | SITE_ADMIN | ADMIN | MANAGER | MEMBER |
|--------|-----------|-------|---------|--------|
| View own resources | yes | yes | yes | yes |
| View team resources | yes | yes | yes | no |
| Manage org settings | yes | yes | no | no |
| Manage users | yes | yes | no | no |
| Platform admin panel | yes | no | no | no |

## 5. Data Isolation (Non-Negotiable)

### Personal Data Views

Personal data views (dashboards, profiles, resource lists) MUST use a deterministic, role-independent query:

```
// Good: Always returns the user's own data, regardless of role
getUserOwnResources(userId)

// Bad: Returns different data based on role — admin sees everything
getUserResources(userId, role)
```

### Admin Oversight Views

Admin views that show cross-user data:
- MUST be behind role checks (`requireRole(["ADMIN"])`)
- MUST be visually distinct from personal views
- MUST NOT be accessible from personal navigation

### Validation Rule

On ambiguity, show nothing — never show the wrong user's data.

## 6. API Route Auth Pattern

Every API route follows:

```
export async function POST(request) {
  // 1. Authenticate
  const user = await authGateway.requireAuth();

  // 2. Authorize (role check)
  // await authGateway.requireRole(["ADMIN"]);  // if needed

  // 3. Resource access check
  const hasAccess = await authGateway.canAccessResource(user, resourceId);
  if (!hasAccess) return forbidden();

  // 4. Business logic
  // ...

  // 5. Audit
  await authGateway.audit({ actor: user.id, action: "resource.update", target: resourceId });
}
```

## 7. Cross-references

- **[CONSTRAINTS.md](../CONSTRAINTS.md)** — Security constraints (§6), Data isolation (§6.2)
- **[design/security.md](security.md)** — Input validation, CORS/CSRF
- **[design/api-design.md](api-design.md)** — API route conventions

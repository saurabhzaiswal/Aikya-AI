# Docker operations scripts

`validate.ps1` performs non-destructive Compose and Excalidraw structure checks. Run it from any location with:

```powershell
powershell -ExecutionPolicy Bypass -File docker/scripts/validate.ps1
```

Future scripts must be idempotent, fail fast, avoid embedding secrets, and document destructive behavior. Database migration and retention jobs belong to application/operations tooling, not opaque shell startup hooks.

# Next Trainer Pi Agent plugin

Optional marketplace plugin source. It is not imported by the Next Trainer core and is not part of the default core distribution.

## Runtime baseline

- Build/test Node: exactly 22.19.x (`.nvmrc` and `engine-strict`).
- Pi SDK: exactly 0.84.2.
- Distributed sidecar: Bun 1.4.0 standalone Windows x64 baseline executable.
- Network: fixed loopback listener; the browser iframe never connects to the sidecar directly.

## Self-service package & skill installs (bundled runtime)

The distributed bundle carries its own toolchain so users can install pi
packages (`npm:<pkg>` in the Plugins UI) and skills without installing
anything: Node 22.19 + npm CLI are bundled (`runtime/node/`, unix
`runtime/lib/node_modules/npm`) and the Windows bundle additionally carries
portable MinGit (`runtime/git-mingw/`) because skill installs clone
GitHub-hosted repos. On first plugin action the runtime writes, once:

- `npmCommand = [bundled node, npm-cli.js, --userconfig <agentDir>/npmrc]`
  into the agent settings (a user-configured `npmCommand` is never overwritten);
- a commented `<agentDir>/npmrc` and an agent-local npm cache.

**Proxy / registry users:** the host deliberately gives the runtime no host
environment (no PATH/HOME/proxy passthrough). To install through a corporate
proxy or a registry mirror, edit `<agentDir>/npmrc` — plain npm syntax, e.g.
`proxy=http://127.0.0.1:7890`, `https-proxy=…`, or
`registry=https://registry.npmmirror.com`. One edit covers packages and skills.

## Development

```powershell
npm ci --ignore-scripts
npm run check
```

The initial skeleton exposes authenticated health, provider-profile and session/event seams. The production Pi adapter is intentionally isolated behind `PiRuntimeAdapter`; tests use an in-memory adapter and do not imply that the real Provider path is complete.

No Provider key may be stored in browser persistence, logged, returned by a status route, committed, or included in evidence.

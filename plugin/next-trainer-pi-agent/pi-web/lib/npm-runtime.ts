/**
 * Bundled npm runtime defaults.
 *
 * The Next Trainer plugin ships its own Node.js runtime (`runtime/node/`) and
 * the host launches it with a deliberately minimal environment: no PATH, no
 * HOME, and therefore no npm reachable the usual way. Without a fix, the
 * Plugins UI ("npm:..." package install) fails with `spawn npm ENOENT` and
 * skill installs fail with `spawn npx ENOENT` — users cannot extend the agent.
 *
 * pi's SDK supports exactly the escape hatch we need: the `npmCommand`
 * setting runs an arbitrary command array with `shell: false`. So we point it
 * at the BUNDLED npm itself — `[node, npm-cli.js, --userconfig, <agentDir>/npmrc]`
 * — which resolves the problem without ever touching PATH or spawning .cmd
 * shims (Node refuses to spawn .cmd without a shell since CVE-2024-27980).
 *
 * The generated `npmrc` gives the user one visible, stable place to configure
 * proxy / registry mirrors for the plugin runtime (npm's own syntax), and
 * pins the cache inside the agent dir so nothing leaks into whatever HOME the
 * process happens to have. Existing files and existing settings are NEVER
 * overwritten (user sovereignty), and every failure degrades to a warning:
 * a broken npm setup must never take the chat runtime down.
 */
import { existsSync, mkdirSync, writeFileSync } from "fs";
import path from "path";
import { execPath } from "process";

export interface NpmDefaultsSettings {
  getNpmCommand(): string[] | null | undefined;
  setNpmCommand(command: string[]): void;
  flush(): Promise<void>;
}

interface NpmRuntimePaths {
  nodeBin: string;
  npmCli: string | null;
  npxCli: string | null;
  npmrc: string;
  cacheDir: string;
}

const NPMRC_TEMPLATE = (cacheDir: string, nodeBin: string, npmCli: string) =>
  [
    "# Next Trainer plugin runtime npm configuration (npm syntax; yours to edit).",
    "# Used for package installs from the Plugins UI and skill installs.",
    "#",
    "# Examples:",
    "# proxy=http://127.0.0.1:7890",
    "# https-proxy=http://127.0.0.1:7890",
    "# registry=https://registry.npmmirror.com",
    `cache=${cacheDir}`,
    "",
    `# Bundled runtime: ${nodeBin}`,
    `# Bundled npm:    ${npmCli}`,
    "",
  ].join("\n");

/**
 * Locate the npm suite bundled NEXT TO the running node binary. Same two
 * layouts the pi installer produces and the same shapes lib/npx.ts already
 * understands: Windows keeps node_modules beside node.exe; unix uses
 * <prefix>/bin/node + <prefix>/lib/node_modules/npm.
 */
export function resolveNpmRuntimePaths(agentDir: string, nodeBin = execPath): NpmRuntimePaths {
  const nodeDir = path.dirname(nodeBin);
  const candidates = [
    path.join(nodeDir, "node_modules", "npm", "bin", "npm-cli.js"),
    path.join(nodeDir, "..", "lib", "node_modules", "npm", "bin", "npm-cli.js"),
  ];
  let npmCli: string | null = null;
  for (const candidate of candidates) {
    try {
      if (existsSync(candidate)) {
        npmCli = candidate;
        break;
      }
    } catch {
      /* ignore */
    }
  }
  const npmBinDir = npmCli ? path.dirname(npmCli) : null;
  const npxCli = npmBinDir && existsSync(path.join(npmBinDir, "npx-cli.js"))
    ? path.join(npmBinDir, "npx-cli.js")
    : null;
  return {
    nodeBin,
    npmCli,
    npxCli,
    npmrc: path.join(agentDir, "npmrc"),
    cacheDir: path.join(agentDir, "npm-cache"),
  };
}

/** Write the default npmrc unless the user already has one. Returns its path. */
export function ensureNpmRc(paths: Pick<NpmRuntimePaths, "npmrc" | "cacheDir" | "nodeBin" | "npmCli">): string {
  if (existsSync(paths.npmrc)) return paths.npmrc;
  try {
    mkdirSync(path.dirname(paths.npmrc), { recursive: true });
    writeFileSync(
      paths.npmrc,
      NPMRC_TEMPLATE(paths.cacheDir, paths.nodeBin, paths.npmCli ?? "(not bundled)"),
      "utf-8",
    );
  } catch {
    /* npm will fall back to its own defaults */
  }
  return paths.npmrc;
}

/**
 * Point pi's package manager at the bundled npm (once). An `npmCommand` the
 * user configured themselves always wins; without a bundled npm-cli.js we
 * leave settings untouched (a system npm on PATH, if any, still works).
 */
export async function ensureBundledNpmDefaults(
  settingsManager: NpmDefaultsSettings,
  agentDir: string,
  nodeBin = execPath,
): Promise<void> {
  // The host launches this process with no HOME/USERPROFILE/PATH, so npm/npx
  // (spawned as children by both the package manager and the skill installer)
  // would resolve their cache/config against a missing home and fail. Pinning
  // these on process.env — which every npm/npx child inherits — makes installs
  // work without touching user-controlled argv or the user's global npm state.
  ensureBundledNpmEnv(agentDir, nodeBin);
  const paths = resolveNpmRuntimePaths(agentDir, nodeBin);
  if (!paths.npmCli) return; // nothing bundled to wire up
  const current = settingsManager.getNpmCommand();
  if (current && current.length > 0) return; // user sovereignty: explicit config wins
  settingsManager.setNpmCommand([paths.nodeBin, paths.npmCli, "--userconfig", paths.npmrc]);
  await settingsManager.flush();
}

/**
 * Export npm's own env-override channel so npm/npx find a writable cache and
 * our scoped npmrc regardless of the (stripped) HOME. Never overwrites an
 * explicit value the operator already set.
 */
export function ensureBundledNpmEnv(agentDir: string, nodeBin = execPath): void {
  const paths = resolveNpmRuntimePaths(agentDir, nodeBin);
  try {
    mkdirSync(paths.cacheDir, { recursive: true });
  } catch {
    /* fall back to npm defaults if the cache dir can't be created */
  }
  if (!process.env.npm_config_cache) process.env.npm_config_cache = paths.cacheDir;
  if (!process.env.npm_config_userconfig) {
    process.env.npm_config_userconfig = ensureNpmRc(paths);
  }
  // Some npm/npx code paths consult HOME even when a config is passed; give
  // them the agent dir so a missing home never derails the spawn.
  if (!process.env.HOME) process.env.HOME = agentDir;
  // npx runs a target package's bin, whose `#!/usr/bin/env node` shebang must
  // resolve `node` on PATH. The host launches this process with a stripped
  // PATH (System32 only), so prepend OUR OWN bundled node dir — never the
  // host's PATH (which could expose unrelated tooling). Idempotent.
  const nodeDir = path.dirname(paths.nodeBin);
  const currentPath = process.env.PATH ?? process.env.Path ?? "";
  const onPath = currentPath
    .split(path.delimiter)
    .some((entry) => entry && path.resolve(entry).toLowerCase() === nodeDir.toLowerCase());
  if (!onPath) {
    const nextPath = currentPath ? `${nodeDir}${path.delimiter}${currentPath}` : nodeDir;
    process.env.PATH = nextPath;
    process.env.Path = nextPath; // Windows child inheritance reads `Path`
  }
}

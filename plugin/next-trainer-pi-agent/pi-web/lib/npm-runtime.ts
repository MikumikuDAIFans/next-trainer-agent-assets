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
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync, statSync, writeFileSync } from "fs";
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
 * Locate a git directory to put on PATH. Skill installs run `npx skills add`,
 * whose CLI spawns `git` to clone GitHub-hosted skill repos — in the stripped
 * host environment that spawn dies with ENOENT. Prefer the git bundled with
 * the plugin (runtime/git-mingw, Windows), then well-known Git-for-Windows
 * install dirs, then the standard unix locations (once PATH is set
 * explicitly, the loader's built-in default search paths no longer apply).
 */
export function findRuntimeGitDir(nodeBin = execPath, platform = process.platform): string | null {
  const gitExe = platform === "win32" ? "git.exe" : "git";
  const runtimeRoot = path.dirname(path.dirname(nodeBin)); // runtime/node/<exe> -> runtime
  const dirs: string[] = [];
  if (platform === "win32") {
    dirs.push(path.join(runtimeRoot, "git-mingw", "cmd"));
    const programFiles = process.env.ProgramFiles || process.env["ProgramFiles(x86)"] || "C:\\Program Files";
    dirs.push(path.join(programFiles, "Git", "cmd"));
    if (process.env.LOCALAPPDATA) {
      dirs.push(path.join(process.env.LOCALAPPDATA, "Programs", "Git", "cmd"));
    }
  } else {
    dirs.push("/usr/bin", "/usr/local/bin");
  }
  for (const dir of dirs) {
    try {
      if (existsSync(path.join(dir, gitExe))) return dir;
    } catch {
      /* ignore */
    }
  }
  return null;
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
  // Children need real executables on PATH: `node` (npx runs package bins via
  // `#!/usr/bin/env node`) and `git` (the skills CLI clones GitHub repos).
  // We prepend ONLY our bundled/known-good dirs — never the host's PATH,
  // which the host stripped on purpose. Idempotent.
  const prepend: string[] = [];
  const pushDir = (dir: string | null): void => {
    if (dir && !prepend.includes(dir)) prepend.push(dir);
  };
  pushDir(path.dirname(paths.nodeBin));
  pushDir(findRuntimeGitDir(paths.nodeBin));
  if (prepend.length === 0) return;
  const currentPath = process.env.PATH ?? process.env.Path ?? "";
  const known = new Set(
    currentPath
      .split(path.delimiter)
      .filter((entry) => entry)
      .map((entry) => path.resolve(entry).toLowerCase()),
  );
  const missing = prepend.filter((dir) => !known.has(path.resolve(dir).toLowerCase()));
  if (missing.length === 0) return;
  const nextPath = [...missing, currentPath].filter(Boolean).join(path.delimiter);
  process.env.PATH = nextPath;
  process.env.Path = nextPath; // Windows child inheritance reads `Path`
}

/**
 * Bridge for `npx skills add -g --agent pi`: the CLI installs into the NATIVE
 * pi global dir `$HOME/.pi/agent/skills`, but this deployment relocates the
 * agent dir (NEXT_TRAINER_PI_AGENT_DIR), and the SDK resource loader scans
 * <agentDir>/skills - so CLI-installed skills would be invisible to the agent.
 * Copy each installed skill into <agentDir>/skills (replacing any previous
 * copy). Returns the synced skill names; failures degrade to skips.
 */
export function syncCliInstalledSkills(agentDir: string, homeDir = process.env.HOME): string[] {
  const home = homeDir || (process.env.USERPROFILE ?? "");
  if (!home) return [];
  const srcRoot = path.join(home, ".pi", "agent", "skills");
  const synced: string[] = [];
  let names: string[];
  try {
    names = readdirSync(srcRoot);
  } catch {
    return [];
  }
  for (const name of names) {
    const src = path.join(srcRoot, name);
    try {
      if (!statSync(src).isDirectory() || !existsSync(path.join(src, "SKILL.md"))) continue;
      const dst = path.join(agentDir, "skills", name);
      rmSync(dst, { recursive: true, force: true });
      cpSync(src, dst, { recursive: true });
      synced.push(name);
    } catch {
      /* a broken skill dir must not fail the whole install */
    }
  }
  return synced;
}

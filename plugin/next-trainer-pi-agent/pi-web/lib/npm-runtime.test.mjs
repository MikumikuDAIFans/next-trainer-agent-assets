import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

import {
  resolveNpmRuntimePaths,
  ensureNpmRc,
  ensureBundledNpmDefaults,
  ensureBundledNpmEnv,
  findRuntimeGitDir,
} from "./npm-runtime.ts";

/** Create a fake node distro: win = node_modules beside node.exe, unix = ../lib layout. */
function makeFakeRuntime(layout) {
  const root = mkdtempSync(path.join(tmpdir(), "nt-npm-"));
  const nodeDir = path.join(root, "runtime", "node");
  mkdirSync(nodeDir, { recursive: true });
  const nodeBin = path.join(nodeDir, process.platform === "win32" ? "node.exe" : "node");
  writeFileSync(nodeBin, "");
  const npmDir =
    layout === "win"
      ? path.join(nodeDir, "node_modules", "npm")
      : path.join(root, "runtime", "lib", "node_modules", "npm");
  mkdirSync(path.join(npmDir, "bin"), { recursive: true });
  writeFileSync(path.join(npmDir, "bin", "npm-cli.js"), "// fake npm");
  writeFileSync(path.join(npmDir, "bin", "npx-cli.js"), "// fake npx");
  return { root, nodeDir, nodeBin, agentDir: path.join(root, "agent"), cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

function fakeSettings(initial = {}) {
  let state = { ...initial };
  return {
    getNpmCommand() {
      return state.npmCommand ? [...state.npmCommand] : undefined;
    },
    setNpmCommand(command) {
      state.npmCommand = [...command];
    },
    async flush() {
      state.flushed = true;
    },
    snapshot: () => state,
  };
}

const ENV_KEYS = [
  "npm_config_cache",
  "npm_config_userconfig",
  "HOME",
  "PATH",
  "Path",
  "ProgramFiles",
  "ProgramFiles(x86)",
  "LOCALAPPDATA",
];
function withCleanEnv(fn) {
  const saved = Object.fromEntries(ENV_KEYS.map((k) => [k, process.env[k]]));
  for (const k of ENV_KEYS) delete process.env[k];
  try {
    return fn();
  } finally {
    for (const k of ENV_KEYS) {
      if (saved[k] === undefined) delete process.env[k];
      else process.env[k] = saved[k];
    }
  }
}

test("resolveNpmRuntimePaths finds the windows-layout bundled npm (node_modules beside node.exe)", () => {
  const rt = makeFakeRuntime("win");
  try {
    const paths = resolveNpmRuntimePaths(rt.agentDir, rt.nodeBin);
    assert.ok(paths.npmCli?.endsWith(path.join("node_modules", "npm", "bin", "npm-cli.js")));
    assert.ok(paths.npxCli?.endsWith(path.join("node_modules", "npm", "bin", "npx-cli.js")));
    assert.equal(paths.npmrc, path.join(rt.agentDir, "npmrc"));
    assert.equal(paths.cacheDir, path.join(rt.agentDir, "npm-cache"));
  } finally {
    rt.cleanup();
  }
});

test("resolveNpmRuntimePaths finds the unix-layout bundled npm (../lib/node_modules/npm)", () => {
  const rt = makeFakeRuntime("unix");
  try {
    const paths = resolveNpmRuntimePaths(rt.agentDir, rt.nodeBin);
    assert.ok(paths.npmCli?.includes(path.join("runtime", "lib", "node_modules", "npm", "bin", "npm-cli.js")));
    assert.ok(paths.npxCli);
  } finally {
    rt.cleanup();
  }
});

test("resolveNpmRuntimePaths reports no bundled npm when none is present", () => {
  const root = mkdtempSync(path.join(tmpdir(), "nt-npm-empty-"));
  try {
    const paths = resolveNpmRuntimePaths(path.join(root, "agent"), path.join(root, "node.exe"));
    assert.equal(paths.npmCli, null);
    assert.equal(paths.npxCli, null);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("ensureNpmRc writes the template once and never overwrites the user's file", () => {
  const rt = makeFakeRuntime("win");
  try {
    const paths = resolveNpmRuntimePaths(rt.agentDir, rt.nodeBin);
    mkdirSync(rt.agentDir, { recursive: true });
    ensureNpmRc(paths);
    const first = readFileSync(paths.npmrc, "utf-8");
    assert.match(first, new RegExp(`cache=${paths.cacheDir.replace(/[\\^$.*+?()[\]{}|]/g, "\\$&")}`));
    assert.match(first, /https-proxy/); // proxy hint present for the user
    writeFileSync(paths.npmrc, "registry=https://example.invalid\n", "utf-8");
    ensureNpmRc(paths);
    assert.equal(readFileSync(paths.npmrc, "utf-8"), "registry=https://example.invalid\n");
  } finally {
    rt.cleanup();
  }
});

test("ensureBundledNpmDefaults wires npmCommand to the bundled node + npm-cli with userconfig", async () => {
  const rt = makeFakeRuntime("win");
  try {
    mkdirSync(rt.agentDir, { recursive: true });
    const settings = fakeSettings();
    await withCleanEnv(() => ensureBundledNpmDefaults(settings, rt.agentDir, rt.nodeBin));
    assert.deepEqual(settings.getNpmCommand(), [
      rt.nodeBin,
      path.join(rt.nodeDir, "node_modules", "npm", "bin", "npm-cli.js"),
      "--userconfig",
      path.join(rt.agentDir, "npmrc"),
    ]);
    assert.equal(settings.snapshot().flushed, true);
    assert.ok(existsSync(path.join(rt.agentDir, "npmrc")));
  } finally {
    rt.cleanup();
  }
});

test("ensureBundledNpmDefaults never overwrites a user-configured npmCommand", async () => {
  const rt = makeFakeRuntime("win");
  try {
    mkdirSync(rt.agentDir, { recursive: true });
    const settings = fakeSettings({ npmCommand: ["pnpm"] });
    await withCleanEnv(() => ensureBundledNpmDefaults(settings, rt.agentDir, rt.nodeBin));
    assert.deepEqual(settings.getNpmCommand(), ["pnpm"]);
    assert.notEqual(settings.snapshot().flushed, true);
  } finally {
    rt.cleanup();
  }
});

test("ensureBundledNpmDefaults is a settings no-op when no bundled npm exists", async () => {
  const root = mkdtempSync(path.join(tmpdir(), "nt-npm-none-"));
  try {
    const agentDir = path.join(root, "agent");
    const settings = fakeSettings();
    await withCleanEnv(() => ensureBundledNpmDefaults(settings, agentDir, path.join(root, "node.exe")));
    assert.equal(settings.getNpmCommand(), undefined);
    assert.notEqual(settings.snapshot().flushed, true);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("ensureBundledNpmEnv pins npm cache/config, keeps HOME sane, and puts the bundled node dir on PATH", () => {
  const rt = makeFakeRuntime("win");
  try {
    mkdirSync(rt.agentDir, { recursive: true });
    withCleanEnv(() => {
      process.env.PATH = "C:\\Windows\\System32";
      ensureBundledNpmEnv(rt.agentDir, rt.nodeBin);
      assert.equal(process.env.npm_config_cache, path.join(rt.agentDir, "npm-cache"));
      assert.equal(process.env.npm_config_userconfig, path.join(rt.agentDir, "npmrc"));
      assert.equal(process.env.HOME, rt.agentDir);
      const entries = process.env.PATH.split(path.delimiter);
      assert.equal(entries[0].toLowerCase(), rt.nodeDir.toLowerCase());
      assert.equal(entries[1], "C:\\Windows\\System32");
      assert.equal(process.env.Path, process.env.PATH);
      // idempotent: a second bootstrap call does not double-prepend
      ensureBundledNpmEnv(rt.agentDir, rt.nodeBin);
      assert.equal(process.env.PATH.split(path.delimiter).length, 2);
    });
  } finally {
    rt.cleanup();
  }
});

test("ensureBundledNpmEnv preserves explicit npm_config values", () => {
  const rt = makeFakeRuntime("win");
  try {
    mkdirSync(rt.agentDir, { recursive: true });
    withCleanEnv(() => {
      process.env.npm_config_cache = "D:\\mine\\cache";
      ensureBundledNpmEnv(rt.agentDir, rt.nodeBin);
      assert.equal(process.env.npm_config_cache, "D:\\mine\\cache");
    });
  } finally {
    rt.cleanup();
  }
});

test("findRuntimeGitDir prefers the git bundled in the runtime over system dirs", () => {
  const rt = makeFakeRuntime("win");
  try {
    const bundledCmd = path.join(rt.root, "runtime", "git-mingw", "cmd");
    mkdirSync(bundledCmd, { recursive: true });
    writeFileSync(path.join(bundledCmd, "git.exe"), "");
    const systemCmd = path.join(rt.root, "Program Files", "Git", "cmd");
    mkdirSync(systemCmd, { recursive: true });
    writeFileSync(path.join(systemCmd, "git.exe"), "");
    withCleanEnv(() => {
      process.env.ProgramFiles = path.join(rt.root, "Program Files");
      assert.equal(findRuntimeGitDir(rt.nodeBin, "win32"), bundledCmd);
      rmSync(path.join(rt.root, "runtime", "git-mingw"), { recursive: true, force: true });
      assert.equal(findRuntimeGitDir(rt.nodeBin, "win32"), systemCmd); // system fallback
    });
  } finally {
    rt.cleanup();
  }
});

test("findRuntimeGitDir reports null when no git exists anywhere", () => {
  const root = mkdtempSync(path.join(tmpdir(), "nt-npm-nogit-"));
  try {
    withCleanEnv(() => {
      process.env.ProgramFiles = path.join(root, "nope");
      assert.equal(findRuntimeGitDir(path.join(root, "runtime", "node", "node.exe"), "win32"), null);
    });
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("ensureBundledNpmEnv puts bundled node AND git dirs on PATH (in order)", () => {
  const rt = makeFakeRuntime("win");
  try {
    mkdirSync(rt.agentDir, { recursive: true });
    const gitCmd = path.join(rt.root, "runtime", "git-mingw", "cmd");
    mkdirSync(gitCmd, { recursive: true });
    writeFileSync(path.join(gitCmd, "git.exe"), "");
    withCleanEnv(() => {
      process.env.PATH = "C:\\Windows\\System32";
      process.env.ProgramFiles = path.join(rt.root, "unused");
      ensureBundledNpmEnv(rt.agentDir, rt.nodeBin);
      const entries = process.env.PATH.split(path.delimiter);
      assert.equal(entries[0].toLowerCase(), rt.nodeDir.toLowerCase());
      assert.equal(entries[1].toLowerCase(), gitCmd.toLowerCase());
      assert.equal(entries[2], "C:\\Windows\\System32");
      // idempotent
      ensureBundledNpmEnv(rt.agentDir, rt.nodeBin);
      assert.equal(process.env.PATH.split(path.delimiter).length, 3);
    });
  } finally {
    rt.cleanup();
  }
});

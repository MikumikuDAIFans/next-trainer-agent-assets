import { Suspense } from "react";
import { AppShell } from "@/components/AppShell";
import { I18nProvider } from "@/hooks/useI18n";

/**
 * P1-6②: SSR first-paint skeleton.
 *
 * The client app is a single hydration-heavy bundle (~7.2 MB / 204 assets).
 * Until the JS downloads, parses and hydrates, the served HTML is EMPTY —
 * the user opens the floating panel into ~10 s of pure blank. Server-render
 * the "Opening workspace..." state into the initial HTML (the exact state
 * the client shows in AppShell's `validating` branch) so the FIRST byte the
 * browser can paint already carries readable feedback:
 *
 *   - text: "Opening workspace..." (default locale, mirroring the client's
 *     en default; the zh-CN locale renders 正在打开工作区... post-hydration)
 *   - path: the ?cwd= target when present (same input the client uses via
 *     lib/initial-navigation.ts)
 *
 * Handoff: AppShell removes `#initial-workspace-skeleton` on mount, so the
 * client's own validating/ready/error UI takes over with zero flash (the
 * skeleton uses the same CSS variables and layout as the client state). If
 * the JS never arrives, the skeleton stays — text instead of blank.
 */
export default async function Home({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;
  const cwd = typeof params.cwd === "string" ? params.cwd.trim() : "";
  return (
    <>
      <div
        id="initial-workspace-skeleton"
        role="status"
        style={{
          position: "fixed",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 8,
          padding: 24,
          background: "var(--bg)",
          color: "var(--text-muted)",
          textAlign: "center",
          zIndex: 0,
        }}
      >
        <div
          style={{
            width: 26,
            height: 26,
            border: "2px solid var(--text-dim)",
            borderTopColor: "transparent",
            borderRadius: "50%",
            animation: "iws-spin 0.9s linear infinite",
          }}
          aria-hidden="true"
        />
        <div style={{ fontSize: 14, color: "var(--text)" }}>
          {cwd ? "Opening workspace..." : "Loading..."}
        </div>
        {cwd ? (
          <div
            style={{
              maxWidth: "min(720px, 100%)",
              overflowWrap: "anywhere",
              fontFamily: "var(--font-mono)",
              fontSize: 12,
            }}
          >
            {cwd}
          </div>
        ) : null}
        <style>{`@keyframes iws-spin{to{transform:rotate(360deg)}}`}</style>
      </div>
      <Suspense>
        <I18nProvider>
          <AppShell />
        </I18nProvider>
      </Suspense>
    </>
  );
}

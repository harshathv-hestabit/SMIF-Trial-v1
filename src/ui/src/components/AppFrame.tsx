import { NavLink, Outlet } from "react-router-dom";

export function AppFrame() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[var(--canvas)] text-[var(--ink-strong)]">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-[-12rem] top-[-14rem] h-[28rem] w-[28rem] rounded-full bg-[radial-gradient(circle,_rgba(26,110,255,0.18),_transparent_64%)] blur-3xl" />
        <div className="absolute right-[-10rem] top-[8rem] h-[30rem] w-[30rem] rounded-full bg-[radial-gradient(circle,_rgba(227,88,50,0.14),_transparent_64%)] blur-3xl" />
        <div className="absolute inset-x-0 bottom-[-16rem] h-[26rem] bg-[radial-gradient(circle_at_center,_rgba(29,177,117,0.14),_transparent_60%)] blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-screen w-full max-w-[1500px] flex-col gap-6 px-4 py-5 sm:px-6 lg:px-8">
        <header className="rounded-[2rem] border border-[var(--line)] bg-[var(--panel-strong)] px-5 py-5 shadow-[0_24px_80px_rgba(3,15,36,0.24)] backdrop-blur-xl sm:px-7">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-[11px] font-semibold uppercase tracking-[0.34em] text-[var(--accent)]">
                v1.2
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-[var(--ink-strong)] sm:text-5xl">
                Smart Market Insight Feed
              </h1>
            </div>
          </div>

          <nav className="mt-6 flex flex-wrap gap-2">
            <PrimaryNav to="/" label="Overview" />
            <PrimaryNav to="/ops" label="Ops Center" />
            <PrimaryNav to="/clients" label="Client Workspace" />
          </nav>
        </header>

        <main className="pb-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function PrimaryNav(props: { to: string; label: string }) {
  return (
    <NavLink
      end={props.to === "/"}
      to={props.to}
      className={({ isActive }) =>
        [
          "rounded-full border px-4 py-2 text-sm font-medium transition",
          isActive
            ? "border-[var(--accent)] bg-[var(--accent)] text-white shadow-[0_12px_30px_rgba(26,110,255,0.22)]"
            : "border-[var(--line)] bg-white/70 text-[var(--ink-muted)] hover:border-[var(--line-strong)] hover:bg-white hover:text-[var(--ink-strong)]",
        ].join(" ")
      }
    >
      {props.label}
    </NavLink>
  );
}

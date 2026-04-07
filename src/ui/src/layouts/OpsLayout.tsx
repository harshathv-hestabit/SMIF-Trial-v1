import { Outlet } from "react-router-dom";

import { SectionHeader } from "../components/SectionHeader";
import { SubNav } from "../components/SubNav";

const OPS_NAV_ITEMS = [
  {
    to: "/ops/overview",
    label: "Overview",
    description: "Metrics and recent insight activity.",
  },
  {
    to: "/ops/news",
    label: "News Explorer",
    description: "Lifecycle monitoring with full document detail.",
  },
  {
    to: "/ops/pipeline",
    label: "Pipeline",
    description: "Manual ingestion and output monitoring.",
  },
];

export function OpsLayout() {
  return (
    <section className="grid gap-4">
      <div className="grid gap-4 rounded-[1.75rem] border border-[var(--border-1)] bg-[linear-gradient(180deg,rgba(14,20,38,0.88),rgba(18,24,44,0.72))] p-5 shadow-[0_18px_70px_rgba(1,5,20,0.3)]">
        <SectionHeader
          eyebrow="Operations"
          title="Ops workspace"
          description="Separate views for monitoring, document triage, and pipeline operations."
        />
        <SubNav items={OPS_NAV_ITEMS} />
      </div>
      <Outlet />
    </section>
  );
}

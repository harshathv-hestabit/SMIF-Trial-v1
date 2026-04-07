interface StatCardProps {
  label: string;
  value: string;
  hint: string;
  tone?: "default" | "accent" | "warm" | "critical";
}

const toneClasses: Record<NonNullable<StatCardProps["tone"]>, string> = {
  default: "from-white to-[#eff4fb]",
  accent: "from-[#edf4ff] to-[#dfe9ff]",
  warm: "from-[#fff3eb] to-[#ffe2d1]",
  critical: "from-[#fff2f0] to-[#ffdeda]",
};

export function StatCard(props: StatCardProps) {
  return (
    <article
      className={[
        "rounded-[1.75rem] border border-[var(--line)] bg-gradient-to-br p-5 shadow-[0_12px_40px_rgba(7,23,42,0.08)]",
        toneClasses[props.tone ?? "default"],
      ].join(" ")}
    >
      <p className="text-sm font-medium text-[var(--ink-soft)]">{props.label}</p>
      <p className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-[var(--ink-strong)]">
        {props.value}
      </p>
      <p className="mt-2 text-sm leading-6 text-[var(--ink-soft)]">{props.hint}</p>
    </article>
  );
}

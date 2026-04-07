export function StatusBadge(props: { label: string; tone?: "neutral" | "good" | "warn" | "bad" }) {
  const tone = props.tone ?? "neutral";

  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]",
        tone === "good" && "bg-[rgba(29,177,117,0.12)] text-[var(--success)]",
        tone === "warn" && "bg-[rgba(227,88,50,0.12)] text-[var(--accent-warm-strong)]",
        tone === "bad" && "bg-[rgba(198,40,40,0.12)] text-[var(--critical)]",
        tone === "neutral" && "bg-[rgba(26,110,255,0.1)] text-[var(--accent)]",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      {props.label}
    </span>
  );
}

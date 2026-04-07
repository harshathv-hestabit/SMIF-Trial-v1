export function EmptyState(props: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-[1.5rem] border border-dashed border-[var(--line-strong)] bg-white/60 px-5 py-6">
      <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
        {props.eyebrow}
      </p>
      <h3 className="mt-3 text-lg font-semibold text-[var(--ink-strong)]">{props.title}</h3>
      <p className="mt-2 max-w-xl text-sm leading-6 text-[var(--ink-soft)]">
        {props.description}
      </p>
    </div>
  );
}

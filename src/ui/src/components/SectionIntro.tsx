export function SectionIntro(props: {
  eyebrow: string;
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div className="max-w-2xl">
        <p className="text-[11px] font-semibold uppercase tracking-[0.3em] text-[var(--accent)]">
          {props.eyebrow}
        </p>
        <h2 className="mt-2 text-2xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
          {props.title}
        </h2>
        <p className="mt-2 text-sm leading-6 text-[var(--ink-soft)]">{props.description}</p>
      </div>
      {props.action ? <div>{props.action}</div> : null}
    </div>
  );
}

import type { ReactNode } from "react";

interface SectionHeaderProps {
  eyebrow: string;
  title: string;
  description?: string;
  action?: ReactNode;
}

export function SectionHeader(props: SectionHeaderProps) {
  return (
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--text-3)]">
          {props.eyebrow}
        </p>
        <h2 className="text-lg font-semibold text-white">{props.title}</h2>
        {props.description ? (
          <p className="mt-1 text-sm text-[var(--text-3)]">{props.description}</p>
        ) : null}
      </div>
      {props.action}
    </div>
  );
}

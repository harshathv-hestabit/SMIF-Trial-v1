import type { ReactNode } from "react";

export function Surface(props: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={[
        "rounded-[1.9rem] border border-[var(--line)] bg-[var(--panel)] p-5 shadow-[0_16px_44px_rgba(6,20,37,0.08)] backdrop-blur-xl sm:p-6",
        props.className ?? "",
      ].join(" ")}
    >
      {props.children}
    </section>
  );
}

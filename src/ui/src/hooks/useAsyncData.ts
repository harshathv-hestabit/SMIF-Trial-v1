import { useEffect, useState } from "react";
import type { DependencyList } from "react";

interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useAsyncData<T>(loader: () => Promise<T>, deps: DependencyList) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: true,
    error: null,
  });
  const [reloadToken, setReloadToken] = useState(0);

  useEffect(() => {
    let cancelled = false;

    setState((current) => ({
      data: current.data,
      loading: true,
      error: null,
    }));

    loader()
      .then((data) => {
        if (!cancelled) {
          setState({
            data,
            loading: false,
            error: null,
          });
        }
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setState((current) => ({
            data: current.data,
            loading: false,
            error: error instanceof Error ? error.message : "Request failed",
          }));
        }
      });

    return () => {
      cancelled = true;
    };
  }, [...deps, reloadToken]);

  return {
    ...state,
    reload: () => setReloadToken((current) => current + 1),
  };
}

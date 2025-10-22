export const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || `${window.location.origin}/api`;

export function apiFetch(path: string, options?: RequestInit) {
  const base = API_BASE.replace(/\/$/, "");
  const rel = path.startsWith("/") ? path : `/${path}`;
  return fetch(`${base}${rel}`, options);
}



import { useAuthStore } from "@/stores/auth-store";

export function useCredits() {
  const user = useAuthStore((s) => s.user);
  return { credits: user?.credits ?? 0 };
}

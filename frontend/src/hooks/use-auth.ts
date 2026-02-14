import { useEffect } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";

export function useAuth() {
  const { user, token, setUser, logout } = useAuthStore();

  useEffect(() => {
    if (token && !user) {
      api
        .get("/users/me")
        .then((res) => setUser(res.data))
        .catch(() => logout());
    }
  }, [token, user, setUser, logout]);

  return { user, token, isAuthenticated: !!token, logout };
}

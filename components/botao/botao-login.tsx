"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useAuth } from "@/providers/auth-provider";
import { UserAvatar } from "@/components/user-avatar";

export function LoginButton() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  const handleLoginClick = () => {
    router.push("/login");
  };

  // Se o usuário estiver autenticado, mostra o avatar
  if (isAuthenticated) {
    return <UserAvatar />;
  }

  // Se não estiver autenticado, mostra o botão de login
  return <Button onClick={handleLoginClick}>Login</Button>;
}

"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";

export function LoginButton() {
  const router = useRouter();

  const handleLoginClick = () => {
    router.push("/login");
  };

  return <Button onClick={handleLoginClick}>Login</Button>;
}

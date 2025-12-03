"use client";

import CustomLink from "./navbar";
import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

interface User {
  id: string;
  name: string;
  email: string;
  favoriteInstrumentId?: string;
}

export default function NavbarFinal() {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<User | null>(null);
  const [mounted, setMounted] = useState(false);
  const isAboutUs = pathname === "/aboutus";

  useEffect(() => {
    setMounted(true);
    const localUser = localStorage.getItem("user");
    if (localUser) {
      try {
        setUser(JSON.parse(localUser));
      } catch (e) {
        console.warn("Erro ao parsear usuário:", e);
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    router.push("/login");
    setUser(null);
  };

  if (!mounted) return null;

  return (
    <div className="absolute top-0 left-0 w-full h-16 flex items-center justify-between px-24 z-30">
      <nav className="flex items-center space-x-8">
        <CustomLink href="/home" label="Home" />
        <CustomLink href="/aboutus" label="About Us" />
        <CustomLink href="/instruments" label="Our Instruments" />
        <CustomLink href="/pricing" label="Pricing" />
      </nav>

      <div className="flex items-center space-x-4">
        {user ? (
          <>
            <span className={`font-semibold text-sm ${isAboutUs ? "text-black" : "text-white"}`}>{user.name}</span>
            <Button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 text-sm"
            >
              Logout
            </Button>
          </>
        ) : (
          <>
            <CustomLink href="/login" label="Login" />
            <CustomLink href="/signup" label="Sign Up" />
          </>
        )}
      </div>
    </div>
  );
}

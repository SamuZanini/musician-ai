"use client";

import * as React from "react";
import { AnimatedShinyTextDemo } from "@/components/botao/botao";
import { AuroraText } from "@/components/magicui/aurora-text";
import { useTheme } from "next-themes";
import { useSidebar } from "@/components/ui/sidebar";

export default function Home() {
  const { theme } = useTheme();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const gradient =
    theme === "dark"
      ? "linear-gradient(to right, rgba(0,0,0,1) 25%, rgba(0,0,0,0.9) 35%, rgba(0,0,0,0.9) 45%, rgba(0,0,0,0.8) 75%, rgba(0,0,0,0.7) 85%, rgba(0,0,0,0) 99%)"
      : "linear-gradient(to right, rgba(255,255,255,0.8) 25%, rgba(255,255,255,0.7) 35%, rgba(255,255,255,0.6) 45%, rgba(255,255,255,0.4) 75%, rgba(255,255,255,0.2) 85%, rgba(255,255,255,0) 99%)";

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen w-full relative">
      {/* Background image */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: "url('/images/maestro.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Overlay with blur effect */}
      <div
        className={`absolute inset-0 transition-all duration-300 ${
          open || openMobile ? "backdrop-blur-md bg-black/10" : ""
        }`}
        style={{ zIndex: 20 }}
      />

      {/* Gradient overlay */}
      <div
        className="absolute top-0 left-0 h-full"
        style={{
          width: "50%",
          background: gradient,
          pointerEvents: "none",
          zIndex: 10,
        }}
      />

      {/* Content */}
      <div className="relative flex items-center min-h-screen">
        <div
          className="flex flex-col items-center justify-center w-1/3 h-screen gap-6 pl-12"
          style={{ zIndex: 30 }}
        >
          <img
            src="/images/logo-png.png"
            alt="logo-png"
            className="w-56 h-56 mb-2"
          />
          <h1 className="font-bold text-7xl font-italianno mb-2">#Dô</h1>
          <p className="text-5xl font-italianno">Your Online Music Teacher</p>
          <div className="w-full -mt-25">
            <AnimatedShinyTextDemo />
          </div>
        </div>
      </div>
    </div>
  );
}

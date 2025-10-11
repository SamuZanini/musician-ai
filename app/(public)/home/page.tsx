"use client";

import * as React from "react";
import { AnimatedShinyTextDemo } from "@/components/botao/botao";
import { AuroraText } from "@/components/magicui/aurora-text";
import { useTheme } from "next-themes";
import NavbarFinal from "@/components/navbar";
import { useRouter } from "next/navigation";
import { motion } from "motion/react";

export default function Home() {
  const { theme } = useTheme();
  const [mounted, setMounted] = React.useState(false);
  const router = useRouter();

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const handleGetStartedClick = () => {
    router.push("/pricing");
  };

  const gradient =
    theme === "dark"
      ? "linear-gradient(to right, rgba(0,0,0,1) 25%, rgba(0,0,0,0.9) 35%, rgba(0,0,0,0.9) 45%, rgba(0,0,0,0.8) 75%, rgba(0,0,0,0.7) 85%, rgba(0,0,0,0) 99%)"
      : "linear-gradient(to right, rgba(255,255,255,0.8) 25%, rgba(255,255,255,0.7) 35%, rgba(255,255,255,0.6) 45%, rgba(255,255,255,0.4) 75%, rgba(255,255,255,0.2) 85%, rgba(255,255,255,0) 99%)";

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen w-full relative">
      {/* Navbar */}
      <NavbarFinal />
      {/* Background image */}
      <div
        className="absolute inset-0 bg-no-repeat h-screen w-screen overflow-hidden"
        style={{
          backgroundImage: "url('/images/maestro.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
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
          style={{ zIndex: 10 }}
        >
          <motion.div
            initial={{ opacity: 0, y: 200 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.0 }}
          >
            <img
              src="/images/logo-png.png"
              alt="logo-png"
              className="w-56 h-56 mb-2"
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 200 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1.5 }}
          >
            <h1 className="font-bold text-7xl font-italianno mb-2">#Dô</h1>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 200 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 2.0 }}
          >
            <p className="text-5xl font-italianno">Your Online Music Teacher</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 200 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 2.5 }}
            className="w-full -mt-25"
          >
            <AnimatedShinyTextDemo onClick={handleGetStartedClick} />
          </motion.div>
        </div>
      </div>
    </div>
  );
}

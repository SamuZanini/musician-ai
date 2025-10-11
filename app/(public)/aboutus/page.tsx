"use client";

import * as React from "react";
import NavbarFinal from "@/components/navbar";
import SocialLinksArrowAnimation from "@/components/redesSociais/socialLinks";
import { Github, Linkedin } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Highlighter } from "@/components/ui/highlighter";
import { useTheme } from "next-themes";
import { useSidebar } from "@/components/ui/sidebar";
import { motion } from "motion/react";

export default function AboutUs() {
  const { theme } = useTheme();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }
  const samuelLinks = [
    {
      key: "github",
      icon: <Github />,
      link: "https://github.com/SamuZanini",
    },
    {
      key: "linkedin",
      icon: <Linkedin />,
      link: "https://www.linkedin.com/in/samuel-zanini-campos-vanoni-b2834b268/",
    },
  ];

  const hugoLinks = [
    {
      key: "github",
      icon: <Github />,
      link: "https://github.com/hugo-santos",
    },
    {
      key: "linkedin",
      icon: <Linkedin />,
      link: "https://github.com/HugOtavioS",
    },
  ];

  return (
    <div
      className={`min-h-screen w-full relative ${
        theme === "dark" ? "bg-black-900" : "bg-gray-50"
      }`}
    >
      {/* Overlay with blur effect when sidebar is open */}
      <div
        className={`absolute inset-0 transition-all duration-300 ${
          open || openMobile ? "backdrop-blur-md bg-black/10" : ""
        }`}
        style={{ zIndex: 20 }}
      />

      <motion.div
        initial={{ opacity: 0, y: 200 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.0 }}
      >
        <NavbarFinal />
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 200 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
        className="flex flex-col items-center justify-center h-screen gap-8 relative"
        style={{ zIndex: 10 }}
      >
        <p
          className={`text-center text-2xl pd-10 ${
            theme === "dark" ? "text-white" : "text-gray-800"
          }`}
        >
          Turn creators{" "}
          <Highlighter action="underline" color="#FFD700">
            into mentors.
          </Highlighter>{" "}
          Teach music,{" "}
          <Highlighter action="highlight" color="#B87333">
            ignite passion.
          </Highlighter>{" "}
        </p>
        <div className="flex gap-20 items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            <Avatar className="w-70 h-70">
              <AvatarImage src="/images/samuel.jpeg" />
              <AvatarFallback>SZ</AvatarFallback>
            </Avatar>
            <h1
              className={`text-5xl text-center font-italianno ${
                theme === "dark" ? "text-white" : "text-gray-800"
              }`}
            >
              Samuel Zanini Campos Vanoni
            </h1>
            <SocialLinksArrowAnimation links={samuelLinks} />
          </div>
          <div className="flex flex-col items-center gap-4">
            <Avatar className="w-70 h-70">
              <AvatarImage src="/images/hugo.jpeg" />
              <AvatarFallback>HO</AvatarFallback>
            </Avatar>
            <h1
              className={`text-5xl text-center font-italianno ${
                theme === "dark" ? "text-white" : "text-gray-800"
              }`}
            >
              Hugo Otávio dos Santos de Paula
            </h1>
            <SocialLinksArrowAnimation links={hugoLinks} />
          </div>
        </div>
      </motion.div>
    </div>
  );
}

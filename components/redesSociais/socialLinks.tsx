"use client";
import { CircleArrowRight, Linkedin, Github } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";
import React, { useState } from "react";

type SocialLink = {
  key: string;
  icon: React.ReactNode;
  link: string;
};

type SocialLinksArrowAnimationProps = {
  links?: SocialLink[];
};

const DEFAULT_SOCIALS_LINKS: SocialLink[] = [
  {
    key: "github",
    icon: <Github />,
    link: "/",
  },
  {
    key: "linkedin",
    icon: <Linkedin />,
    link: "/",
  },
];

const SocialLinksArrowAnimation = ({
  links = DEFAULT_SOCIALS_LINKS,
}: SocialLinksArrowAnimationProps) => {
  const [hovered, setHover] = useState<string>("");

  return (
    <div className="flex flex-wrap justify-center gap-4 md:gap-6">
      {links.map((l, index) => (
        <Link
          key={index}
          href={l.link}
          target="_blank"
          rel="noopener noreferrer"
          className="flex bg-gradient-to-br from-gray-500 hover:from-gray-400 to-50% to-neutral-900 p-px rounded-xl overflow-hidden"
          onMouseEnter={() => setHover(l.key)}
          onMouseLeave={() => setHover("")}
        >
          <div className="w-full flex justify-center items-center text-white bg-gradient-to-br from-neutral-900/60 from-35% to-white/5 py-1.5 px-2 md:py-2 md:px-3 rounded-[11px]">
            <AnimatePresence initial={false}>
              {hovered !== l.key && (
                <motion.div
                  key={l.key}
                  initial={{ x: -80, width: 0 }}
                  animate={{ x: 0, width: 20 }}
                  exit={{ x: -80, width: 0 }}
                  transition={{ duration: 0.4 }}
                  className="h-5 flex items-center"
                >
                  {l.icon}
                </motion.div>
              )}
            </AnimatePresence>
            <p className="text-xs md:text-base font-medium capitalize px-2">
              {l.key}
            </p>
            <AnimatePresence>
              {hovered === l.key && (
                <motion.div
                  key="circle-arrow"
                  initial={{ x: 80, width: 0 }}
                  animate={{ x: 0, width: 20 }}
                  exit={{ x: 80, width: 0 }}
                  transition={{ duration: 0.4 }}
                  className="h-5 flex items-center"
                >
                  <CircleArrowRight />
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </Link>
      ))}
    </div>
  );
};

export default SocialLinksArrowAnimation;

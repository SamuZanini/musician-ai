"use client";

import { LayoutGroup, motion } from "motion/react";
import TextRotate from "@/components/fancy/text/text-rotate";

export default function TextComponent() {
  return (
    <div className="w-full text-2xl sm:text-3xl md:text-4xl flex flex-row items-center justify-center font-overused-grotesk text-foreground font-light pt-20 sm:pt-24 md:pt-28 pb-1 sm:pb-1 md:pb-1">
      <LayoutGroup>
        <motion.div className="flex whitespace-pre" layout>
          <motion.span
            className="pt-0.5 sm:pt-1 md:pt-2"
            layout
            transition={{ type: "spring", damping: 30, stiffness: 400 }}
          >
            Learn music{" "}
          </motion.span>
          <TextRotate
            texts={["anytime!", "anywhere!", "right now!"]}
            mainClassName="text-white px-2 sm:px-2 md:px-3 bg-gray-700 overflow-hidden py-0.5 sm:py-1 md:py-2 justify-center rounded-lg"
            staggerFrom={"last"}
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "-120%" }}
            staggerDuration={0.025}
            splitLevelClassName="overflow-hidden pb-0.5 sm:pb-1 md:pb-1"
            transition={{ type: "spring", damping: 30, stiffness: 400 }}
            rotationInterval={2000}
          />
        </motion.div>
      </LayoutGroup>
    </div>
  );
}

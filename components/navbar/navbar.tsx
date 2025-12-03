"use client";

import Link from "next/link";
import React from "react";
import { usePathname } from "next/navigation";

type Props = {
  label: string;
  href: string;
};

export default function CustomLink({ label, href }: Props) {
  const pathname = usePathname();
  const isAboutUs = pathname === "/aboutus";
  const textColor = isAboutUs ? "text-black" : "text-white";

  return (
    <Link href={href}>
      {/* link container */}
      <div className="group h-[40px] p-2 overflow-hidden">
        {/* labels container */}
        <div className="flex flex-col items-center justify-center group-hover:-translate-y-10 transition duration-700">
          <span className={`text-xl font-semibold ${textColor}`}>{label}</span>
          <span className={`text-xl font-semibold ${textColor}`}>{label}</span>
        </div>
      </div>
    </Link>
  );
}

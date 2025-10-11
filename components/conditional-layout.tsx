"use client";

import { usePathname } from "next/navigation";
import {
  SidebarProvider,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebar/app-sidebar";
import { LoginButton } from "@/components/botao/botao-login";

function LayoutContent({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { open } = useSidebar();
  const isLoginPage = pathname === "/login";

  if (isLoginPage) {
    return <div className="min-h-screen w-full">{children}</div>;
  }

  return (
    <div className="flex min-h-screen w-full">
      <AppSidebar />
      <main className="flex-1 flex flex-col">
        <div
          className="fixed top-6 z-[100] transition-all duration-300"
          style={{ left: "1.5rem" }}
        >
          <SidebarTrigger className="h-12 w-12 translate-x-0 data-[state=expanded]:translate-x-64 transition-transform duration-300" />
        </div>
        <div className="fixed top-6 right-6 z-[100] transition-all duration-300">
          <LoginButton />
        </div>
        <div className={`transition-all duration-300 ${open ? "blur-sm" : ""}`}>
          {children}
        </div>
      </main>
    </div>
  );
}

export function ConditionalLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLoginPage = pathname === "/login";

  if (isLoginPage) {
    return <div className="min-h-screen w-full">{children}</div>;
  }

  return (
    <SidebarProvider defaultOpen={false}>
      <LayoutContent>{children}</LayoutContent>
    </SidebarProvider>
  );
}

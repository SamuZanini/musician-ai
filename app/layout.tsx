import { Navbar } from "@/components/navbar/navbar";
import ProviderWrapper from "@/providers/provider-wrapper";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebar/app-sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Musician AI",
  description: "Uma maneira moderna de estudar música",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-no-repeat h-screen w-screen overflow-hidden`}
        style={{
          backgroundImage: "url('/images/maestro.jpg')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <ProviderWrapper>
          <SidebarProvider defaultOpen={false}>
            <div className="flex min-h-screen w-full">
              <AppSidebar />
              <main className="flex-1 flex flex-col">
                <div
                  className="fixed top-6 z-[100] transition-all duration-300"
                  style={{ left: "1.5rem" }}
                >
                  <SidebarTrigger className="h-12 w-12 translate-x-0 data-[state=expanded]:translate-x-64 transition-transform duration-300" />
                </div>
                {children}
              </main>
            </div>
          </SidebarProvider>
        </ProviderWrapper>
      </body>
    </html>
  );
}

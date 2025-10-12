"use client";

import React from "react";
import {
  Dices,
  Notebook,
  PersonStandingIcon,
  Search,
  Settings,
  Signal,
} from "lucide-react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { ModeToggle } from "@/components/tema/mode-toggle";
import { Separator } from "../ui/separator";
import { useAuth } from "@/providers/auth-provider";

// Menu items.
const allItems = [
  {
    title: "Select Your Instrument",
    url: "/selectinstrument",
    icon: Notebook,
    requiresAuth: true,
  },
  {
    title: "Tuning",
    url: "/tuning",
    icon: Dices,
    requiresAuth: false,
  },
  {
    title: "Practice Area",
    url: "/practice",
    icon: Signal,
    requiresAuth: false,
  },
  {
    title: "Music Sheets",
    url: "/musicsheets",
    icon: Search,
    requiresAuth: false,
  },
  {
    title: "My Profile",
    url: "/profile",
    icon: PersonStandingIcon,
    requiresAuth: true,
  },
];

export function AppSidebar() {
  const { isAuthenticated } = useAuth();

  // Filtrar itens baseado no estado de autenticação
  const items = allItems.filter(
    (item) => !item.requiresAuth || (item.requiresAuth && isAuthenticated)
  );

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarHeader className="flex items-left justify-start">
            <ModeToggle enableDirectToggle />
          </SidebarHeader>
          <SidebarHeader>
            <a href="/home">
              <img src="/images/logo-png.png" alt="logo-png" />
            </a>
          </SidebarHeader>
          <SidebarHeader>
            <a href="/home">
              <h1 className="font-bold text-6xl flex justify-center font-italianno">
                #Dô
              </h1>
            </a>
          </SidebarHeader>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item, idx) => (
                <React.Fragment key={item.title}>
                  {idx !== 0 && <Separator className="my-2" />}
                  <SidebarMenuItem>
                    <SidebarMenuButton asChild>
                      <a
                        href={item.url}
                        className="flex items-center gap-2 py-2 px-3 w-full"
                      >
                        <item.icon />
                        <span>{item.title}</span>
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                </React.Fragment>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}

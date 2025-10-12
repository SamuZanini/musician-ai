import { TooltipProvider } from "@/components/ui/tooltip";
import type React from "react";
import { ThemeProvider } from "./theme-provider";
import { AuthProvider } from "./auth-provider";

/**
 * ProviderWrapper: Componente central para gerenciamento de providers da aplicação
 *
 * Este arquivo serve como ponto central para adicionar novos providers.
 * Quando precisar adicionar um novo provider global, adicione-o aqui.
 *
 * Providers atuais:
 * - ThemeProvider: Gerenciamento de tema (claro/escuro)
 * - TooltipProvider: Gerenciamento de tooltips
 * - AuthProvider: Gerenciamento de autenticação
 *
 * Exemplo de uso:
 * Para adicionar um novo provider:
 * 1. Importe o provider
 * 2. Adicione-o envolvendo o componente children
 * 3. Mantenha a ordem adequada de aninhamento
 */
function ProviderWrapper({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <AuthProvider>
        <TooltipProvider>{children}</TooltipProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default ProviderWrapper;

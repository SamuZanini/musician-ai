import { TooltipProvider } from '@/components/ui/tooltip'
import React from 'react'
import { ThemeProvider } from './theme-provider'

/**
 * ProviderWrapper: Componente central para gerenciamento de providers da aplicação
 * 
 * Este arquivo serve como ponto central para adicionar novos providers.
 * Quando precisar adicionar um novo provider global, adicione-o aqui.
 * 
 * Providers atuais:
 * - ThemeProvider: Gerenciamento de tema (claro/escuro)
 * - TooltipProvider: Gerenciamento de tooltips
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
      <TooltipProvider>{children}</TooltipProvider>
    </ThemeProvider>
  )
}

export default ProviderWrapper

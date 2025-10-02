# Create Chico App

Uma maneira moderna de iniciar projetos Next.js com configurações pré-definidas e componentes úteis.

## Características

- 🏃‍♂️ Next.js 15 com App Router e Turbopack
- 💨 Tailwind V4 para estilização
- 🎨 Tema claro/escuro com next-themes
- 🧱 Componentes shadcn/ui pré-configurados
- 🎯 Tipagem forte com TypeScript
- 🧹 Formatação com Biome

## Início Rápido

```bash
bunx --use-bun create-chico-app
cd meu-projeto
bun install
bun dev
```

Abra [http://localhost:3000](http://localhost:3000) no seu navegador para ver o resultado.

## Adicionando Componentes shadcn/ui

⚠️ **Importante**: Ao adicionar novos componentes do shadcn/ui, sempre use a flag `@canary`:

```bash
bunx --bun shadcn@canary add button
```

Não use `@latest`, pois pode causar incompatibilidades com as versões mais recentes do Next.js e Tailwind CSS.

## Estrutura do Projeto

```
├── app/                # Rotas e páginas
├── components/         # Componentes React
│   ├── ui/            # Componentes shadcn/ui
│   └── magicui/       # Componentes com efeitos especiais
├── providers/         # Providers React (tema, etc)
└── lib/              # Utilitários e configurações
```

## Providers Disponíveis

O projeto já vem com os seguintes providers configurados:

- `ThemeProvider`: Gerenciamento de tema (claro/escuro)
- `TooltipProvider`: Gerenciamento de tooltips

Para adicionar novos providers, utilize o arquivo `providers/provider-wrapper.tsx`.

## Scripts Disponíveis

- `bun dev`: Inicia o servidor de desenvolvimento
- `bun build`: Gera a build de produção
- `bun start`: Inicia o servidor de produção
- `bun lint`: Executa a verificação de linting

## Aprenda Mais

Para saber mais sobre as tecnologias utilizadas:

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind V4](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com)
- [Bun Runtime](https://bun.sh)

## Deploy

A maneira mais fácil de fazer deploy é usando a [Plataforma Vercel](https://vercel.com/new). Confira a [documentação de deploy do Next.js](https://nextjs.org/docs/app/building-your-application/deploying) para mais detalhes.

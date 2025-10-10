import { ArrowRightIcon } from "@radix-ui/react-icons";

import { cn } from "@/lib/utils";
import { AnimatedShinyText } from "../ui/animated-shiny-text";

interface AnimatedShinyTextDemoProps {
  onClick?: () => void;
}

export function AnimatedShinyTextDemo({ onClick }: AnimatedShinyTextDemoProps) {
  const handleClick = () => {
    console.log("Evento de clique recebido no botão");
    onClick?.();
  };

  return (
    <div className="z-30 flex min-h-64 items-center justify-center">
      <button
        className={cn(
          "group relative z-30 rounded-full border border-black/5 bg-neutral-100 text-base text-white transition-all ease-in hover:cursor-pointer hover:bg-neutral-200 dark:border-white/5 dark:bg-neutral-900 dark:hover:bg-neutral-800"
        )}
        onClick={onClick}
        type="button"
      >
        <AnimatedShinyText className="inline-flex items-center justify-center px-4 py-1 transition ease-out hover:text-neutral-600 hover:duration-300 hover:dark:text-neutral-400">
          <span>🎶 Get Started</span>
          <ArrowRightIcon className="ml-1 size-3 transition-transform duration-300 ease-in-out group-hover:translate-x-0.5" />
        </AnimatedShinyText>
      </button>
    </div>
  );
}

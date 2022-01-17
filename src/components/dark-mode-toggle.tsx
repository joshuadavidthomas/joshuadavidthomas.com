import { FunctionComponent, useEffect, useState } from "react";
import { Switch } from "@headlessui/react";
import { useTheme } from "next-themes";
import clsx from "clsx";
import { MoonIcon, SunIcon } from "@heroicons/react/solid";

interface ToggleProps {
  className?: string;
}

const Toggle: FunctionComponent<ToggleProps> = ({ className }) => {
  const { theme, setTheme } = useTheme();
  const [enabled, setEnabled] = useState(theme === "dark");
  const [mounted, setMounted] = useState(false);

  const handleToggle = () => {
    setEnabled(!enabled);
    setTheme(theme === "dark" ? "light" : "dark");
  };

  useEffect(() => {
    setMounted(true);

    console.log("theme", theme);
    console.log("enabled", enabled);
  }, [theme, enabled]);

  if (!mounted) return <div className="h-6 w-11"></div>;

  return (
    <Switch
      checked={enabled}
      onChange={handleToggle}
      className={clsx(
        !enabled ? "bg-gray-200" : "bg-gray-700",
        "relative inline-flex shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500",
        className
      )}
    >
      <span className="sr-only">Use setting</span>
      <span
        className={clsx(
          !enabled ? "translate-x-5" : "translate-x-0",
          "pointer-events-none shadow relative inline-block h-5 w-5 rounded-full bg-white dark:bg-gray-100 ring-0 transition ease-in-out duration-200"
        )}
      >
        <span
          className={clsx(
            !enabled
              ? "opacity-0 ease-out duration-100"
              : "opacity-100 ease-in duration-200",
            "absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
          )}
          aria-hidden="true"
        >
          <MoonIcon className="w-3 h-3 text-indigo-500" />
        </span>
        <span
          className={clsx(
            !enabled
              ? "opacity-100 ease-in duration-200"
              : "opacity-0 ease-out duration-100",
            "absolute inset-0 h-full w-full flex items-center justify-center transition-opacity"
          )}
          aria-hidden="true"
        >
          <SunIcon className="w-3 h-3 text-orange-400" />
        </span>
      </span>
    </Switch>
  );
};

export default Toggle;

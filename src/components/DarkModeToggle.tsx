import { FunctionComponent, useEffect, useState } from "react";
import { Switch } from "@headlessui/react";
import clsx from "clsx";
import { MoonIcon, SunIcon } from "@heroicons/react/solid/index.js";

const themes = [
  { name: "Light", value: "light" },
  { name: "Dark", value: "dark" },
  { name: "System", value: "system" },
];

interface ToggleProps {
  className?: string;
}

const Toggle: FunctionComponent<ToggleProps> = ({ className }) => {
  let [selectedTheme, setSelectedTheme] = useState("");

  function getThemeFromDocument() {
    const theme = document.documentElement.getAttribute("data-theme");
    if (theme) {
      return theme;
    }
    return "light";
  }

  useEffect(() => {
    if (selectedTheme.length !== 0) {
      document.documentElement.setAttribute("data-theme", selectedTheme);
    } else {
      setSelectedTheme(
        // @ts-ignore
        themes.find(
          (theme) =>
            theme.value === document.documentElement.getAttribute("data-theme")
        ).value
      );
    }
  }, [selectedTheme]);
  
  const enabled = selectedTheme === "dark";

  return (
    <Switch
      checked={enabled}
      onChange={() => {
        const newTheme = enabled ? themes[0] : themes[1];
        setSelectedTheme(newTheme.value);
        localStorage.setItem("theme", newTheme.value);
      }}
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

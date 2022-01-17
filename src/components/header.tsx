import { FunctionComponent } from "react";
import Link from "next/link";

import DarkModeToggle from "./dark-mode-toggle";
import GitHubIcon from "./icons/github";
import LinkedInIcon from "./icons/linkedin";

interface HeaderProps {}

const Header: FunctionComponent<HeaderProps> = () => {
  return (
    <header className="flex items-center justify-between py-8">
      <nav className="flex items-center space-x-4 text-lg font-semibold">
        <h1>
          <Link href="/">
            <a className="hover:text-gray-500 dark:hover:text-gray-300">home</a>
          </Link>
        </h1>
        <Link href="/snippets">
          <a className="hover:text-gray-500 dark:hover:text-gray-300">
            snippets
          </a>
        </Link>
      </nav>
      <div className="flex items-center space-x-4 last:ml-8">
        <a href="https://github.com/joshuadavidthomas" target="_blank">
          <GitHubIcon />
        </a>
        <a
          href="https://www.linkedin.com/in/joshua-thomas-b1745a16/"
          className="pr-3"
          target="_blank"
        >
          <LinkedInIcon />
        </a>
        <DarkModeToggle />
      </div>
    </header>
  );
};

export default Header;

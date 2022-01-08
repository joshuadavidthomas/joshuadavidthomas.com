import { FunctionComponent } from "react";
import Link from "next/link";

import Container from "./container";
import Toggle from "./dark-mode-toggle";
import GitHubIcon from "./icons/github";
import LinkedInIcon from "./icons/linkedin";

interface HeaderProps {}

const Header: FunctionComponent<HeaderProps> = () => {
  return (
    <Container>
      <header className="flex items-center justify-between py-8 text-gray-800 dark:text-gray-100">
        <h1 className="font-mono text-xl font-bold hover:text-gray-500 dark:hover:text-gray-300">
          <Link href="/">joshthomas.dev</Link>
        </h1>
        <div className="flex items-center space-x-4 last:ml-8">
          <a href="https://github.com/joshuadavidthomas">
            <GitHubIcon />
          </a>
          <a href="https://www.linkedin.com/in/joshua-thomas-b1745a16/" className="pr-3">
            <LinkedInIcon />
          </a>
          <Toggle />
        </div>
      </header>
    </Container>
  );
};

export default Header;

import { FunctionComponent, useEffect } from "react";
import Link from "next/link";
import { MenuIcon, XIcon } from "@heroicons/react/solid";
import { Disclosure, Transition } from "@headlessui/react";
import clsx from "clsx";

import DarkModeToggle from "./dark-mode-toggle";
import MobileMenu from "./mobile-menu";
import GitHubIcon from "./icons/github";
import LinkedInIcon from "./icons/linkedin";

const navigation = [
  {
    label: "home",
    href: "/",
  },
  {
    label: "snippets",
    href: "/snippets",
  },
];
const social = [
  {
    label: "github",
    href: "https://github.com/joshuadavidthomas",
    icon: (
      <GitHubIcon className="hover:text-gray-800 dark:hover:text-gray-300" />
    ),
  },
  {
    label: "linkedin",
    href: "https://www.linkedin.com/in/joshua-thomas-b1745a16/",
    icon: (
      <LinkedInIcon className="hover:text-gray-800 dark:hover:text-gray-300" />
    ),
  },
];

interface HeaderProps {}

const Header: FunctionComponent<HeaderProps> = () => {
  useEffect(() => {
    console.log(navigation.length + 1);
  }, []);
  return (
    <Disclosure>
      {({ open }) => (
        <header className="py-8 text-lg font-semibold">
          <div className="flex items-center justify-between">
            <div className="flex items-center sm:hidden">
              <Disclosure.Button title="Mobile Menu">
                {open ? (
                  <XIcon className="w-6 h-6" />
                ) : (
                  <MenuIcon className="w-6 h-6" />
                )}
              </Disclosure.Button>
            </div>
            <nav className="items-center hidden space-x-4 sm:flex">
              {navigation.map(({ label, href }) => (
                <Link key={label} href={href}>
                  <a className="hover:underline">{label}</a>
                </Link>
              ))}
            </nav>
            <div className="flex items-center space-x-10">
              <div className="items-center hidden space-x-4 sm:flex">
                {social.map(({ label, href, icon }) => (
                  <a key={label} href={href} className="hover:underline">
                    {icon}
                  </a>
                ))}
              </div>
              <div className="flex items-center">
                <DarkModeToggle />
              </div>
            </div>
          </div>
          <Transition>
            <div className="py-6 mt-4 space-y-6 bg-gray-200 shadow-inner dark:bg-gray-700 full-width">
              <Disclosure.Panel className="flex flex-col items-center space-y-2">
                {navigation.map((item, index) => (
                  <Transition.Child
                    enter="transition ease-out"
                    enterFrom="transform -translate-y-4 opacity-0"
                    enterTo="transform translate-y-0 opacity-100"
                    leave="transition duration-75 ease-out"
                    leaveFrom="transform scale-100 opacity-100"
                    leaveTo="transform scale-95 opacity-0"
                    style={
                      open
                        ? { transitionDelay: `${(index + 1) * 100}ms` }
                        : null
                    }
                  >
                    <Disclosure.Button key={item.label} as="a" href={item.href}>
                      {item.label}
                    </Disclosure.Button>
                  </Transition.Child>
                ))}
              </Disclosure.Panel>
              <Transition.Child
                enter="transition ease-out"
                enterFrom="transform -translate-y-4 opacity-0"
                enterTo="transform translate-y-0 opacity-100"
                leave="transition duration-75 ease-out"
                leaveFrom="transform scale-100 opacity-100"
                leaveTo="transform scale-95 opacity-0"
                style={
                  open
                    ? {
                        transitionDelay: `${(navigation.length + 1) * 100}ms`,
                      }
                    : null
                }
              >
                <div className="flex items-center justify-center space-x-4">
                  {social.map((item) => (
                    <Disclosure.Button
                      key={item.label}
                      as="a"
                      href={item.href}
                      target="_blank"
                    >
                      {item.icon}
                    </Disclosure.Button>
                  ))}
                </div>
              </Transition.Child>
            </div>
          </Transition>
        </header>
      )}
    </Disclosure>
  );
};

export default Header;

import type { FC } from "react";

import { Popover } from "@headlessui/react";
import { motion, AnimatePresence } from "framer-motion";
import { MenuIcon, XIcon } from "@heroicons/react/solid/index.js";
import clsx from "clsx";

interface MenuMobileProps {
  navigation: {
    title: string;
    url: string;
  }[];
}

const MenuMobile: FC<MenuMobileProps> = ({ navigation }) => {
  return (
    <Popover>
      {({ open, close }) => (
        <div className="sm:hidden">
          <Popover.Button
            className={clsx(
              open
                ? "border-gray-300 bg-gray-100 text-gray-700"
                : "border-gray-50/60 bg-gray-700/40 text-gray-100 backdrop-blur-sm",
              "relative z-50 flex items-center border p-2 text-xs font-medium uppercase lg:hidden"
            )}
          >
            {open ? (
              <>
                <XIcon className="w-6 h-6 mr-2" />
                <span>Close</span>
              </>
            ) : (
              <>
                <MenuIcon className="w-6 h-6 mr-2" />
                <span>Menu</span>
              </>
            )}
          </Popover.Button>
          <AnimatePresence initial={false}>
            {open && (
              <>
                <Popover.Overlay
                  static
                  as={motion.div}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="fixed inset-0 z-30 bg-gray-300/20 backdrop-blur"
                />
                <Popover.Panel
                  static
                  as={motion.div}
                  initial={{ opacity: 0, y: -32 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{
                    opacity: 0,
                    y: -32,
                    transition: { duration: 0.2 },
                  }}
                  className="absolute inset-x-0 top-0 z-40 px-4 pb-6 text-gray-900 origin-top bg-white shadow-2xl pt-28 dark:bg-gray-700 shadow-gray-900/20 dark:text-gray-50"
                >
                  <ul className="space-y-4">
                    {navigation.map((item) => (
                      <li key={`${item.title}-${item.url}`}>
                        <a href={item.url}>{item.title}</a>
                      </li>
                    ))}
                  </ul>
                  <Popover.Button className="flex items-center justify-center w-full py-2 mt-12 text-gray-700 bg-gray-100 border border-gray-300">
                    <span className="text-sm font-medium uppercase">Close</span>
                    <XIcon className="block w-5 h-5 ml-2" aria-hidden="true" />
                  </Popover.Button>
                </Popover.Panel>
              </>
            )}
          </AnimatePresence>
        </div>
      )}
    </Popover>
  );
};

export default MenuMobile;

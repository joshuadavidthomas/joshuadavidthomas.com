import { Fragment, FunctionComponent, useState } from "react";
import { MenuIcon, XIcon } from "@heroicons/react/solid";
import { Disclosure, Transition } from "@headlessui/react";

interface MobileMenuProps {
  navItems: any;
  socialItems: any;
}

const MobileMenu: FunctionComponent<MobileMenuProps> = ({ navItems, socialItems }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
    document.body.style.overflow = isOpen ? "" : "hidden";
  };
  return (
    <Disclosure>
      {({ open }) => (
        <>
          <Disclosure.Button onClick={toggleMenu} title="Mobile Menu">
            {open ? (
              <XIcon className="w-6 h-6" />
            ) : (
              <MenuIcon className="w-6 h-6" />
            )}
          </Disclosure.Button>
          <Transition
            enter="transition duration-100 ease-out"
            enterFrom="transform scale-95 opacity-0"
            enterTo="transform scale-100 opacity-100"
            leave="transition duration-75 ease-out"
            leaveFrom="transform scale-100 opacity-100"
            leaveTo="transform scale-95 opacity-0"
          >
            <Disclosure.Panel>
              <div>Menu</div>
              {navItems.map((item) => (
                <Disclosure.Button key={item.label} as="a" href={item.href}>
                  {item.label}
                </Disclosure.Button>
              ))}
            </Disclosure.Panel>
            <div className="flex items-center justify-center space-x-2">
              {socialItems.map((item) => (
                <Disclosure.Button key={item.label} as="a" href={item.href} target="_blank">
                  {item.icon}
                </Disclosure.Button>
              ))}
            </div>
          </Transition>
        </>
      )}
    </Disclosure>
  );
};

export default MobileMenu;

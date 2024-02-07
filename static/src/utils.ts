import type { SvelteComponent } from "svelte";

type ComponentConstructor<T = any> = new (options: {
  target: Element;
  props?: T;
}) => SvelteComponent;

// Optionally accept a function to generate props from a target element.
export function mountSvelteComponents<T = any>(
  componentName: string,
  ComponentClass: ComponentConstructor<T>,
  getProps?: (target: Element) => T,
): void {
  document.addEventListener("DOMContentLoaded", () => {
    const targets = document.querySelectorAll(
      `[data-component="${componentName}"]`,
    );

    targets.forEach((target) => {
      // Generate props using the provided function, or default to undefined if no function is provided.
      const props = getProps ? getProps(target) : undefined;

      new ComponentClass({
        target,
        props,
      });
    });
  });
}

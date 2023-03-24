interface Options {
  dirname: string;
  layout: string;
}

export function defaultLayoutPlugin(options: Options[]) {
  return function (tree: any, file: any) {
    const NO_LAYOUT_SET =
      typeof file.data.astro.frontmatter.layout === "undefined" ||
      file.data.astro.frontmatter.layout === null;

    if (NO_LAYOUT_SET) {
      const layout = options.find((option) => {
        if (
          file.dirname.endsWith(option.dirname) ||
          file.dirname.includes(option.dirname)
        ) {
          return option.layout;
        }
      });

      if (layout) {
        file.data.astro.frontmatter.layout = `/src/layouts/${layout}`;
      } else {
        file.data.astro.frontmatter.layout = `/src/layouts/Layout.astro`;
      }
    }
  };
}

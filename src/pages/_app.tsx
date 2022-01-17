import { AppProps } from "next/app";
import { FunctionComponent } from "react";
import { ThemeProvider } from "next-themes";
import { MDXProvider } from "@mdx-js/react";
import "../../assets/css/styles.css";
import Head from "next/head";

const components = {
  pre: (props) => (
    <pre className={`lg:container-breakout text-sm lg:text-base ` + props.className}>
      {props.children}
    </pre>
  ),
};

const App: FunctionComponent<AppProps> = ({ Component, pageProps }) => {
  return (
    <>
      <Head>
        {/* https://nextjs.org/docs/messages/no-document-viewport-meta */}
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <ThemeProvider attribute="class" enableSystem={true}>
        <MDXProvider components={components}>
          <Component {...pageProps} />
        </MDXProvider>
      </ThemeProvider>
    </>
  );
};

export default App;

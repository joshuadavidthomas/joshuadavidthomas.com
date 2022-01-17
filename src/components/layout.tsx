import { FunctionComponent } from "react";
import Head from "next/head";

import Header from "./header";
import config from "../config";

interface LayoutProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

const Layout: FunctionComponent<LayoutProps> = ({
  title,
  description,
  children,
}) => {
  return (
    <>
      <Head>
        <title>
          {title} | {config.title}
        </title>
        {description ? <meta name="description" content={description} /> : <meta name="description" content={config.description} />}
      </Head>
      <Header />
      <main className="mx-auto max-w-prose">{children}</main>
    </>
  );
};

export default Layout;

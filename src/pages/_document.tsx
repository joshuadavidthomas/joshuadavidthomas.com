import Document, { Html, Head, Main, NextScript } from "next/document";
import Container from "@/components/container";

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>
          <meta charSet="utf-8" />
          <link
            rel="apple-touch-icon"
            sizes="180x180"
            href="/apple-touch-icon.png"
          />
          <link
            rel="icon"
            type="image/png"
            sizes="32x32"
            href="/favicon-32x32.png"
          />
          <link
            rel="icon"
            type="image/png"
            sizes="16x16"
            href="/favicon-16x16.png"
          />
          <link rel="manifest" href="/site.webmanifest" />
          <script defer data-domain="joshthomas.dev" src="https://bloodhound.joshthomas.dev/js/plausible.js"></script>
        </Head>
        <body className="text-gray-800 dark:text-gray-100 bg-gray-50 dark:bg-gray-800">
          <Container>
            <Main />
          </Container>
          <NextScript />
        </body>
      </Html>
    );
  }
}

import Document, { Html, Head, Main, NextScript } from 'next/document'

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head />
        <body className="px-4 text-gray-900 dark:text-gray-50 bg-gray-50 dark:bg-gray-800">
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  };
};
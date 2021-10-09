import Document, { Html, Head, Main, NextScript } from 'next/document'

export default class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head />
        <body className="px-4 mx-auto text-gray-900 bg-gray-50 max-w-prose">
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}
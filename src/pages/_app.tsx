import { AppProps } from "next/app";
import { FunctionComponent } from "react";
import { ThemeProvider } from "next-themes";
import "../../assets/css/styles.css";

const App: FunctionComponent<AppProps> = ({ Component, pageProps }) => {
  return (
    <ThemeProvider attribute="class" enableSystem={true}>
      <Component {...pageProps} />
    </ThemeProvider>
  );
};

export default App;

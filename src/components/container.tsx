import { FunctionComponent } from "react";

interface ContainerProps {
  children?: React.ReactNode;
}

const Container: FunctionComponent<ContainerProps> = ({ children }) => {
  return <div className="container px-2 mx-auto">{children}</div>;
};

export default Container;

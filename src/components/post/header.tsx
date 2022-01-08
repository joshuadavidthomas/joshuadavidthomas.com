import { FunctionComponent } from 'react';
import DateFormatter from "../date-formatter";
import PostTitle from "./title";

interface HeaderProps {
  title: string;
  date: string;
}

const Header: FunctionComponent<HeaderProps> = ({ title, date }) => {
  return (
    <>
      <PostTitle>{title}</PostTitle>
      <div className="max-w-2xl mx-auto">
        <div className="mb-6 text-lg">
          <DateFormatter dateStr={date} />
        </div>
      </div>
    </>
  );
};

export default Header;

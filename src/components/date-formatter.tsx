import { FunctionComponent } from "react";
import { format, parseISO } from "date-fns";

interface DateFormatterProps {
  dateStr: string;
}

const DateFormatter: FunctionComponent<DateFormatterProps> = ({ dateStr }) => {
  const dateObj = parseISO(dateStr);
  const formattedDate = format(dateObj, "MMMM d, yyyy");
  
  return <time dateTime={dateStr}>{formattedDate}</time>;
};

export default DateFormatter;

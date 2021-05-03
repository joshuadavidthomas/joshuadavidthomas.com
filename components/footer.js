export default function Footer() {
  return (
    <footer className="flex flex-col items-center justify-center w-full h-32 border-t border-gray-300">
      <a
      className="flex items-center justify-center"
        href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
        target="_blank"
        rel="noopener noreferrer"
      >
        Powered by <img className="w-20 h-20 ml-2" src="/vercel.svg" alt="Vercel Logo" />
      </a>
    </footer>
  );
}

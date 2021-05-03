import Layout from "../components/layout";
import Content from "../components/content";

export default function Home() {
  return (
    <>
      <Layout title="Joshua David Thomas">
        <div className="container mx-auto sm:py-20">
            <div className="flex items-center py-10">
              <img src="/me.png" className="mx-auto rounded-full shadow-md" />
            </div>
          <div className="prose lg:prose-xl">
            <p className="lead">
              👋 Hi, my name is Josh. I am the web developer at{" "}
              <a
                className="hover:text-[#050]"
                href="https://www.westervelt.com"
              >
                The Westervelt Company
              </a>{" "}
              in Tuscaloosa, AL.
            </p>
            <p>I use Python and Django to make things on the web.</p>
            <p>If you want, you can say <a className="hover:text-[#050]" href="mailto:hello@joshuadavidthomas.com">hello</a>.</p>
          </div>
        </div>
      </Layout>
    </>
  );
}

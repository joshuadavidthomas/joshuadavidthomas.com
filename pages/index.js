import Layout from "../components/layout";
import Content from "../components/content";

export default function Home() {
  return (
    <>
      <Layout title="Joshua David Thomas">
        <div className="container py-20 mx-auto">
            <div className="flex items-center py-10">
              <img src="/me.png" className="mx-auto rounded-full shadow-md" />
            </div>
          <div className="prose lg:prose-xl">
            <p className="lead">
              👋 Hi, my name is Josh. I am the web developer at{" "}
              <a
                className="hover:text-blue-600"
                href="https://www.westervelt.com"
              >
                The Westervelt Company
              </a>{" "}
              in Tuscaloosa, AL.
            </p>
            <p>I enjoy using Python and Django to make things.</p>
          </div>
        </div>
      </Layout>
    </>
  );
}

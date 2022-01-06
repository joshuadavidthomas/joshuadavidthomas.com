import type { NextPage } from 'next'
import Image from 'next/image'
import Layout from "../components/layout"

const Home: NextPage = () => {
  return (
    <>
      <Layout title="Joshua David Thomas">
        <div className="container pb-10 mx-auto sm:py-20">
            <div className="flex items-center justify-center py-10">
              <Image src="/me.png" width="250" height="250" alt="A picture of Josh" className="rounded-full shadow-md" />
            </div>
          <div className="prose lg:prose-xl">
            <p className="lead">
              👋 Hi, my name is Josh. I am a web developer in Tuscaloosa, AL.
            </p>
            <p>I use Python and Django to make things on the web.</p>
            <p>If you want, you can say <a className="hover:text-[#050]" href="mailto:hello@joshuadavidthomas.com">hello</a>.</p>
          </div>
        </div>
      </Layout>
    </>
  );
}

export default Home

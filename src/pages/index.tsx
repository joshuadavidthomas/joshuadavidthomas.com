import { FunctionComponent } from "react";
import Image from "next/image";

import Layout from "@/components/layout";

interface IndexProps {}

const Index: FunctionComponent<IndexProps> = () => {
  return (
    <Layout title="Joshua David Thomas">
      <div className="container max-w-2xl mx-auto">
        <section className="pb-10 mx-auto sm:pt-10 sm:pb-40">
          <div className="flex items-center justify-center py-10">
            <Image
              src="/me.png"
              width="250"
              height="250"
              alt="A picture of Josh"
              className="rounded-full shadow-md"
            />
          </div>
          <h1 className="text-3xl md:text-5xl leading-tighter">
            👋
            <span className="pl-2 font-bold tracking-wide">
              Hi, my name is Josh.
            </span>
          </h1>
          <p className="pt-2 text-lg font-medium md:pt-4 md:text-2xl">
            I am a web developer in Tuscaloosa, AL.
          </p>
          <div className="pt-4 space-y-1">
            <p>I use Python and Django to make things on the web.</p>
            <p>
              If you want, you can say{" "}
              <a
                className="hover:text-[#050] hover:underline"
                href="mailto:hello@joshuadavidthomas.com"
              >
                ✉ hello
              </a>
              .
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Index;

import { FunctionComponent, useEffect } from "react";
import { GetStaticProps } from "next";

import Layout from "@/components/layout";
import { getAllSnippetsByCategory, getAllSnippets } from "@/lib/snippets";
import DjangoIcon from "@/components/icons/django";

export const getStaticProps: GetStaticProps = async () => {
  const allSnippetsByCategory = getAllSnippetsByCategory([
    "title",
    "date",
    "slug",
    "description",
  ]);
  const allSnippets = getAllSnippets([
    "date",
    "category",
    "slug",
    "title",
    "description",
  ]);

  return {
    props: {
      allSnippets: allSnippetsByCategory,
      latestSnippet: allSnippets.reverse()[0],
    },
  };
};

interface SnippetsProps {
  allSnippets: any;
  latestSnippet: any;
}

const Snippets: FunctionComponent<SnippetsProps> = ({
  allSnippets,
  latestSnippet,
}) => {
  useEffect(() => {
    console.log("Snippets");
    console.log(allSnippets);
  }, [allSnippets]);

  return (
    <Layout title="Snippets">
      <h1 className="text-3xl font-bold">Code Snippets</h1>
      <p className="pt-2 text-lg">
        Here are some code snippets I've found useful.
      </p>
      <section className="pt-6 space-y-4">
        {allSnippets.map((category) => (
          <section key={category.category}>
            <h3 className="flex items-center text-lg font-medium capitalize">
              {category.category === "django" ? <DjangoIcon className="mr-2" /> : null}
              {category.category}
            </h3>
            <ul>
              {category.snippets.map((snippet) => (
                <li key={snippet.slug}>
                  <a
                    href={`/snippets/${category.category}/${snippet.slug}`}
                    className="hover:underline"
                  >
                    {snippet.title}
                  </a>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </section>
    </Layout>
  );
};

export default Snippets;

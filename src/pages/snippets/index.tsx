import { FunctionComponent } from "react";
import { GetStaticProps } from "next";

import Layout from "@/components/layout";
import { getAllSnippetsByCategory, getAllSnippets } from "@/lib/snippets";
import DjangoIcon from "@/components/icons/django";
import GitIcon from "@/components/icons/git";

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
  return (
    <Layout title="Snippets" description="Some useful code snippets">
      <h1 className="text-3xl font-bold">Code Snippets</h1>
      <p className="pt-2 text-lg">
        Here are some code snippets I've found useful.
      </p>
      <section className="pt-8 space-y-6">
        {allSnippets.map((category) => (
          <section key={category.category}>
            <h3 className="flex items-center text-lg font-medium capitalize">
              {category.category === "django" ? (
                <DjangoIcon className="mr-2" />
              ) : category.category === "git" ? (
                <GitIcon className="mr-2" />
              ) : null}
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

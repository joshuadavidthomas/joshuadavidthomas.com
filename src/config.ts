import MastodonIcon from "./components/IconMastodon.astro";
import GitHubIcon from "./components/IconGitHub.astro";
import LinkedInIcon from "./components/IconLinkedIn.astro";

interface Config {
  title: string;
  navigation: {
    title: string;
    url: string;
  }[];
  social: {
    title: string;
    url: string;
    Icon: any;
  }[];
  blogCollections: string[];
}

const config: Config = {
  title: "joshthomas.dev",
  navigation: [
    {
      title: "Home",
      url: "/",
    },
    {
      title: "Blog",
      url: "/blog",
    },
  ],
  social: [
    {
      title: "Mastodon",
      url: "https://joshthomas.dev/@josh",
      Icon: MastodonIcon,
    },
    {
      title: "GitHub",
      url: "https://github.com/joshuadavidthomas",
      Icon: GitHubIcon,
    },
    {
      title: "LinkedIn",
      url: "https://www.linkedin.com/in/joshua-thomas-b1745a16/",
      Icon: LinkedInIcon,
    },
  ],
  blogCollections: ["til"],
};

export default config;

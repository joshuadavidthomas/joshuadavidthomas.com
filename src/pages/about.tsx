import { FunctionComponent } from 'react';
import Layout from '@/components/layout';

interface AboutProps {}
 
const About: FunctionComponent<AboutProps> = () => {
  return (
    <Layout title="About">
      <h1>About</h1>
    </Layout>
  );
}
 
export default About;
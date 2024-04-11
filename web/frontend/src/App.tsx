import { TRIApp } from '@toyota-research-institute/rse-react-library2';
import '@toyota-research-institute/rse-react-library/style.css';
import config from './tri.app.config';
import Prelogin from '@/pages/pre-login/pre-login';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TRIApp config={config} PreloginPage={<Prelogin />} />
  </QueryClientProvider>
);

export default App;

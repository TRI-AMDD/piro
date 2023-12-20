import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CognitoProvider from '@/features/cognito/cognito-hosted';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import './index.css';

const queryClient = new QueryClient();
const Home = lazy(() => import('@/pages/Home/Home'));
const About = lazy(() => import('@/pages/About/About'));

const App = () => (
  <QueryClientProvider client={queryClient}>
    <CognitoProvider>
      <BrowserRouter>
        <div className="app">
          <Header />
          <div className="appbody">
          <Suspense fallback={<div>Loading...</div>}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </Suspense>
          </div>
          <Footer />
        </div>
      </BrowserRouter>
    </CognitoProvider>
  </QueryClientProvider>
);

export default App;

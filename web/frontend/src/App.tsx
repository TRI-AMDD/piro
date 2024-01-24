import { Suspense, lazy, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CognitoProvider from '@/features/cognito/cognito-hosted';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import FeedbackButton from '@/components/FeedbackButton';
import './index.css';
import './fonts.css';

const queryClient = new QueryClient();
const Home = lazy(() => import('@/pages/Home/Home'));
const About = lazy(() => import('@/pages/About/About'));

const App: React.FC = () => {
  const [highlightedParagraph, setHighlightedParagraph] = useState<string | null>(null);
  const highlight = (id: string | null) => {
    setHighlightedParagraph(id);
  };
  return (
    <QueryClientProvider client={queryClient}>
      <CognitoProvider>
        <BrowserRouter>
          <div className="app">
            <Header />
            <div className="appbody">
              <Suspense fallback={<div>Loading...</div>}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route
                    path="/about"
                    element={<About highlightedParagraph={highlightedParagraph} highlight={highlight} />}
                  />
                </Routes>
              </Suspense>
            </div>
            <Footer highlight={highlight} />
            <FeedbackButton showFeedbackButton={true} />
          </div>
        </BrowserRouter>
      </CognitoProvider>
    </QueryClientProvider>
  );
};

export default App;

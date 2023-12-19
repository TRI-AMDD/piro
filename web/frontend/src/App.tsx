import { Suspense, lazy, useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Header from './components/Header';
import Footer from './components/Footer';
import CognitoProvider from './CognitoHosted';

const queryClient = new QueryClient();
const Home = lazy(() => import('./pages/Home/Home'));
const About = lazy(() => import('./pages/About/About'));


const App: React.FC = () => {
    const [highlightedParagraph, setHighlightedParagraph] = useState<string | null>(null);
    const highlight =(id: string | null) =>{
            setHighlightedParagraph(id);
        }
    return(
    <QueryClientProvider client={queryClient}>
        <Router>
            <CognitoProvider>
                    <Header />
                    <div className="app">
                        <Suspense fallback={<div>Loading...</div>}>
                            <Switch>
                                <Route exact path="/" component={Home} />
                                <Route exact path="/about">
                                    <About highlightedParagraph={highlightedParagraph} highlight={highlight}/>
                                </Route>
                            </Switch>
                        </Suspense>
                        </div>
                    <Footer highlight={highlight} />
            </CognitoProvider>
        </Router>
    </QueryClientProvider>
    );
};

export default App;

import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Header from './components/Header';
import Footer from './components/Footer';
import CognitoProvider from './CognitoHosted';

const queryClient = new QueryClient();
const Home = lazy(() => import('./pages/Home/Home'));
const About = lazy(() => import('./pages/About/About'));

const App = () => (
    <QueryClientProvider client={queryClient}>
        <Router>
            <CognitoProvider>
                    <Header />
                    <div className="app">
                        <Suspense fallback={<div>Loading...</div>}>
                            <Switch>
                                <Route exact path="/" component={Home} />
                                <Route exact path="/about" component={About} />
                            </Switch>
                        </Suspense>
                        </div>
                    <Footer />
            </CognitoProvider>
        </Router>
    </QueryClientProvider>
);

export default App;

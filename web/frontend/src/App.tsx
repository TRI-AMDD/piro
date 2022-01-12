import { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Header from './components/Header';
import Footer from './components/Footer';
import AmplifySetup from './components/AmplifySetup';

const queryClient = new QueryClient();
const Home = lazy(() => import('./pages/Home/Home'));
const About = lazy(() => import('./pages/About/About'));

const App = () => (
    <QueryClientProvider client={queryClient}>
        <Router>
            <AmplifySetup>
                <div className="app">
                    <Header />
                        <Suspense fallback={<div>Loading...</div>}>
                            <Switch>
                                <Route exact path="/" component={Home} />
                                <Route exact path="/about" component={About} />
                            </Switch>
                        </Suspense>
                    <Footer />
                </div>
            </AmplifySetup>
        </Router>
    </QueryClientProvider>
);

export default App;

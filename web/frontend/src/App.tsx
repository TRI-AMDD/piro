import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient();
const Home = lazy(() => import('./pages/Home/Home'));

const App = () => (
    <QueryClientProvider client={queryClient}>
        <Router>
            <Suspense fallback={<div>Loading...</div>}>
                <Switch>
                    <Route exact path="/" component={Home} />
                </Switch>
            </Suspense>
        </Router>
    </QueryClientProvider>
);

export default App;

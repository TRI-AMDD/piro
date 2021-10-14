import React, { Suspense, lazy } from 'react';
import Amplify from 'aws-amplify';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { AmplifyAuthenticator, AmplifySignIn, AmplifySignUp } from '@aws-amplify/ui-react';
import Header from './components/Header';
import Footer from './components/Footer';

Amplify.configure(AWS_CONFIG);
const queryClient = new QueryClient();
const Home = lazy(() => import('./pages/Home/Home'));
const About = lazy(() => import('./pages/About/About'));

const App = () => (
    <QueryClientProvider client={queryClient}>
        <Router>
            <AmplifyAuthenticator usernameAlias="email">
                <AmplifySignIn
                    headerText="Sign In To Synthesis Analyzer"
                    slot="sign-in"
                />
                <AmplifySignUp
                    headerText="Sign Up for Synthesis Analyzer"
                    slot="sign-up"
                    usernameAlias="email"
                    formFields={[
                        {
                            type: "email",
                            label: "Email",
                            placeholder: "Email",
                            inputProps: { required: true, autocomplete: "email" },
                        },
                        {
                            type: "password",
                            label: "Password",
                            placeholder: "Password",
                            inputProps: { required: true, autocomplete: "new-password" },
                        }
                    ]}
                />
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
            </AmplifyAuthenticator>
        </Router>
    </QueryClientProvider>
);

export default App;

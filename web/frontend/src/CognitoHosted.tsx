import { Amplify, Auth, Hub } from 'aws-amplify';
import styles from './login.module.css';

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';

Amplify.configure(AWS_CONFIG);

type UserAuthProps = {
    token: string;
    userEmail: string;
    signOut: () => void;
};

const UserAuthContext = createContext({} as UserAuthProps);

// @ts-ignore
export default function CognitoProvider({ children }) {
    const [token, setToken] = useState('');
    const [userEmail, setUserEmail] = useState('debug@gmail.com');
    const signOut = useCallback(() => {
        Auth.signOut().catch((error) => console.log(error));
    }, []);

    useEffect(() => {
        const unsubscribe = Hub.listen('auth', ({ payload: { event, data } }) => {
            switch (event) {
                case 'signIn':
                case 'cognitoHostedUI':
                    setToken(data.signInUserSession.idToken.jwtToken);
                    setUserEmail(data.signInUserSession.idToken.payload.email);
                    break;
                case 'signIn_failure':
                case 'cognitoHostedUI_failure':
                    console.log('Error', data);
                    break;
            }
        });

        // fetch the jwt token for use of api calls later
        Auth.currentAuthenticatedUser()
            .then((currentUser) => {
                setToken(currentUser.signInUserSession.idToken.jwtToken);
                setUserEmail(currentUser.signInUserSession.idToken.payload.email);
            })
            .catch(() => console.log('Not signed in'));

        return unsubscribe;
    }, []);

    const value = useMemo(
        () => ({
            token,
            userEmail,
            signOut
        }),
        [token, userEmail, signOut]
    );

    if (!AMPLIFY_ENABLED) {
        return <>{children}</>;
    }

    // the Phase Mapper app needs a token to work, show the login screen
    if (token === '') {
        return (
            <div className={styles.app}>
                You have to login to use the Phase Mapper app.
                <button className={styles.login} onClick={() => Auth.federatedSignIn()}>
                    Login
                </button>
            </div>
        );
    }

    return <UserAuthContext.Provider value={value}>{children}</UserAuthContext.Provider>;
}

function useUserAuthContext() {
    const context = useContext(UserAuthContext);
    if (context === undefined) {
        throw new Error('useUserAuth must be used within a UserAuthProvider');
    }
    return context;
}

export { useUserAuthContext };

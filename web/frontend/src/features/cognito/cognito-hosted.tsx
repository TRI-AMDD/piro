import { Amplify, Auth, Hub } from 'aws-amplify';
import { ReactNode, useCallback, useEffect, useMemo, useState } from 'react';
import { UserAuthContext } from './user-auth-context';
import PreLogin from './Prelogin';
Amplify.configure(AWS_CONFIG);

interface Props {
  children?: ReactNode;
}

export default function CognitoProvider({ children }: Props) {
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

  // the app needs a token to work, show the login screen
  if (token === '') {
    return <PreLogin />;
  }

  return <UserAuthContext.Provider value={value}>{children}</UserAuthContext.Provider>;
}

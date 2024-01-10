import { Amplify, Auth, Hub } from 'aws-amplify';
import { ReactNode, useCallback, useEffect, useMemo, useState } from 'react';
import { UserAuthContext } from './user-auth-context';
import Login from '@/components/loginheader';
import LoginFooter from '@/components/loginfooter';
import LoginCSS from './login.module.css';
import logo from './loginpic.png';
import logo2 from './blackimage.png'
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
    return (
      <div>
      <header className={LoginCSS.AppHeader}>
        <img src={logo2} alt="Logo" width={"150px"}/>
        <button className={LoginCSS.loginsignin} onClick={() => Auth.federatedSignIn()}>SIGN IN</button>
    </header>
      <div className={LoginCSS.firstblock}>
        <div className={LoginCSS.piroheader}>
        Piro Synthesis Analyzer
        </div>
        <div className={LoginCSS.firstblockbody}>
        The Piro Synthesis Analyzer is an application that assists with rational planning of solid-state synthesis routes for inorganics. It is a recommendation system for navigation and planning of synthesis of inorganic materials based on classical nucleation theory and semi-empirical, data-driven approximations to its parts. Currently, the app works with Materials Project data via its Rester API. Sign in to learn more and use the tool.
        </div>
        <button className={LoginCSS.signinbutton}><div className={LoginCSS.signincontent} onClick={() => Auth.federatedSignIn()}>Go to sign in page</div></button>
        <p className={LoginCSS.donthavesignin}>Don’t have a sign in?<i className={LoginCSS.requestsignin}>Request one here</i> </p>
      </div>
      <div className={LoginCSS.secondblock}>
        <div className={LoginCSS.secondblockcontent}>
        <h4 className={LoginCSS.secondblockheader}>More about the tool</h4><p className={LoginCSS.secondblockmargin}>Piro creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic conditions and a precursor library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics: nucleation barrier and phase-selection.</p> 
<p className={LoginCSS.secondblockmargin}>It allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree (i.e. laying out the reaction pathways necessary to arrive at the target from practical/purchasable reagents/starting materials).</p></div>
<img className={LoginCSS.imagecontent} src={logo} alt="Logo"/>

      </div>
      <div className={LoginCSS.thirdblock}>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Contact</h4>
          <p className={LoginCSS.thirdblockcontent}>The Piro platform is developed by a team of researchers and software developers at Toyota Research Institute: Murat Aykol, Joseph Montoya, Jens Hummelshøj, Chris Fajardo, Michael Puzon, and Reko Ong.</p>
<br></br>
<p className={LoginCSS.thirdblockcontent}>To request access or if you have questions about logging in, reach out to us at <a href="mailto:em-piro@tri.global" className={LoginCSS.mailstyle}>em-piro@tri.global</a>.</p>
        </div>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Code</h4>
          <p className={LoginCSS.thirdblockcontent}>If you’d like to use the python interface to Piro, or to access the code for this site, please visit our github page: <u><a href="https://github.com/TRI-AMDD/piro">https://github.com/TRI-AMDD/piro</a></u>. Tutorial jupyter notebooks showing how to use Piro locally are provided in the notebooks folder.</p>
        </div>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Manuscript</h4>
          <p className={LoginCSS.thirdblockcontent}>For more information about the physical theory behind Piro, please read our paper, “Rational Solid-State Synthesis Routes for Inorganic Materials” by Murat Aykol et al. (<u><a href="https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888">https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888</a></u>).</p>
        </div>
      </div>
      <LoginFooter/>
      </div>
    );
  }

  return <UserAuthContext.Provider value={value}>{children}</UserAuthContext.Provider>;
}

import LoginCSS from './login.module.css';
import { Auth } from 'aws-amplify';
import LoginFooter from '@/components/loginfooter';
import logo from './loginpic.png';
import logo2 from './blackimage.png';

export default function PreLogin() {
  return (
    <div>
      <header className={LoginCSS.AppHeader}>
        <img src={logo2} alt="Logo" width={'150px'} />
        <button className={LoginCSS.loginsignin} onClick={() => Auth.federatedSignIn()}>
          <div className={LoginCSS.signintext}>SIGN IN</div>
        </button>
      </header>
      <div className={LoginCSS.firstblock}>
        <div className={LoginCSS.piroheader}>Piro Synthesis Analyzer</div>
        <div className={LoginCSS.firstblockbody}>
          The Piro Synthesis Analyzer is an application that assists with rational planning of solid-state synthesis
          routes for inorganics. It is a recommendation system for navigation and planning of synthesis of inorganic
          materials based on classical nucleation theory and semi-empirical, data-driven approximations to its parts.
          Currently, the app works with Materials Project data via its Rester API. Sign in to learn more and use the
          tool.
        </div>
        <button className={LoginCSS.signinbutton}>
          <div className={LoginCSS.signincontent} onClick={() => Auth.federatedSignIn()}>
            Go to sign in page
          </div>
        </button>
        <p className={LoginCSS.donthavesignin}>
          Don’t have a sign in?<span> </span>
          <a href="mailto:em-piro@tri.global" target="_blank" rel="noreferrer" className={LoginCSS.requestsignin}>
            Request one here
          </a>{' '}
        </p>
      </div>
      <div className={LoginCSS.secondblock}>
        <div className={LoginCSS.secondblockcontent}>
          <h4 className={LoginCSS.secondblockheader}>More about the tool</h4>
          <p className={LoginCSS.secondblockmargin}>
            Piro creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic
            conditions and a precursor library, where favorable routes are those that are (nearly) Pareto optimal in
            terms of two metrics: nucleation barrier and phase-selection.
          </p>
          <p className={LoginCSS.secondblockmargin}>
            It allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree (i.e.,
            laying out the reaction pathways necessary to arrive at the target from practical/purchasable
            reagents/starting materials).
          </p>
        </div>
        <img src={logo} alt="image" style={{ maxWidth: '100%', maxHeight: '100%', display: 'block' }} />
      </div>
      <div className={LoginCSS.thirdblock}>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Contact</h4>
          <p className={LoginCSS.thirdblockcontent}>
            The Piro platform is developed by a team of researchers and software developers at Toyota Research
            Institute: Murat Aykol, Joseph Montoya, Jens Hummelshøj, Chris Fajardo, Michael Puzon, and Reko Ong.
          </p>
          <br></br>
          <p className={LoginCSS.thirdblockcontent}>
            To request access or if you have questions about logging in, reach out to us at{' '}
            <a href="mailto:em-piro@tri.global" target="_blank" rel="noreferrer" className={LoginCSS.mailstyle}>
              em-piro@tri.global
            </a>
            .
          </p>
        </div>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Code</h4>
          <p className={LoginCSS.thirdblockcontent}>
            If you’d like to use the Python interface to Piro, or to access the code for this site, please visit our
            GitHub page:{' '}
            <u>
              <a href="https://github.com/TRI-AMDD/piro" target="_blank" rel="noreferrer">
                https://github.com/TRI-AMDD/piro
              </a>
            </u>
            . Tutorial Jupyter notebooks showing how to use Piro locally are provided in the{' '}
            <a href="https://github.com/TRI-AMDD/piro/tree/main/piro/notebooks" target="_blank" rel="noreferrer">
              <u>notebooks folder</u>
            </a>
            .
          </p>
        </div>
        <div>
          <h4 className={LoginCSS.thirdblockheader}>Manuscript</h4>
          <p className={LoginCSS.thirdblockcontent}>
            For more information about the physical theory behind Piro, please read our paper, “Rational Solid-State
            Synthesis Routes for Inorganic Materials” by Murat Aykol et al. (
            <u>
              <a href="https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888" target="_blank" rel="noreferrer">
                https://pubs.acs.org/doi/abs/10.1021/jacs.1c04888
              </a>
            </u>
            ).
          </p>
        </div>
      </div>
      <LoginFooter />
    </div>
  );
}

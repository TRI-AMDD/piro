import styles from './components.module.css';
import { useUserAuth } from '@/features/cognito/use-user-auth';
import logo from '../images/blackimage.png';

export default function Header() {
  const { signOut } = useUserAuth();

  return (
    <header className={styles.AppHeader}>
      <a href="/">
        <img src={logo} alt="Logo" width={'150px'} />
      </a>{' '}
      <h3>Piro Synthesis Analyzer</h3>
      <a href="/about" className={styles.Aboutlink}>
        About
      </a>
      {AMPLIFY_ENABLED && (
        <button className={styles.Signout} onClick={signOut}>
          SIGN OUT
        </button>
      )}
    </header>
  );
}

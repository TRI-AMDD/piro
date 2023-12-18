import { AmplifySignOut } from '@aws-amplify/ui-react';
import styles from './components.module.css';


export default function Header() {
    return (
        <header className={styles.AppHeader}>
            <h3>Piro Synthesis Analyzer</h3>
            <a href="/about" className={styles.Aboutlink}>About</a>
            <button className={styles.Signout}>Sign Out</button>
            {AMPLIFY_ENABLED && <AmplifySignOut />}
            
        </header>
    );
}
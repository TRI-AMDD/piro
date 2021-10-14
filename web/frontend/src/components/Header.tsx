import { AmplifySignOut } from '@aws-amplify/ui-react';
import styles from './components.module.css';

export default function Header() {
    return (
        <header className={styles.AppHeader}>
            <h1>Synthesis Analyzer</h1>
            <AmplifySignOut />
        </header>
    );
}

import styles from './components.module.css';
import { Button } from "@material-tailwind/react";
import { useUserAuth } from '@/features/cognito/use-user-auth';

export default function Header() {
    const { signOut } = useUserAuth();

    return (
        <header className={styles.AppHeader}>
            <h1>Synthesis Analyzer</h1>
            {AMPLIFY_ENABLED && <Button onClick={signOut}>Sign Out</Button>}
        </header>
    );
}

import { Button } from "@material-tailwind/react";
import styles from './components.module.css';
import { useUserAuth } from '@/features/cognito/use-user-auth';
import logo from '../images/blackimage.png'

export default function Login() {
    const { signOut } = useUserAuth();

    return (
        <header className={styles.AppHeader}>
        <img src={logo} alt="Logo" width={"150px"}/>
        <button className={styles.loginsignin} onClick={signOut}>SIGN IN</button>
    </header>
    );
}
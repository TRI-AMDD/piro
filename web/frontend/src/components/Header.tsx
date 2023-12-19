import { AmplifySignOut } from '@aws-amplify/ui-react';
import styles from './components.module.css';
import logo from '../images/blackimage.png'

export default function Header() {
    //var logo = require('../images/Toyota_Research_Institute_Logo.png')
    console.log(logo)
    return (
        <header className={styles.AppHeader}>
            <img src={logo} alt="Logo" width={"150px"}/>
            <h3>Piro Synthesis Analyzer</h3>
            <a href="/about" className={styles.Aboutlink}>About</a>
            <button className={styles.Signout}>SIGN OUT</button>
            {AMPLIFY_ENABLED && <AmplifySignOut />}
        </header>
    );
}
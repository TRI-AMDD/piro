import styles from './components.module.css';
import { Link } from 'react-router-dom';

export default function Footer() {
    const year = new Date().getFullYear();

    return (
        <footer className={styles.Footer}>
            <p><Link  className={styles.Footerlink} to="/about">About</Link></p>
            <p><Link className={styles.Footerlink} to="/about">Code</Link></p>
            <p><Link className={styles.Footerlink} to="/about">Manuscript</Link></p>
            <p ><a className={styles.Footerlink} href="https://www.tri.global/privacy-policy/" target="_blank" rel="noreferrer">Privacy Policy</a></p>
            <p className={styles.Footercopyright}>© Copyright Toyota Research Institute {year}</p>
        </footer>
    );
}

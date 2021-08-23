import styles from './components.module.css';
import { Link } from 'react-router-dom';

export default function Footer() {
    const year = new Date().getFullYear();

    return (
        <footer className={styles.Footer}>
            <p>© Copyright Toyota Research Institute {year}</p>
            <p><Link to="/about">About</Link></p>
            <p><a href="https://www.tri.global/privacy-policy/" target="_blank" rel="noreferrer">Privacy Policy</a></p>
        </footer>
    );
}

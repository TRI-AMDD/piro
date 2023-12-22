import styles from './components.module.css';
import { Link } from 'react-router-dom';

interface FooterProps{
    highlight:(id:string) =>void;
}
const Footer: React.FC<FooterProps> = ({highlight}) => {
    const handleLinkClick = (id:string)=>{
        highlight(id);
    }
    const year = new Date().getFullYear();

    return (
        <footer className={styles.Footer}>
            <p><Link  className={styles.Footerlink} to="/about">About</Link></p>
            <p><Link className={styles.Footerlink} to="/about" onClick={() => handleLinkClick("code")}>Code</Link></p>
            <p><Link className={styles.Footerlink} to="/about" onClick={() => handleLinkClick("manuscript")}>manuscript</Link></p>
            <p ><a className={styles.Footerlink} href="https://www.tri.global/privacy-policy/" target="_blank" rel="noreferrer">Privacy Policy</a></p>
            <p className={styles.Footercopyright}>© Copyright Toyota Research Institute {year}</p>
        </footer>
    );
};

export default Footer;
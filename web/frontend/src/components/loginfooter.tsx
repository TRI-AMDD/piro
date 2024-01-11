import styles from './components.module.css';

export default function LoginFooter() {
  const year = new Date().getFullYear();

  return (
    <footer className={styles.Footer}>
      <p className={styles.Footercopyright}>© Copyright Toyota Research Institute {year}</p>
    </footer>
  );
}

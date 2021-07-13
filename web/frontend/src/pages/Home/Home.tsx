import styles from './Home.module.css';
import Form from './Form';

function Home() {
    return (
        <div className={styles.App}>
            <header className={styles.AppHeader}>
                <h1>Synthesis Analyzer</h1>
            </header>
            <Form />
        </div>
    );
}

export default Home;

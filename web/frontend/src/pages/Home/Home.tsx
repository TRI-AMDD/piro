import Form from './Form';
import SynthesisPlot from "./SynthesisPlot";
import { useState } from "react";
import styles from './Home.module.css';

function Home() {
    const [request, setRequest] = useState<any>();

    return (
        <div className={styles.App}>
            <header className={styles.AppHeader}>
                <h1>Synthesis Analyzer</h1>
            </header>
            <Form setRequest={setRequest} />
            {request && <SynthesisPlot request={request} />}
        </div>
    );
}

export default Home;

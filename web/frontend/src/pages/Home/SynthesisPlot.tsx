import Plot from 'react-plotly.js';
import { useQuery } from "react-query";
import styles from './Home.module.css';

interface Props {
    request: any;
}

function SynthesisPlot(props: Props) {
    const { request } = props;
    const { data, error, isLoading } = useQuery('cats', () => fetch('/sample_resp.json').then((res) => res.json()));

    if (!request) {
        return null;
    }

    if (isLoading) return <>Loading...</>;

    if (error) {
        return <>An error has occurred</>;
    }

    console.log(data);

    return (
        <div className={styles.Plot}>
            <Plot {...data} />
        </div>
    );
}

export default SynthesisPlot;

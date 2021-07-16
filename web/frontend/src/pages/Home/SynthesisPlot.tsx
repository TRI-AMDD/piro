import Plot from 'react-plotly.js';
import { UseMutationResult } from "react-query";
import styles from './Home.module.css';
import { Loading } from '@toyota-research-institute/lakefront';

interface Props {
    mutation: UseMutationResult<any, unknown, void, unknown>;
}

function SynthesisPlot(props: Props) {
    const { mutation } = props;
    const { data, error, isLoading } = mutation;

    if (isLoading) return (
        <div className={styles.Loading}>
            <Loading
                animated
                height={24}
                label="Loading..."
                width={24}
            />
        </div>
    );

    if (error) {
        return <>An error has occurred</>;
    }

    if (!data) {
        return null;
    }

    return (
        <div className={styles.Plot}>
            <Plot {...data} />
        </div>
    );
}

export default SynthesisPlot;

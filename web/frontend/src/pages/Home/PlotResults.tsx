import Plot from 'react-plotly.js';
import { Loading } from '@toyota-research-institute/lakefront';
import { usePlotData } from "./usePlotData";
import styles from './Home.module.css';
import ErrorMessage from "./ErrorMessage";

interface Props {
    taskId: string;
}

function PlotResults(props: Props) {
    const { taskId } = props;
    const { data, error, isLoading } = usePlotData(taskId);

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
        return <ErrorMessage error="Error encountered" />;
    }

    if (!data) {
        return null;
    }

    if (data.status == "started" || data.status == "pending") {
        return (
            <div className={styles.Loading}>
                <Loading
                    animated
                    height={24}
                    label="Request initiated. Loading Results..."
                    width={24}
                />
            </div>
        );
    }

    if (data.status == "failure") {
        return <ErrorMessage error={data.error_message}/>;
    }

    if (data.status == "invalid") {
        return <ErrorMessage error="Invalid request sent." />;
    }

    return (
        <div className={styles.Plot}>
            <Plot {...data.result} />
        </div>
    );
}

export default PlotResults;

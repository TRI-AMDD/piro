import { UseMutationResult } from "react-query";
import { Loading } from '@toyota-research-institute/lakefront';
import styles from './Home.module.css';
import ErrorMessage from "./ErrorMessage";
import PlotResults from './PlotResults';

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
        return <ErrorMessage error="An error has occurred when making the api call." />;
    }

    if (!data) {
        return null;
    }

    if (data.detail) {
        return <ErrorMessage error={data.detail} />;
    }

    if (data.error_message) {
        return <ErrorMessage error={data.error_message} />;
    }    
    
    return (
        <PlotResults key={data.task_id} taskId={data.task_id} />
    );    
}

export default SynthesisPlot;
